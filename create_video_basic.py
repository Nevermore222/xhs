import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time

# 问题库
questions = [
    "你最难忘的一次约会是什么时候？",
    "第一次见到对方的感觉是什么？",
    "你最喜欢对方的哪个特点？",
    "你们之间有什么特别的小秘密？",
    "最想和对方一起去哪里旅行？",
    "第一次牵手的场景还记得吗？",
    "你们之间最甜蜜的一个瞬间是什么？",
    "对方做过最让你感动的事是什么？",
    "你们之间最有趣的一次误会是什么？",
    "最想对对方说的一句话是什么？",
    "最欣赏对方的一个优点是什么？",
    "遇到对方后自己有什么改变？",
    "你们之间有什么特别的小习惯？",
    "第一次吵架是因为什么？",
    "平时吵架后是怎么和好的？",
    "觉得对方最可爱的瞬间是什么时候？",
    "如果可以和对方交换一天身份，你会做什么？",
    "两个人相处时最幸福的时刻是什么？",
    "你曾经为对方偷偷做过什么？",
    "你最想和对方一起完成的事情是什么？"
]

# 视频参数
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 65
FONT_COLOR = (255, 255, 255)
BG_COLOR = (41, 128, 185)  # 蓝色背景
DURATION = 30  # 视频总时长(秒)
FPS = 30
QUESTION_DURATION = 3  # 每个问题显示帧数

def create_text_frame(text):
    """创建带有文字的单帧"""
    # 创建带有文字的图像
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 设置字体
    try:
        font = ImageFont.truetype("simhei.ttf", FONT_SIZE)
    except:
        font = ImageFont.load_default()
    
    # 文本换行处理
    lines = textwrap.wrap(text, width=18)
    line_height = FONT_SIZE + 10
    
    # 计算文本总高度
    text_height = len(lines) * line_height
    
    # 文本居中显示
    y_position = (VIDEO_HEIGHT - text_height) // 2
    
    # 绘制文本
    for line in lines:
        # 计算每行文本宽度，使其居中
        line_width = draw.textlength(line, font=font)
        x_position = (VIDEO_WIDTH - line_width) // 2
        draw.text((x_position, y_position), line, font=font, fill=FONT_COLOR)
        y_position += line_height
    
    # 添加提示文字
    instruction_text = "随时暂停视频，根据停在的问题回答"
    try:
        small_font = ImageFont.truetype("simhei.ttf", 40)
    except:
        small_font = ImageFont.load_default()
    
    instr_width = draw.textlength(instruction_text, font=small_font)
    draw.text(((VIDEO_WIDTH - instr_width) // 2, 100), instruction_text, font=small_font, fill=FONT_COLOR)
    
    # 转换为NumPy数组，BGR格式
    img_array = np.array(img)
    # 从RGB转换为BGR (OpenCV使用BGR)
    img_array = img_array[:, :, ::-1].copy()
    
    return img_array

def create_video():
    print("开始生成视频...")
    
    # 创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('couples_truth_questions_basic.mp4', fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
    
    # 计算一共需要多少帧
    total_frames = DURATION * FPS
    frames_per_question = QUESTION_DURATION
    
    frame_count = 0
    question_index = 0
    
    print(f"开始生成视频，总共需要{total_frames}帧...")
    
    # 循环添加问题，直到达到所需的总帧数
    while frame_count < total_frames:
        if frame_count % 100 == 0:
            print(f"正在生成第{frame_count}/{total_frames}帧...")
        
        # 当前问题
        current_question = questions[question_index % len(questions)]
        
        # 创建当前帧
        frame = create_text_frame(current_question)
        
        # 写入帧
        out.write(frame)
        
        # 更新计数器
        frame_count += 1
        
        # 每隔几帧更换问题
        if frame_count % frames_per_question == 0:
            question_index += 1
    
    # 释放VideoWriter
    out.release()
    
    print(f"视频创建完成: couples_truth_questions_basic.mp4，共{frame_count}帧")

if __name__ == "__main__":
    start_time = time.time()
    create_video()
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒") 