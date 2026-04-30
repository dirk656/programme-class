# ====================== 皮肤切换开关 ======================
from PyQt5.QtCore import QObject, pyqtSignal

# 全局皮肤信号：点击切换后，通知所有窗口关闭
class SkinSignal(QObject):
    toggle = pyqtSignal()

skin_signal = SkinSignal()
SKIN = "style1"  # 默认皮肤


class UIFactory:

    @staticmethod
    def get_skin():
        global SKIN
        return SKIN

    @staticmethod
    def toggle_skin():
        global SKIN
        # 切换：style1 ↔ style2
        SKIN = "style2" if SKIN == "style1" else "style1"
        # 发送信号 → 所有窗口关闭
        skin_signal.toggle.emit()

    # ------------------- 下面你原来的代码完全不动 -------------------
    @staticmethod
    def create_login_window():
        if SKIN == "style1":
            from src.login.ui.render.style1.login_render import LoginRender
        else:
            from src.login.ui.render.style2.login_render import LoginRender

        from src.login.ui.style1.ui_login import LoginWindow
        return LoginWindow(LoginRender)

    @staticmethod
    def create_main_window():
        if SKIN == "style1":
            from src.login.ui.render.style1.main_render import MainRender
        else:
            from src.login.ui.render.style2.main_render import MainRender

        from src.login.ui.style1.ui_main import FaceRecognitionCheckIn
        return FaceRecognitionCheckIn(MainRender)

    @staticmethod
    def create_student_window(username):
        if SKIN == "style1":
            from src.login.ui.render.style1.student_render import StudentRender
        else:
            from src.login.ui.render.style2.student_render import StudentRender

        from src.login.ui.style1.ui_students import StudentMainWindow
        return StudentMainWindow(username, StudentRender)

    # ===== 给 title_bar 用 =====
    @staticmethod
    def create_title_bar(title, parent):
        if SKIN == "style1":
            from src.login.ui.render.style1.title_render import CustomTitleRender
        else:
            from src.login.ui.render.style2.title_render import CustomTitleRender
        return CustomTitleRender(title, parent)