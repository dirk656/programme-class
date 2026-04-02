from manager.ui_manager import UIManager

class WindowManager:
    _instance = None

    def __new__(cls, app=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.app = app
            cls._instance.login_win = None
            cls._instance.main_win = None
        return cls._instance

    def show_login(self):
        self.close_all()
        self.login_win = UIManager().create_login()
        self.login_win.login_success.connect(self.show_main_by_role)
        self.login_win.show()

    def show_main_by_role(self, username, role):
        print(f"[DEBUG] 登录成功 → 用户：{username} 角色：{role}")

        # 1. 先关登录窗口（必须第一步）
        if self.login_win:
            self.login_win.close()
            self.login_win.deleteLater()
            self.login_win = None

        # 2. 创建主窗口
        if role == "teacher":
            self.main_win = UIManager().create_main()
        else:
            self.main_win = UIManager().create_student(username)

        # 3. ✨ 强制显示 + 激活（这是你缺失的关键）
        self.main_win.show()
        self.main_win.raise_()
        self.main_win.activateWindow()

        # 4. ✨ 强制刷新界面（防止界面卡住不绘制）
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