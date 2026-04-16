
import os
import sys
from pathlib import Path
from typing import List, Tuple

import cv2
import face_recognition
import numpy as np


FACES_DATA_DIR = Path("data/known_faces")
TOLERANCE = 0.6 #置信度
FRAME_SCALE = 0.25 #放缩比例

# 加载人脸数据
def load_faces_data(faces_dir:Path) -> Tuple[List[np.ndarray], List[str]]:
    encodings: List[np.ndarray] = []
    names: List[str] = []

    if not faces_dir.exists() or not faces_dir.is_dir():
        print(f"警告：找不到目录 {faces_dir}")
        return encodings, names

    for image_path in faces_dir.glob("*"):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp"}:
            continue

        try:
            image = face_recognition.load_image_file(str(image_path))
            face_encs = face_recognition.face_encodings(image)
            
            if face_encs:
                encodings.append(face_encs[0])
                # 兼容带序号的文件名（比如: admin_1.jpg -> admin）
                base_name = image_path.stem.rsplit("_", 1)[0]
                names.append(base_name)
        except Exception as e:
            print(f"加载图片失败 {image_path}: {e}")

    return encodings, names


   