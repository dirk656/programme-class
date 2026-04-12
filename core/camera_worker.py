# core/camera_worker.py

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from . import face_engine

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
        self.running = True
        self.capture = cv2.VideoCapture(0) #调用默认摄像头对象
        #打开失败
        if not self.capture.isOpened():
            print("❌ 摄像头打开失败")
            self.running = False
            return

        face_engine.load_all_faces()

        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break

            self.frame_ready.emit(frame)

            if self.mode == "checkin":
                name = face_engine.recognize_face(frame)
                if name:
                    self.recognize_result.emit(name)

            elif self.mode == "register":
                if self.register_count < 3:
                    if face_engine.save_face(self.name, frame):
                        self.register_count += 1

                if self.register_count >= 3:
                    self.register_done.emit(self.name)
                    break

        self.capture.release()
        self.capture = None

    def stop(self):
        self.running = False
