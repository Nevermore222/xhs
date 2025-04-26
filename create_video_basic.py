import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
import time

# 问题库
questions = [
    "你最喜欢我身上的哪个部位？",
    "你和前任分手的真实原因是什么？",
    "你有没有偷偷删除过我们的聊天记录？",
    "你最后一次说谎是什么时候？",
    "最让你感到心动的一次约会是什么时候？",
    "如果可以改变我的一个习惯，你会选择什么？",
    "你有没有因为我做过的事情而哭过？",
    "你觉得我最大的缺点是什么？",
    "在我不在的时候，你会偷偷做什么？",
    "你曾经为我放弃过什么？",
    "你最不愿意让我知道的秘密是什么？",
    "第一次见我的时候你真实的想法是什么？",
    "你有没有瞒着我偷偷联系过异性？",
    "如果让你选择和我的一个朋友约会，你会选谁？",
    "你有没有觉得我的某个朋友对你有好感？",
    "你有没有怀疑过我对你不忠？",
    "你最羡慕我的哪一点？",
    "我做过最让你感动的一件事是什么？",
    "和我在一起后你有什么改变？",
    "你最不满意我们关系中的什么？",
    "我做过最让你伤心的事情是什么？",
    "你有没有想过和我分手？",
    "最近有什么话想对我说但一直没说出口？",
    "你最害怕我发现你的什么秘密？",
    "你有没有故意不回我消息？",
    "和我在一起的哪个瞬间让你最开心？",
    "你有没有把我们的私密事情告诉过别人？",
    "你的择偶标准里有哪些是我不符合的？",
    "你会为了我放弃你的梦想吗？",
    "如果我们明天就要分手，你最想对我说什么？"
]

# 视频参数
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 65
FONT_COLOR = (255, 255, 255)
BG_COLOR = (246, 209, 220)  # 淡粉色背景
DURATION = 30  # 视频总时长(秒)
FPS = 30
QUESTION_DURATION = 1  # 每个问题显示帧数，改小以加快切换速度

def create_text_frame(text):
    """创建带有文字的单帧"""
    # 创建带有文字的图像
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 创建简单渐变背景
    for y in range(VIDEO_HEIGHT):
        # 从上到下的粉紫色渐变
        r = int(246 - (y/VIDEO_HEIGHT) * 40)  # 从淡粉到深粉
        g = int(209 - (y/VIDEO_HEIGHT) * 70)
        b = int(220 + (y/VIDEO_HEIGHT) * 35)  # 增加蓝色成分，形成紫色调
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b))
    
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
        
        # 添加文字阴影提高可读性
        shadow_offset = 2
        draw.text((x_position + shadow_offset, y_position + shadow_offset), 
                 line, font=font, fill=(50, 50, 50, 180))
        
        # 绘制主文本
        draw.text((x_position, y_position), line, font=font, fill=FONT_COLOR)
        y_position += line_height
    
    # 添加提示文字
    instruction_text = "随时暂停视频，根据停在的问题回答"
    try:
        small_font = ImageFont.truetype("simhei.ttf", 40)
    except:
        small_font = ImageFont.load_default()
    
    instr_width = draw.textlength(instruction_text, font=small_font)
    
    # 添加提示文字底部半透明背景
    instr_y = 100
    draw.rectangle([(VIDEO_WIDTH - instr_width) // 2 - 10, instr_y - 5, 
                   (VIDEO_WIDTH + instr_width) // 2 + 10, instr_y + 45], 
                   fill=(0, 0, 0, 60))
    
    draw.text(((VIDEO_WIDTH - instr_width) // 2, instr_y), 
             instruction_text, font=small_font, fill=FONT_COLOR)
    
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