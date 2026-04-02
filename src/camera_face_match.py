"""Realtime camera face matching script.

This script does not modify any existing project files.
It loads known faces from data/known_faces and matches faces from webcam.

Usage:
    python src/camera_face_match.py

Press 'q' to quit.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

import cv2
import face_recognition
import numpy as np

KNOWN_DIR = Path("data/known_faces")
FRAME_SCALE = 0.25
TOLERANCE = 0.5
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def load_known_faces(known_dir: Path) -> Tuple[List[np.ndarray], List[str]]:
    """Load known face encodings and names from image files."""
    encodings: List[np.ndarray] = []
    names: List[str] = []

    if not known_dir.exists() or not known_dir.is_dir():
        return encodings, names

    for image_path in sorted(known_dir.glob("*")):
        if image_path.suffix.lower() not in SUPPORTED_EXTS:
            continue

        image = face_recognition.load_image_file(str(image_path))
        face_encs = face_recognition.face_encodings(image)
        if not face_encs:
            continue

        # Use the first detected face in each known image.
        encodings.append(face_encs[0])
        names.append(image_path.stem)

    return encodings, names


def camera_face_match() -> None:
    known_encodings, known_names = load_known_faces(KNOWN_DIR)
    if not known_encodings:
        print(f"No known faces loaded from: {KNOWN_DIR}")
        print("Add files like: data/known_faces/Alice.jpg")
        sys.exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        sys.exit(1)

    print("Face matching started. Press 'q' to quit.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame from camera")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=FRAME_SCALE, fy=FRAME_SCALE)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
                name = "Unknown"
                score_text = "N/A"

                distances = face_recognition.face_distance(known_encodings, face_enc)
                if len(distances) > 0:
                    best_idx = int(np.argmin(distances))
                    score_text = f"{distances[best_idx]:.3f}"
                    if distances[best_idx] <= TOLERANCE:
                        name = known_names[best_idx]

                # Scale face coordinates back to original frame size.
                top = int(top / FRAME_SCALE)
                right = int(right / FRAME_SCALE)
                bottom = int(bottom / FRAME_SCALE)
                left = int(left / FRAME_SCALE)

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

            cv2.imshow("Camera Face Match", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera_face_match()
