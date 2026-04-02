# config/settings.py
import os

# 路径配置
FACE_DATA_PATH = "face_data.pkl"  # 人脸数据保存路径
ICON_PATH = os.path.normpath(r"D:\Users\ysr\Desktop\PyUIProjects\a4y2a-oo7kx.ico")  # 图标路径

# 样式常量
WINDOW_ROUND_RADIUS = 12  # 窗口圆角
BUTTON_ROUND_RADIUS = 15  # 按钮圆角
TITLE_BAR_HEIGHT = 70     # 标题栏高度
EDGE_MARGIN = 8           # 窗口拉伸边距
MIN_WINDOW_WIDTH = 800    # 窗口最小宽度
MIN_WINDOW_HEIGHT = 600   # 窗口最小高度

# 摄像头配置
CAMERA_ID = 0             # 默认摄像头ID
MAX_REGISTER_COUNT = 3    # 人脸录入最大次数

# 样式颜色
COLOR_PRIMARY = "#00d2be"
COLOR_PRIMARY_LIGHT = "#00f0e0"
COLOR_SECONDARY = "#3a7bd5"
COLOR_BACKGROUND = "#202020"
COLOR_TEXT_WHITE = "#ffffff"
COLOR_TEXT_GRAY = "#e0e0e0"

# 字体配置
FONT_MAIN = "Microsoft YaHei UI"
FONT_SIZE_NORMAL = 14
FONT_SIZE_TITLE = 18
FONT_SIZE_BUTTON = 14

