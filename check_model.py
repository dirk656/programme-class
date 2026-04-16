import sys
print("Python 路径:", sys.executable) # 确认当前运行的是哪个 Python

try:
    import face_recognition_models
    print("face_recognition_models 版本:", face_recognition_models.__version__)
except ImportError as e:
    print("导入 models 失败:", e)

try:
    import face_recognition
    print("face_recognition 导入成功")
except ImportError as e:
    print("导入 face_recognition 失败:", e)