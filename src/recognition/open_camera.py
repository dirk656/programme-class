import sys
import cv2


def open_camera() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        sys.exit(1)
    
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame from camera")
                break

            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()





