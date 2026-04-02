# ui/factory/factory.py
from ui.base.base_windows import BaseLoginWindow, BaseMainWindow, BaseStudentWindow

# 👇 这个类必须存在！！！
class UIFactory:
    @staticmethod
    def create_login_window() -> BaseLoginWindow:
        from ui.style1.ui_login import LoginWindow
        return LoginWindow()

    @staticmethod
    def create_main_window() -> BaseMainWindow:
        from ui.style1.ui_main import FaceRecognitionCheckIn
        return FaceRecognitionCheckIn()

    @staticmethod
    def create_student_window(username) -> BaseStudentWindow:
        from ui.style1.ui_students import StudentMainWindow
        return StudentMainWindow(username)