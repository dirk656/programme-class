# core/face_engine.py
import cv2
import face_recognition
import numpy as np
import sys
from pathlib import Path

# 把 src 目录加进环境变量以便能引到 recognition 包
sys.path.append(str(Path(__file__).resolve().parents[2]))

from recognition.load_faces_data import load_faces_data

# 人脸库路径
USER_FACE_DIR = "img_user"
if not os.path.exists(USER_FACE_DIR):
    os.makedirs(USER_FACE_DIR)

known_encodings = []
known_names = []
_faces_loaded = False

def load_data():
    """包装 load_faces_data，实现数据缓存避免重复加载"""
    global known_encodings, known_names, _faces_loaded
    if _faces_loaded:
        return
    
    encodings, names = load_faces_data(USER_FACE_DIR)
    known_encodings.clear()
    known_encodings.extend(encodings)
    known_names.clear()
    known_names.extend(names)
    _faces_loaded = True

def recognize_single_frame(frame, draw_box=True):
    """适配单帧画面的人脸匹配 (代替原 camera_face_match 的死循环模式)"""
    if not known_encodings:
        return None

    # 用缩小图片的方式加快识别速度
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    detected_name = None

    for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
        name = "Unknown"
        score_text = "N/A"
        
        distances = face_recognition.face_distance(known_encodings, face_enc)
        if len(distances) > 0:
            best_idx = int(np.argmin(distances))
            score_text = f"{distances[best_idx]:.3f}"
            if distances[best_idx] <= 0.6:  # 常规容差值
                name = known_names[best_idx]
                # 记录找到的最优名字返回
                if detected_name is None or name != "Unknown":
                    detected_name = name

        if draw_box:
            # 还原缩放比例，绘制在原帧上
            top = int(top / 0.25)
            right = int(right / 0.25)
            bottom = int(bottom / 0.25)
            left = int(left / 0.25)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 200, 0), 2)
            cv2.rectangle(frame, (left, bottom - 28), (right, bottom), (0, 200, 0), cv2.FILLED)
            cv2.putText(
                frame,
                f"{name} {score_text}",
                (left + 6, bottom - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
            )

    return detected_name

def save_face(username, frame):
    """保存人脸到 known_faces 根目录并更新缓存"""
    path = USER_FACE_DIR / f"{username}.jpg"
    cv2.imwrite(str(path), frame)
    
    # 获取新图片的编码并追加到缓存
    image = face_recognition.load_image_file(str(path))
    face_enc = face_recognition.face_encodings(image)
    if face_enc:
        known_encodings.append(face_enc[0])
        known_names.append(username)
    return True
