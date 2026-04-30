from src.login.manager.ui_manager import UIManager
from src.login.ui.factory.factory import skin_signal

class WindowManager:
    _instance = None

    def __new__(cls, app=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.app = app
            cls._instance.login_win = None
            cls._instance.main_win = None
            # 绑定皮肤切换信号：切皮肤就回到登录页
            skin_signal.toggle.connect(cls._instance.show_login)
        return cls._instance

    def show_login(self):
        self.close_all()
        self.login_win = UIManager().create_login()
        self.login_win.login_success.connect(self.show_main_by_role)
        self.login_win.show()

    def show_main_by_role(self, username, role):
        print(f"[DEBUG] 登录成功 → 用户：{username} 角色：{role}")

        # 1. 先关登录窗口
        if self.login_win:
            self.login_win.close()
            self.login_win.deleteLater()
            self.login_win = None

        # 2. 创建主窗口
        if role == "teacher":
            self.main_win = UIManager().create_main()
        else:
            self.main_win = UIManager().create_student(username)

        # 3. 强制显示激活
        self.main_win.show()
        self.main_win.raise_()
        self.main_win.activateWindow()

        # 4. 强制刷新界面
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()

    def close_all(self):
        try:
            if self.main_win:
                self.main_win.clean()
                self.main_win.close()
                self.main_win.deleteLater()
                self.main_win = None
        except:
            pass

        try:
            if self.login_win:
                self.login_win.close()
                self.login_win = None
        except:
            pass