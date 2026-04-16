# manager/ui_manager.py
from src.login.ui.factory.factory import UIFactory

class UIManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    # 统一创建
    def create_login(self):
        return UIFactory.create_login_window()

    def create_main(self):
        return UIFactory.create_main_window()

    def create_student(self, username):
        return UIFactory.create_student_window(username)

    # 统一显示
    def show(self, window):
        window.show()