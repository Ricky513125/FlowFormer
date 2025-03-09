import os
import glob
from shutil import copyfile


def create_frame_pairs(input_folder, output_folder):
    """ 创建相邻帧对（frame1.png 和 frame2.png） """
    video_folders = sorted(glob.glob(os.path.join(input_folder, "*")))

    os.makedirs(output_folder, exist_ok=True)

    for video_folder in video_folders:
        frames = sorted(glob.glob(os.path.join(video_folder, "*.png")))

        if len(frames) < 2:
            continue  # 跳过小于 2 帧的视频片段

        video_name = os.path.basename(video_folder)

        for i in range(len(frames) - 1):
            pair_folder = os.path.join(output_folder, f"{video_name}_pair_{i:05d}")
            os.makedirs(pair_folder, exist_ok=True)
            copyfile(frames[i], os.path.join(pair_folder, "frame1.png"))
            copyfile(frames[i + 1], os.path.join(pair_folder, "frame2.png"))


if __name__ == "__main__":
    create_frame_pairs("/mnt/ssd2/lingyu/FlowFormer/tennis_frames", "/mnt/ssd2/lingyu/FlowFormer/tennis_pairs")

# import json
# import os
# from tqdm import tqdm
# import cv2
# import warnings
# warnings.filterwarnings('ignore')
#
# # save images
# def save_imgs(cap, start, end, file_name, dim=224):
#     # if not os.path.isdir('./vid_frames_%d' % dim):
#     #     os.mkdir('./vid_frames_%d' % dim)
#     # path = os.path.join('./vid_frames_%d' % dim, file_name)
#     if not os.path.isdir('/mnt/ssd2/lingyu/Tennis/vid_frames_%d' % dim):
#         os.mkdir('/mnt/ssd2/lingyu/Tennis/vid_frames_%d' % dim)
#     path = os.path.join('/mnt/ssd2/lingyu/Tennis/vid_frames_%d' % dim, file_name)
#     if not os.path.isdir(path):
#         os.mkdir(path)
#     count = 0
#     cap.set(1, start)
#     for t in range(start, end):
#         # frame_path = './vid_frames_%d/%s/%06d.jpg' % (dim, file_name, count)
#         frame_path = '/mnt/ssd2/lingyu/Tennis/vid_frames_%d/%s/%06d.jpg' % (dim, file_name, count)
#         # if not os.path.exists(frame_path):
#         _, frame = cap.read()
#         H, W, _ = frame.shape
#         resized = cv2.resize(frame, (W * dim // H, dim))
#         cv2.imwrite(frame_path, resized)
#         count += 1
#
# data_name = ['train', 'val', 'test']
# dim = 224
# for i, name in enumerate(data_name):
#     print(name)
#     out = []
#     # json_file = json.load(open('./data/f3tennis/%s.json' % name))
#     json_file = json.load(open('/mnt/ssd2/lingyu/Tennis/%s.json' % name))
#     for clip in tqdm(json_file):
#         match_id = '_'.join(clip['video'].split('_')[:-2])
#         # video_name = './videos/%s.mp4' % match_id
#         video_name = '/mnt/ssd2/videos/f3set-tennis/%s.mp4' % match_id
#         cap = cv2.VideoCapture(video_name)
#         # save images
#         start, end = int(clip['video'].split('_')[-2]), int(clip['video'].split('_')[-1])
#         file_name = clip['video']
#         save_imgs(cap, start, end, file_name, dim=dim)