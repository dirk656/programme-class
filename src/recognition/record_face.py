from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import cv2

CASCADE_FILE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def record_face(
    person_name: str,
    save_root: Optional[Union[str, Path]] = None,
    max_samples: int = 3,
) -> int:
    """Record face images from webcam and save them to known_faces.

    Controls:
    - Press `s` to save current detected face
    - Press `q` to stop early
    """
    if not person_name.strip():
        return 0

    safe_name = person_name.strip().replace(" ", "_")

    if save_root is None:
        project_root = Path(__file__).resolve().parents[2]
        save_dir = project_root / "data" / "known_faces"
    else:
        save_dir = Path(save_root)

    save_dir.mkdir(parents=True, exist_ok=True)

    detector = cv2.CascadeClassifier(CASCADE_FILE)
    if detector.empty():
        print("Failed to load face detector")
        return 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return 0

    # 降低输入分辨率可提升实时性
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    saved = 0
    print("Record started. Press 's' to save, 'q' to quit.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame")
                break

            preview = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            boxes_small = detector.detectMultiScale(
                small_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40),
            )
            boxes = [(x * 2, y * 2, w * 2, h * 2) for (x, y, w, h) in boxes_small]

            largest = None
            if len(boxes) > 0:
                largest = max(boxes, key=lambda b: b[2] * b[3])
                x, y, w, h = largest
                cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 200, 0), 2)

            cv2.putText(
                preview,
                f"Saved: {saved}/{max_samples}  [s:save q:quit]",
                (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Face Record", preview)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s"):
                if largest is None:
                    print("No face detected in current frame")
                    continue

                x, y, w, h = largest
                face_img = frame[y : y + h, x : x + w]
                if face_img.size == 0:
                    continue

                out_path = save_dir / f"{safe_name}_{saved + 1}.jpg"
                cv2.imwrite(str(out_path), face_img)
                saved += 1
                print(f"Saved: {out_path}")

                if saved >= max_samples:
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return saved
