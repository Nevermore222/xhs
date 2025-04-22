try:
    import moviepy.editor as mpy
    print("MoviePy版本:", mpy.__version__)
    print("MoviePy可用!")
except ImportError as e:
    print("导入MoviePy时出错:", e)
    
try:
    from PIL import Image, ImageDraw, ImageFont
    print("PIL可用!")
except ImportError as e:
    print("导入PIL时出错:", e)
    
try:
    import numpy as np
    print("NumPy版本:", np.__version__)
    print("NumPy可用!")
except ImportError as e:
    print("导入NumPy时出错:", e) 