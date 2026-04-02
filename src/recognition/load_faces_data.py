
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
    encodings= List[np.ndarray] = []
    names = List[str] = []

    if not faces_dir.exists():
        sys.exit(1)

    else:
        images = face_recognition.load_image_file(str(faces_dir))
        face_encodings = face_recognition.face_encodings(images)

        if not face_encodings:
            sys.exit(1)

        encodings.append(face_encodings[0])
        names.append(faces_dir.stem)

        return encodings , names


   