import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import time
import random

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
FONT_SIZE = 70
FONT_COLOR = (255, 255, 255)
TITLE_FONT_SIZE = 45
DURATION = 30  # 视频总时长(秒)，压缩至30秒
FPS = 30
QUESTION_DURATION = 1  # 每个问题显示帧数，改小以加快切换速度
COVER_DURATION = 3  # 封面显示时间（秒）

# 渐变背景颜色对 (RGB格式)
GRADIENT_COLORS = [
    [(246, 209, 220), (188, 140, 191)],  # 淡粉色到淡紫色
    [(237, 187, 230), (165, 125, 190)],  # 浅粉紫到紫色
    [(220, 176, 196), (175, 138, 188)],  # 粉灰色到淡紫
    [(248, 200, 220), (193, 145, 193)],  # 浅粉红到淡紫红
    [(240, 219, 230), (198, 164, 196)],  # 极淡粉紫到中等淡紫
]

def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        # 计算当前位置的颜色 - 使用平滑的过渡
        progress = y / height
        # 使用平方函数使过渡更加平滑
        smooth_progress = progress * progress
        
        r = int(color1[0] + (color2[0] - color1[0]) * smooth_progress)
        g = int(color1[1] + (color2[1] - color1[1]) * smooth_progress)
        b = int(color1[2] + (color2[2] - color1[2]) * smooth_progress)
        
        # 绘制水平线
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def add_decorative_elements(img):
    """添加装饰元素到背景 - 减少元素数量和模糊效果，避免闪烁"""
    draw = ImageDraw.Draw(img)
    
    # 添加一些小星星或装饰点 - 减少数量并固定位置，避免闪烁
    for i in range(12):
        # 使用固定的随机种子，确保每帧的装饰元素位置一致
        x = int(VIDEO_WIDTH * (i * 0.083 + 0.05))
        y = int(VIDEO_HEIGHT * ((i % 4) * 0.2 + 0.1))
        size = 15 + (i % 3) * 10  # 10到35之间的大小
        opacity = 40 + (i % 4) * 10  # 不太透明，避免明显闪烁
        color = (255, 255, 255, opacity)
        
        # 对于PIL的RGBA模式
        if img.mode == 'RGBA':
            draw.ellipse((x, y, x+size, y+size), fill=color)
        else:
            # 对于RGB模式，忽略透明度
            draw.ellipse((x, y, x+size, y+size), fill=color[:3])
    
    # 减少模糊效果，使用更小的半径
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

def create_text_frame(text):
    """创建带有文字的单帧"""
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
    
    # 转换为NumPy数组，BGR格式 (OpenCV使用BGR)
    img_array = np.array(img)
    img_array = img_array[:, :, ::-1].copy()
    
    return img_array

def create_cover_frame():
    """创建视频封面，参考提供的图片风格但添加俏皮元素"""
    # 使用固定的粉色背景色 - 参考图片中的粉色
    background_color = (226, 187, 196)  # RGB格式的粉色
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), background_color)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        large_font = ImageFont.truetype("simhei.ttf", 90)
        medium_font = ImageFont.truetype("simhei.ttf", 80)
        small_font = ImageFont.truetype("simhei.ttf", 50)
    except:
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 绘制主标题 - 使用深红褐色，参考图片中的颜色
    title_color = (121, 57, 57)  # 深红褐色
    title = '恋爱"小考卷"'
    title_width = draw.textlength(title, font=large_font)
    title_y = VIDEO_HEIGHT * 0.4
    draw.text(((VIDEO_WIDTH - title_width) // 2, title_y), 
             title, font=large_font, fill=title_color)
    
    # 绘制副标题
    subtitle = "暂停就要回答"
    subtitle_width = draw.textlength(subtitle, font=large_font)
    subtitle_y = title_y + 120
    draw.text(((VIDEO_WIDTH - subtitle_width) // 2, subtitle_y), 
             subtitle, font=large_font, fill=title_color)
    
    # 绘制第三行文字
    third_line = "甜蜜真心话"
    third_line_width = draw.textlength(third_line, font=large_font)
    third_line_y = subtitle_y + 120
    draw.text(((VIDEO_WIDTH - third_line_width) // 2, third_line_y), 
             third_line, font=large_font, fill=title_color)
    
    # 绘制底部小字
    footer_text = "解锁Ta的小秘密 💕"
    footer_width = draw.textlength(footer_text, font=small_font)
    footer_y = VIDEO_HEIGHT - 150
    draw.text(((VIDEO_WIDTH - footer_width) // 2, footer_y), 
             footer_text, font=small_font, fill=title_color)
    
    # 添加俏皮元素 - 小爱心装饰
    heart_size = 40
    for i in range(6):
        angle = i * 60  # 每60度放置一个爱心，围成一个圆
        radius = 150  # 爱心围成的圆的半径
        center_x = VIDEO_WIDTH // 2
        center_y = (title_y + third_line_y) // 2  # 爱心围绕在标题区域周围
        
        # 根据角度计算位置
        x = center_x + int(radius * np.cos(np.radians(angle)))
        y = center_y + int(radius * np.sin(np.radians(angle)))
        
        # 绘制爱心
        draw_heart(draw, x, y, heart_size, title_color)
    
    # 添加顶部装饰元素 - 小皇冠
    crown_y = title_y - 130
    draw_crown(draw, VIDEO_WIDTH // 2, crown_y, 100, title_color)
    
    # 转换为NumPy数组，BGR格式
    img_array = np.array(img)
    img_array = img_array[:, :, ::-1].copy()
    
    return img_array

def draw_heart(draw, x, y, size, color):
    """绘制一个爱心形状"""
    # 爱心的上半部分是两个圆
    circle_radius = size // 3
    draw.ellipse((x - size//2, y - size//2, x - size//2 + size//1.5, y - size//2 + size//1.5), fill=color)
    draw.ellipse((x + size//6, y - size//2, x + size//6 + size//1.5, y - size//2 + size//1.5), fill=color)
    
    # 爱心的下半部分是一个三角形
    points = [
        (x - size//2, y - size//4),
        (x + size//2, y - size//4),
        (x, y + size//2)
    ]
    draw.polygon(points, fill=color)

def draw_crown(draw, x, y, size, color):
    """绘制一个简单的皇冠"""
    # 皇冠的基座
    base_points = [
        (x - size//2, y + size//4),
        (x + size//2, y + size//4),
        (x + size//2 - size//10, y),
        (x + size//4, y + size//8),
        (x, y - size//4),
        (x - size//4, y + size//8),
        (x - size//2 + size//10, y)
    ]
    draw.polygon(base_points, fill=color)
    
    # 皇冠上的小圆点
    circle_radius = size // 10
    draw.ellipse((x - size//4 - circle_radius, y - size//3 - circle_radius, 
                 x - size//4 + circle_radius, y - size//3 + circle_radius), fill=color)
    draw.ellipse((x - circle_radius, y - size//3 - circle_radius, 
                 x + circle_radius, y - size//3 + circle_radius), fill=color)
    draw.ellipse((x + size//4 - circle_radius, y - size//3 - circle_radius, 
                 x + size//4 + circle_radius, y - size//3 + circle_radius), fill=color)

def create_video():
    print("开始生成视频...")
    
    # 创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('couples_truth_questions_enhanced.mp4', fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
    
    # 添加封面
    cover_frame = create_cover_frame()
    cover_duration = COVER_DURATION * FPS  # 3秒
    
    print("添加视频封面...")
    for _ in range(cover_duration):
        out.write(cover_frame)
    
    # 计算一共需要多少帧
    question_frames = (DURATION - COVER_DURATION) * FPS
    frames_per_question = QUESTION_DURATION
    
    frame_count = 0
    question_index = 0
    
    print(f"开始生成问题画面，总共需要{question_frames}帧...")
    
    # 循环添加问题，直到达到所需的总帧数
    while frame_count < question_frames:
        if frame_count % 100 == 0:
            print(f"正在生成第{frame_count}/{question_frames}帧...")
        
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
    
    print(f"视频创建完成: couples_truth_questions_enhanced.mp4，共{cover_duration + frame_count}帧")

if __name__ == "__main__":
    start_time = time.time()
    create_video()
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f}秒") 