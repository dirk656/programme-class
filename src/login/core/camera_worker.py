# core/camera_worker.py

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from . import face_engine

from recognition.open_camera import open_camera

class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    recognize_result = pyqtSignal(str)
    register_done = pyqtSignal(str)

    def __init__(self, mode="checkin", name="", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.name = name
        self.running = False
        self.capture = None
        self.register_count = 0

    #摄像头运行函数
    def run(self):
        # 兼容原来的 capture 实例或重新打开
        if self.capture is None or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)
            
        self.running = True
        face_engine.load_data()

        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break

            self.frame_index += 1

            if self.mode == "checkin":
                if self.frame_index % self.recognize_interval == 0:
                    name = face_engine.recognize_single_frame(frame, draw_box=True)
                    if name and name != "Unknown":
                        self.recognize_result.emit(name)
                    
                self.frame_ready.emit(frame)

            elif self.mode == "register":
                if self.register_count < 1:
                    if self.frame_index % self.register_interval == 0:
                        if face_engine.save_face(self.name, frame):
                            self.register_count += 1

                self.frame_ready.emit(frame)

                if self.register_count >= 1:
                    self.register_done.emit(self.name)
                    break

        self.capture.release()
        self.capture = None

    def stop(self):
        self.running = False
