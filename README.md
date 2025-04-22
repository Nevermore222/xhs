# 情侣真心话视频生成器

这个项目可以生成一个高质量的情侣真心话游戏视频，类似于抽奖视频快速切换的效果，用户可以随时暂停视频，根据停下时显示的问题进行回答。

## 功能特点

- 快速切换的问题文本，模拟抽奖效果
- 精美的渐变背景和视觉设计
- 自定义问题库
- 可调整视频长度和问题切换速度
- 高清竖屏视频输出 (1080x1920)
- 包含使用说明的开场介绍

## 使用方法

### 环境要求

需要安装以下Python库：
```
pip install opencv-python pillow numpy
```

### 基础版本

运行 `create_video_basic.py` 生成基础版本的视频：

```
python create_video_basic.py
```

### 增强版本

运行 `create_video_enhanced_cv.py` 生成带有更多视觉效果的增强版本：

```
python create_video_enhanced_cv.py
```

生成的视频会保存在当前目录下，文件名为 `couples_truth_questions_basic.mp4` 或 `couples_truth_questions_enhanced.mp4`。

## 自定义选项

可以通过修改脚本中的以下变量来自定义视频：

- `questions`: 修改问题库中的问题
- `DURATION`: 调整视频总时长（秒）
- `QUESTION_DURATION`: 每个问题显示的时间（帧数），数值越小切换越快
- `VIDEO_WIDTH` 和 `VIDEO_HEIGHT`: 调整视频尺寸
- `GRADIENT_COLORS`: 修改背景渐变颜色（仅增强版）

## 玩法说明

1. 播放视频
2. 随时暂停视频
3. 根据暂停时显示的问题，情侣双方轮流回答
4. 继续播放，再次随机暂停
5. 真诚回答每个问题，增进彼此了解

## 注意事项

- 视频生成可能需要一定时间，取决于视频长度和电脑性能
- 增强版本生成时间较长，因为每帧都有渐变和装饰效果
- 确保系统上安装了中文字体（默认使用"simhei.ttf"）

## 实现技术

该项目使用了OpenCV和PIL库来生成视频，主要功能包括：

1. 创建渐变背景
2. 添加装饰性视觉元素
3. 使用PIL渲染中文文本
4. 使用OpenCV生成MP4视频

## 问题排查

如果遇到无法导入库的问题，请确保正确安装了所需依赖：

```
pip install opencv-python pillow numpy
```

如果遇到中文显示问题，请确保系统中安装了中文字体，或修改脚本中的字体设置。 