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
USER_FACE_DIR = Path(__file__).resolve().parents[3] / "data" / "known_faces"
USER_FACE_DIR.mkdir(parents=True, exist_ok=True)

known_encodings = []
known_names = []
_faces_loaded = False

def _normalize_face_image(frame):
    """把任意摄像头帧规范成 face_recognition 可接受的 8bit RGB/gray。"""
    if frame is None:
        return None

    frame = np.asarray(frame)
    if frame.size == 0:
        return None

    if frame.dtype != np.uint8:
        # 常见浮点帧是 0~1 区间，先放大到 0~255 再转 uint8。
        if np.issubdtype(frame.dtype, np.floating):
            if frame.max(initial=0) <= 1.0:
                frame = frame * 255.0
        frame = np.clip(frame, 0, 255).astype(np.uint8)

    if frame.ndim == 2:
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            return None
        return np.require(frame, dtype=np.uint8, requirements=["C_CONTIGUOUS"])

    if frame.ndim != 3:
        return None

    if frame.shape[0] == 0 or frame.shape[1] == 0:
        return None

    channels = frame.shape[2]
    if channels == 3:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    elif channels == 4:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
    elif channels == 1:
        rgb = frame[:, :, 0]
    else:
        return None

    return np.require(rgb, dtype=np.uint8, requirements=["C_CONTIGUOUS"])

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
    face_input = _normalize_face_image(small_frame)
    if face_input is None:
        return None

    face_locations = face_recognition.face_locations(face_input)
    face_encodings = face_recognition.face_encodings(face_input, face_locations)

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
    face_image = _normalize_face_image(frame)
    if face_image is None:
        shape = getattr(frame, "shape", None)
        dtype = getattr(frame, "dtype", None)
        print(f"人脸图像无效 {username}: shape={shape}, dtype={dtype}")
        return False

    # 保存时统一写成 BGR 三通道，避免部分后端生成异常格式文件。
    save_image = face_image
    if face_image.ndim == 3:
        save_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)

    if not cv2.imwrite(str(path), save_image):
        return False

    try:
        face_enc = face_recognition.face_encodings(face_image)
    except RuntimeError as e:
        channels = 1 if face_image.ndim == 2 else face_image.shape[2]
        print(
            f"人脸编码失败 {username}: {e}; "
            f"shape={face_image.shape}, dtype={face_image.dtype}, channels={channels}"
        )
        return False

    if not face_enc:
        return False

    known_encodings.append(face_enc[0])
    known_names.append(username)
    return True
