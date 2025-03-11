import os
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import imageio
import argparse
import argparse
import os
import time
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from configs.submissions import get_cfg as get_submission_cfg
from core.utils.misc import process_cfg
# import datasets
from core.FlowFormer import build_flowformer
from core.utils.utils import InputPadder
from core.utils import flow_viz


@torch.no_grad()
def compute_flow(model, image1_path, image2_path):
    """ 计算两张图片之间的光流 """
    image1 = imageio.imread(image1_path)
    image2 = imageio.imread(image2_path)

    image1 = torch.from_numpy(image1).permute(2, 0, 1).float().unsqueeze(0).cuda()
    image2 = torch.from_numpy(image2).permute(2, 0, 1).float().unsqueeze(0).cuda()

    padder = InputPadder(image1.shape)
    image1, image2 = padder.pad(image1, image2)

    flow_pre, _ = model(image1, image2)
    flow_pre = padder.unpad(flow_pre[0]).cpu().numpy()

    return flow_pre


@torch.no_grad()
def process_videos(input_root, output_root, model):
    """ 遍历输入文件夹，处理所有的视频和pair文件夹 """
    cnt = 0
    for video_folder in sorted(os.listdir(input_root)):
        video_path = os.path.join(input_root, video_folder)
        if not os.path.isdir(video_path):
            continue

        output_video_path = os.path.join(output_root, video_folder)
        os.makedirs(output_video_path, exist_ok=True)

        for pair_folder in sorted(os.listdir(video_path)):
            pair_path = os.path.join(video_path, pair_folder)
            if not os.path.isdir(pair_path):
                continue

            frame1_path = os.path.join(pair_path, "frame1.png")
            frame2_path = os.path.join(pair_path, "frame2.png")
            if not os.path.exists(frame1_path) or not os.path.exists(frame2_path):
                print(f"Missing frames in {pair_path}, skipping.")
                continue

            flow = compute_flow(model, frame1_path, frame2_path)

            # 保存 .npy 文件
            npy_output = os.path.join(output_video_path, f"{pair_folder}.npy")
            np.save(npy_output, flow)

            # 生成光流图像并保存
            # 确保 `flow` 是 numpy 数组
            if isinstance(flow, torch.Tensor):
                flow = flow.cpu().numpy()

            # 修正 shape: 从 [2, H, W] 变成 [H, W, 2]
            if flow.shape[0] == 2:
                flow = flow.transpose(1, 2, 0)
            flow_img = flow_viz.flow_to_image(flow)

            flow_image = Image.fromarray(flow_img)
            flow_image.save(os.path.join(output_video_path, f"{pair_folder}.png"))

            # print(f"Processed {pair_path}, saved results to {output_video_path}")
        # break
        cnt+=1
        print(cnt)
        break
    print("Finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to trained model file')
    parser.add_argument('--input', required=True, help='Path to input root directory (tennis_pairs)')
    parser.add_argument('--output', required=True, help='Path to output root directory (tennis_flow)')
    args = parser.parse_args()

    # 加载模型
    # cfg = None
    cfg = get_submission_cfg()
    cfg.update(vars(args))  # 把 argparse 解析的参数加进去
    model = torch.nn.DataParallel(build_flowformer(cfg))
    model.load_state_dict(torch.load(args.model))
    model.cuda()
    model.eval()

    # 处理所有视频
    process_videos(args.input, args.output, model)
