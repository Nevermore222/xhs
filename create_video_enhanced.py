from moviepy.editor import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random

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
    "你最想和对方一起完成的事情是什么？",
    "如何描述你们的初次约会？",
    "你觉得情侣间最重要的是什么？",
    "什么时候觉得对方特别可靠？",
    "对方哪个小习惯让你特别喜欢？",
    "你们第一次一起做饭做的什么？",
    "最想和对方一起看的电影是？",
    "你们之间有什么特别的纪念日庆祝方式？",
    "你给对方取过什么昵称？",
    "最想一起完成的愿望清单是什么？",
    "和对方一起最放松的时刻是？"
]

# 视频参数
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 70
FONT_COLOR = (255, 255, 255)
TITLE_FONT_SIZE = 45
DURATION = 60  # 视频总时长(秒)
FPS = 30
QUESTION_DURATION = 0.08  # 每个问题显示时间(秒)

# 渐变背景颜色对
GRADIENT_COLORS = [
    [(142, 68, 173), (41, 128, 185)],  # 紫色到蓝色
    [(41, 128, 185), (22, 160, 133)],  # 蓝色到绿色
    [(243, 156, 18), (211, 84, 0)],    # 黄色到橙色
    [(231, 76, 60), (192, 57, 43)],    # 亮红到深红
    [(52, 152, 219), (155, 89, 182)],  # 蓝色到紫色
]

def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        # 计算当前位置的颜色
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        
        # 绘制水平线
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def add_decorative_elements(img):
    """添加装饰元素到背景"""
    draw = ImageDraw.Draw(img)
    
    # 添加一些随机圆形装饰
    for _ in range(20):
        x = random.randint(0, VIDEO_WIDTH)
        y = random.randint(0, VIDEO_HEIGHT)
        size = random.randint(10, 50)
        opacity = random.randint(30, 100)
        color = (255, 255, 255, opacity)
        draw.ellipse((x, y, x+size, y+size), fill=color)
    
    # 添加模糊效果
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    return img

def create_text_clip(text, duration):
    # 随机选择渐变颜色
    colors = random.choice(GRADIENT_COLORS)
    
    # 创建渐变背景
    img = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, colors[0], colors[1])
    
    # 添加装饰元素
    img = add_decorative_elements(img)
    
    draw = ImageDraw.Draw(img)
    
    # 设置字体
    try:
        font = ImageFont.truetype("simhei.ttf", FONT_SIZE)
        title_font = ImageFont.truetype("simhei.ttf", TITLE_FONT_SIZE)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # 添加标题
    title = "情侣真心话大冒险"
    title_width = draw.textlength(title, font=title_font)
    draw.text(((VIDEO_WIDTH - title_width) // 2, 150), title, font=title_font, fill=(255, 255, 255))
    
    # 绘制装饰线
    line_y = 220
    draw.line([(VIDEO_WIDTH//4, line_y), (VIDEO_WIDTH*3//4, line_y)], fill=(255, 255, 255), width=2)
    
    # 文本换行处理
    lines = textwrap.wrap(text, width=16)
    line_height = FONT_SIZE + 15
    
    # 计算文本总高度
    text_height = len(lines) * line_height
    
    # 文本居中显示
    y_position = (VIDEO_HEIGHT - text_height) // 2
    
    # 为文本添加轻微阴影效果，增强可读性
    shadow_offset = 3
    
    # 绘制文本和阴影
    for line in lines:
        # 计算每行文本宽度，使其居中
        line_width = draw.textlength(line, font=font)
        x_position = (VIDEO_WIDTH - line_width) // 2
        
        # 绘制阴影
        draw.text((x_position + shadow_offset, y_position + shadow_offset), 
                 line, font=font, fill=(0, 0, 0, 128))
        
        # 绘制主文本
        draw.text((x_position, y_position), line, font=font, fill=FONT_COLOR)
        y_position += line_height
    
    # 添加底部提示
    tip = "随时暂停视频回答问题"
    tip_width = draw.textlength(tip, font=title_font)
    draw.text(((VIDEO_WIDTH - tip_width) // 2, VIDEO_HEIGHT - 250), 
             tip, font=title_font, fill=(255, 255, 255))
    
    # 转换为数组
    img_array = np.array(img)
    
    # 创建文本剪辑
    text_clip = ImageClip(img_array).set_duration(duration)
    return text_clip

def create_intro_clip():
    """创建视频开头介绍片段"""
    # 使用紫色渐变背景
    img = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (142, 68, 173), (41, 128, 185))
    img = add_decorative_elements(img)
    
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        large_font = ImageFont.truetype("simhei.ttf", 100)
        medium_font = ImageFont.truetype("simhei.ttf", 60)
    except:
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
    
    # 绘制标题
    title = "情侣真心话"
    title_width = draw.textlength(title, font=large_font)
    draw.text(((VIDEO_WIDTH - title_width) // 2, VIDEO_HEIGHT//2 - 200), 
             title, font=large_font, fill=(255, 255, 255))
    
    # 绘制说明
    instructions = [
        "玩法说明",
        "1. 随时暂停视频",
        "2. 停在哪个问题就回答哪个",
        "3. 双方轮流操作",
        "4. 真诚回答每个问题"
    ]
    
    y_pos = VIDEO_HEIGHT//2
    for line in instructions:
        line_width = draw.textlength(line, font=medium_font)
        draw.text(((VIDEO_WIDTH - line_width) // 2, y_pos), 
                 line, font=medium_font, fill=(255, 255, 255))
        y_pos += 100
    
    # 转换为数组并创建剪辑
    img_array = np.array(img)
    intro_clip = ImageClip(img_array).set_duration(5)  # 5秒介绍时间
    
    return intro_clip

def create_video():
    print("开始生成视频...")
    
    # 创建介绍片段
    intro_clip = create_intro_clip()
    
    # 创建问题剪辑列表
    clips = []
    
    # 根据视频时长和每个问题的持续时间计算循环次数
    total_questions_needed = int((DURATION - 5) / QUESTION_DURATION)  # 减去介绍片段时长
    
    print(f"正在生成{total_questions_needed}个问题片段...")
    
    # 循环添加问题，直到达到所需的总问题数
    for i in range(total_questions_needed):
        if i % 50 == 0:
            print(f"已生成 {i}/{total_questions_needed} 个问题片段...")
        question_index = i % len(questions)
        clips.append(create_text_clip(questions[question_index], QUESTION_DURATION))
    
    # 连接所有问题剪辑
    questions_clip = concatenate_videoclips(clips, method="compose")
    
    # 将介绍和问题片段连接起来
    final_clip = concatenate_videoclips([intro_clip, questions_clip], method="compose")
    
    print("正在渲染最终视频...")
    
    # 导出视频
    final_clip.write_videofile("couples_truth_questions_enhanced.mp4", fps=FPS, codec='libx264')
    print("视频创建完成: couples_truth_questions_enhanced.mp4")

if __name__ == "__main__":
    create_video() 