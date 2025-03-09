import os
import glob
from shutil import copyfile


def create_frame_pairs(input_folder, output_folder):
    """ 创建相邻帧对并保存为文件 """
    video_folders = sorted(glob.glob(os.path.join(input_folder, "*")))

    os.makedirs(output_folder, exist_ok=True)

    for video_folder in video_folders:
        frames = sorted(glob.glob(os.path.join(video_folder, "*.jpg")))

        if len(frames) < 2:
            continue  # 跳过小于 2 帧的视频片段

        video_name = os.path.basename(video_folder)

        # 创建相邻帧对
        for i in range(len(frames) - 1):
            pair_folder = os.path.join(output_folder, f"{video_name}_pair_{i:05d}")
            os.makedirs(pair_folder, exist_ok=True)

            # 获取相邻的两帧
            frame1_path = frames[i]
            frame2_path = frames[i + 1]

            # 保存帧对
            copyfile(frame1_path, os.path.join(pair_folder, "frame1.png"))
            copyfile(frame2_path, os.path.join(pair_folder, "frame2.png"))


if __name__ == "__main__":
    # 设定输入和输出文件夹路径
    input_folder = "/mnt/ssd2/lingyu/Tennis/vid_frames_224"
    output_folder = "/mnt/ssd2/lingyu/FlowFormer/tennis_pairs"

    # 创建帧对并保存
    create_frame_pairs(input_folder, output_folder)
