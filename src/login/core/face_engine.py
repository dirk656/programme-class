# core/face_engine.py
import cv2
import face_recognition
import numpy as np
import os

# 人脸库路径
USER_FACE_DIR = "img_user"
if not os.path.exists(USER_FACE_DIR):
    os.makedirs(USER_FACE_DIR)

# 全局缓存
known_face_encodings = []
known_face_names = []

def load_all_faces():
    """加载所有已注册的人脸"""
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()

    for username in os.listdir(USER_FACE_DIR):
        user_dir = os.path.join(USER_FACE_DIR, username)
        if not os.path.isdir(user_dir):
            continue

        for img_name in os.listdir(user_dir):
            if img_name.endswith((".jpg", ".png")):
                img_path = os.path.join(user_dir, img_name)#再次拼接路径
                try:
                    image = face_recognition.load_image_file(img_path)#通过路径读取人脸数据
                    face_enc = face_recognition.face_encodings(image)#将人脸数据转化为数组
                    if face_enc:
                        known_face_encodings.append(face_enc[0])#录入保存
                        known_face_names.append(username)
                except Exception as e:
                    print(f"数据加载失败 {img_path}: {e}")

def recognize_face(frame):
    """识别人脸，返回名字或 None"""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for enc in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, enc)
        if True in matches:
            idx = matches.index(True)
            return known_face_names[idx]
    return None

def save_face(username, frame):
    """保存人脸到用户目录"""
    user_dir = os.path.join(USER_FACE_DIR, username)#拼接
    if not os.path.exists(user_dir):#没有就创建
        os.makedirs(user_dir)

    path = os.path.join(user_dir, f"face_{np.random.randint(1000)}.jpg")
    cv2.imwrite(path, frame)#写入人脸数据
    load_all_faces()
    return True