# core/camera_worker.py

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from . import face_engine

class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    recognize_result = pyqtSignal(str)
    register_done = pyqtSignal(str)
    register_duplicate = pyqtSignal(str)

    def __init__(self, mode="checkin", name="", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.name = name
        self.running = False
        self.capture = None
        self.register_count = 0
        self.frame_index = 0
        self.recognize_interval = 3
        self.register_interval = 10

    
    def run(self):
   
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
                    name = face_engine.recognize_single_frame(frame, draw_box=False)
                    if name and name != "Unknown":
                        self.recognize_result.emit(name)
                    
                self.frame_ready.emit(frame)

            elif self.mode == "register":
                if self.register_count < 1:
                    if self.frame_index % self.register_interval == 0:
                        # 录入前先与已有人脸库比对，命中则阻止重复录入
                        duplicated_name = face_engine.recognize_single_frame(frame, draw_box=False)
                        if duplicated_name and duplicated_name != "Unknown":
                            self.register_duplicate.emit(duplicated_name)
                            break

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
