#!/bin/bash

# 目标文件夹
INPUT_DIR="/mnt/ssd2/videos/f3set-tennis"   # 你的视频文件夹路径
OUTPUT_DIR="/mnt/ssd2/lingyu/FlowFormer/tennis_frames"  # 输出拆分的帧的目标文件夹

# 创建输出文件夹（如果不存在的话）
mkdir -p "$OUTPUT_DIR"

# 遍历目录中的每个 MP4 文件
for file in "$INPUT_DIR"/*.mp4; do
    # 提取视频文件名（去掉扩展名）
    filename=$(basename "$file" .mp4)

    # 创建对应的视频文件夹
    mkdir -p "$OUTPUT_DIR/$filename"

    # 使用 FFmpeg 拆分视频为帧（30 FPS）
    ffmpeg -i "$file" -q:v 2 -vf "fps=30" "$OUTPUT_DIR/$filename/frame_%05d.png"
done
