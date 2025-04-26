import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import time
import random
import shutil

# 确保输出文件夹存在
output_dir = "output_videos"
os.makedirs(output_dir, exist_ok=True)

# 不同尺度等级的问题库
question_levels = {
    1: [  # 适合初次见面的情侣，非常轻松
        "你最喜欢我哪个笑容？",
        "第一次见面时你穿什么衣服还记得吗？",
        "你平时起床第一件事是什么？",
        "你最喜欢的电影类型是什么？",
        "如果只能选一种零食吃一年，你会选什么？",
        "你最喜欢的颜色是什么？",
        "我做的哪道菜是你最喜欢的？",
        "上一次开怀大笑是因为什么？",
        "如果让你去旅行，最想去哪个城市？",
        "周末你最喜欢做的事情是什么？"
    ],
    2: [  # 轻松互动问题
        "你心中我最可爱的瞬间是什么时候？",
        "如果我们互换一天身份，你最想体验什么？",
        "看到我第一面时，你觉得我是什么样的人？",
        "我有哪些让你印象深刻的小习惯？",
        "我做过什么事情让你特别感动？",
        "我们第一次牵手是在哪里？",
        "你认为我们之间最默契的时刻是什么时候？",
        "你会偷偷保存我的什么照片？",
        "你希望我们的约会方式有什么变化？",
        "如果明天是最后一天，你最想和我做什么？"
    ],
    3: [  # 有趣的了解问题
        "我有哪些口头禅是你觉得很有趣的？",
        "你觉得我们之间最大的共同点是什么？",
        "我们在一起后，你改变了哪些生活习惯？",
        "我做过最让你哭笑不得的事情是什么？",
        "你最欣赏我身上的哪个优点？",
        "我有哪些行为是你一直想让我改的？",
        "我们在一起后，你最大的收获是什么？",
        "在你心里，我们的关系目前处于哪个阶段？",
        "我说过的话中，哪句话让你记忆最深刻？",
        "如果可以和我一起实现一个愿望，你会选择什么？"
    ],
    4: [  # 稍微深入的问题
        "你觉得我们之间最需要改进的是什么？",
        "你有没有因为我而改变一些重要决定？",
        "我们在一起后，你有没有感到失去了什么？",
        "你最欣赏我的家人的哪一点？",
        "我们吵架后，你通常会怎么想？",
        "你愿意为我牺牲哪些个人爱好？",
        "你最希望我能理解你的哪一部分？",
        "有没有一个瞬间，你突然感到很爱我？",
        "在你心中，我有哪些地方比不上你的前任？",
        "我的哪些行为会让你感到不安全？"
    ],
    5: [  # 中等深度问题
        "你曾经为我放弃过什么重要的事情吗？",
        "我哪些行为会让你觉得很受伤？",
        "你觉得我在感情中最大的缺点是什么？",
        "我们之间有没有什么问题你一直不敢提？",
        "你有没有因为我做过的事情而失望过？",
        "你觉得我对待我们的关系够认真吗？",
        "你会介意我和异性朋友单独出去吗？",
        "我们在一起后，你有没有怀疑过这段关系？",
        "你会为了我改变自己的人生规划吗？",
        "如果有一天我们结束了，你认为最可能的原因是什么？"
    ],
    6: [  # 深入关系问题
        "你和前任分手的真正原因是什么？",
        "如果我的事业需要长期异地，你会怎么做？",
        "你觉得我们之间最大的阻碍是什么？",
        "你有没有试过在我们相处时隐藏真实的自己？",
        "你曾经对我说过谎吗？关于什么事情？",
        "我做过什么让你瞬间想要分手的事情？",
        "你有没有过和我在一起但想念前任的时刻？",
        "你觉得我的家人对你的印象如何？",
        "如果我们分手，你会怎么处理我们共同的朋友圈？",
        "你有没有因为我而改变了一些重要的价值观？"
    ],
    7: [  # 挑战性问题
        "你有没有偷偷删除过我们的聊天记录？",
        "你有没有觉得我的某个朋友对你有好感？",
        "你觉得我最大的缺点是什么？",
        "在我不在的时候，你会偷偷做什么？",
        "如果让你选择和我的一个朋友约会，你会选谁？",
        "你有没有瞒着我偷偷联系过异性？",
        "你有没有怀疑过我对你不忠？",
        "我做过最让你伤心的事情是什么？",
        "你会为了我放弃你的梦想吗？",
        "你有没有想过和我分手？"
    ],
    8: [  # 高度挑战性问题
        "你最后一次说谎是什么时候？关于什么？",
        "你在和我交往的同时有没有被别人吸引过？",
        "你有没有故意隐瞒我一些重要信息？",
        "你最害怕我发现你的什么秘密？",
        "你的前任在哪方面比我强？",
        "我的哪些行为会让你特别反感？",
        "如果我发胖20斤，你还会和我在一起吗？",
        "你觉得我父母有什么让你特别不舒服的地方？",
        "你有没有因为与我在一起而后悔过？",
        "如果我事业一直不成功，你会一直支持我吗？"
    ],
    9: [  # 极具挑战性问题
        "如果让你在我和事业中做选择，你会选择什么？",
        "在我们关系中，你有没有做过对不起我的事？",
        "你最隐秘的性幻想是什么？",
        "你有没有拿我和你的前任做过比较？",
        "如果我提出分手，你心里真实的反应会是什么？",
        "你有没有因为我的某些行为而恨过我？",
        "你觉得我们的亲密关系让你满意吗？",
        "你有没有不喜欢但又不敢告诉我的身体部位？",
        "如果我变得特别成功，你会担心我变心吗？",
        "如果我们注定要分开，你现在想对我说什么？"
    ],
    10: [  # 极限挑战问题，高度私密
        "你会为了我放弃你的家人吗？",
        "我们之间有什么事情是你绝对无法接受的？",
        "你有没有过出轨的念头？",
        "你有没有觉得我在亲密关系中表现不够好？",
        "如果你可以改变我的一个身体部位，会是哪里？",
        "你有过和我在一起但想念别人的时刻吗？",
        "你觉得我们的关系能维持多久？",
        "如果我突然变得一无所有，你会离开我吗？",
        "你有多少事情是永远不会告诉我的？",
        "为了能和我在一起，你的底线是什么？"
    ]
}

# 视频参数
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 70
FONT_COLOR = (255, 255, 255)
TITLE_FONT_SIZE = 45
DURATION = 30  # 视频总时长(秒)
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

def create_text_frame(text, level):
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
    title = f"情侣真心话 - 等级 {level}"
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

def create_cover_frame(level):
    """创建视频封面，根据不同等级设置不同的标题"""
    # 使用固定的粉色背景色
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
    
    # 设置颜色
    title_color = (121, 57, 57)  # 深红褐色
    
    # 根据不同等级设置不同的标题
    level_titles = {
        1: '恋爱小白卷',
        2: '初级真心话',
        3: '温和互动版',
        4: '进阶小考验',
        5: '恋爱中级卷',
        6: '深度交流版',
        7: '高阶挑战卷',
        8: '火辣大考验',
        9: '情侣极限版',
        10: '灵魂拷问卷'
    }
    
    # 绘制主标题
    title = f'恋爱"测试卷"'
    title_width = draw.textlength(title, font=large_font)
    title_y = VIDEO_HEIGHT * 0.35
    draw.text(((VIDEO_WIDTH - title_width) // 2, title_y), 
             title, font=large_font, fill=title_color)
    
    # 绘制副标题
    subtitle = level_titles[level]
    subtitle_width = draw.textlength(subtitle, font=large_font)
    subtitle_y = title_y + 120
    draw.text(((VIDEO_WIDTH - subtitle_width) // 2, subtitle_y), 
             subtitle, font=large_font, fill=title_color)
    
    # 绘制第三行文字
    third_line = f"难度等级: {level}/10"
    third_line_width = draw.textlength(third_line, font=medium_font)
    third_line_y = subtitle_y + 130
    draw.text(((VIDEO_WIDTH - third_line_width) // 2, third_line_y), 
             third_line, font=medium_font, fill=title_color)
    
    # 绘制底部小字
    footer_text = "真心话大挑战 💓"
    footer_width = draw.textlength(footer_text, font=small_font)
    footer_y = VIDEO_HEIGHT - 150
    draw.text(((VIDEO_WIDTH - footer_width) // 2, footer_y), 
             footer_text, font=small_font, fill=title_color)
    
    # 添加装饰元素
    draw_heart(draw, VIDEO_WIDTH // 2, footer_y - 70, 60, title_color)
    
    # 添加爱心装饰
    heart_size = 40
    for i in range(5):
        angle = i * 72  # 每72度放置一个爱心，围成一个圆
        radius = 130  # 爱心围成的圆的半径
        center_x = VIDEO_WIDTH // 2
        center_y = (title_y + third_line_y) // 2  # 爱心围绕在标题区域周围
        
        # 根据角度计算位置
        x = center_x + int(radius * np.cos(np.radians(angle)))
        y = center_y + int(radius * np.sin(np.radians(angle)))
        
        # 绘制爱心
        draw_heart(draw, x, y, heart_size, title_color)
    
    # 添加等级指示器
    draw_level_indicator(draw, level, VIDEO_WIDTH // 2, third_line_y + 100, title_color)
    
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

def draw_level_indicator(draw, level, x, y, color):
    """绘制等级指示器"""
    # 绘制10个圆点，当前等级以前的填充，之后的空心
    radius = 10
    spacing = 25
    start_x = x - (spacing * 9) // 2
    
    for i in range(1, 11):
        cx = start_x + (i-1) * spacing
        if i <= level:
            # 填充圆点
            draw.ellipse((cx-radius, y-radius, cx+radius, y+radius), fill=color)
        else:
            # 空心圆点
            draw.ellipse((cx-radius, y-radius, cx+radius, y+radius), outline=color, width=2)

def create_video(level, questions):
    """为特定等级创建视频"""
    output_file = os.path.join(output_dir, f"couples_truth_level_{level}.mp4")
    print(f"开始生成等级 {level} 的视频...")
    
    # 创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
    
    # 添加封面
    cover_frame = create_cover_frame(level)
    cover_duration = COVER_DURATION * FPS  # 3秒
    
    print(f"添加视频封面...")
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
        frame = create_text_frame(current_question, level)
        
        # 写入帧
        out.write(frame)
        
        # 更新计数器
        frame_count += 1
        
        # 每隔几帧更换问题
        if frame_count % frames_per_question == 0:
            question_index += 1
    
    # 释放VideoWriter
    out.release()
    
    print(f"视频创建完成: {output_file}，共{cover_duration + frame_count}帧")
    return output_file

def generate_all_videos():
    """生成所有不同等级的视频"""
    start_time = time.time()
    
    created_files = []
    for level in range(1, 11):
        level_questions = question_levels[level]
        output_file = create_video(level, level_questions)
        created_files.append(output_file)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n所有视频生成完成！总耗时: {total_time:.2f}秒")
    print(f"生成的视频文件:")
    for file in created_files:
        print(f" - {file}")

if __name__ == "__main__":
    generate_all_videos() 