from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from config.settings import ICON_PATH
from ui.base.base_windows import BaseLoginWindow
from core.auth_manager import AuthManager
from ui.render.login_render import LoginRender

class LoginWindow(QMainWindow, BaseLoginWindow):
    login_success = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._init_base_config()
        self.render = LoginRender(self)
        self.render.build()
        self.render.bind_events(
            self.on_login_click,
            self.on_reset_click,
            self.open_register_window
        )

    def _init_base_config(self):
        self.setWindowTitle("登录")
        self.setGeometry(600, 250, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(ICON_PATH))

    def on_login_click(self):
        username = self.render.username_input.text().strip()
        password = self.render.password_input.text().strip()
        success, msg, role = AuthManager.validate_login(username, password)

        if success:
            QMessageBox.information(None, "成功", msg)
            self.login_success.emit(username, role)  # 只发信号，不关窗口！
        else:
            QMessageBox.warning(self, "失败", msg)

    def on_reset_click(self):
        self.render.username_input.clear()
        self.render.password_input.clear()

    def open_register_window(self):
        from ui.style1.register_window import RegisterWindow
        self.reg_win = RegisterWindow()
        self.reg_win.show()