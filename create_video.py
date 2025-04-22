from moviepy.editor import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap

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
QUESTION_DURATION = 0.1  # 每个问题显示时间(秒)

def create_text_clip(text, duration):
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
    
    # 转换为数组
    img_array = np.array(img)
    
    # 创建文本剪辑
    text_clip = ImageClip(img_array).set_duration(duration)
    return text_clip

def create_video():
    # 创建问题剪辑列表
    clips = []
    
    # 根据视频时长和每个问题的持续时间计算循环次数
    total_questions_needed = int(DURATION / QUESTION_DURATION)
    
    # 循环添加问题，直到达到所需的总问题数
    for i in range(total_questions_needed):
        question_index = i % len(questions)
        clips.append(create_text_clip(questions[question_index], QUESTION_DURATION))
    
    # 连接所有剪辑
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # 添加提示文字
    instruction_text = "随时暂停视频，根据停在的问题回答"
    instruction_clip = TextClip(instruction_text, fontsize=40, color='white', size=(VIDEO_WIDTH, 100))
    instruction_clip = instruction_clip.set_position(('center', 100)).set_duration(DURATION)
    
    # 合成最终视频
    final_video = CompositeVideoClip([final_clip, instruction_clip])
    
    # 导出视频
    final_video.write_videofile("couples_truth_questions.mp4", fps=FPS, codec='libx264')
    print("视频创建完成: couples_truth_questions.mp4")

if __name__ == "__main__":
    create_video() 