# core/face_engine.py
import cv2
import face_recognition
import numpy as np
from pathlib import Path

# 人脸库路径
USER_FACE_DIR = Path(__file__).resolve().parents[3] / "data" / "known_faces"
USER_FACE_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_EXTS = {".jpg", ".png", ".jpeg"}

# 全局缓存
known_face_encodings = []
known_face_names = []
_faces_loaded = False


def _append_face_encoding(img_path: Path, username: str) -> None:
    """Encode one image and append to in-memory cache."""
    try:
        image = face_recognition.load_image_file(str(img_path))
        face_enc = face_recognition.face_encodings(image)
        if face_enc:
            known_face_encodings.append(face_enc[0])
            known_face_names.append(username)
    except Exception as e:
        print(f"加载失败 {img_path}: {e}")

def load_all_faces(force_reload=False):
    """加载所有已注册的人脸"""
    global known_face_encodings, known_face_names, _faces_loaded
    if _faces_loaded and not force_reload:
        return

    known_face_encodings.clear()
    known_face_names.clear()

    for entry in USER_FACE_DIR.iterdir():
        if entry.is_dir():
            username = entry.name
            image_paths = [p for p in entry.iterdir() if p.suffix.lower() in IMAGE_EXTS]
        elif entry.is_file() and entry.suffix.lower() in IMAGE_EXTS:
            # 扁平文件命名示例: username_1.jpg
            username = entry.stem.rsplit("_", 1)[0]
            image_paths = [entry]
        else:
            continue

        for img_path in image_paths:
            _append_face_encoding(img_path, username)

    _faces_loaded = True

def recognize_face(frame):
    """识别人脸，返回名字或 None"""
    if not known_face_encodings:
        return None

    # 降采样可显著提升实时识别速度
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for enc in face_encodings:
        distances = face_recognition.face_distance(known_face_encodings, enc)
        if len(distances) == 0:
            continue
        idx = int(np.argmin(distances))
        if distances[idx] <= 0.48:
            return known_face_names[idx]
    return None

def save_face(username, frame):
    """保存人脸到 known_faces 根目录"""
    path = USER_FACE_DIR / f"{username}_{np.random.randint(1000)}.jpg"
    cv2.imwrite(str(path), frame)
    _append_face_encoding(path, username)
    return True