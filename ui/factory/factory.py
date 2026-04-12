# ====================== 皮肤切换开关 ======================
SKIN = "style2"

class UIFactory:

    @staticmethod
    def create_login_window():
        if SKIN == "style1":
            from ui.render.style1.login_render import LoginRender
        else:
            from ui.render.style2.login_render import LoginRender

        from ui.style1.ui_login import LoginWindow
        return LoginWindow(LoginRender)

    @staticmethod
    def create_main_window():
        if SKIN == "style1":
            from ui.render.style1.main_render import MainRender
        else:
            from ui.render.style2.main_render import MainRender

        from ui.style1.ui_main import FaceRecognitionCheckIn
        return FaceRecognitionCheckIn(MainRender)

    @staticmethod
    def create_student_window(username):
        if SKIN == "style1":
            from ui.render.style1.student_render import StudentRender
        else:
            from ui.render.style2.student_render import StudentRender

        from ui.style1.ui_students import StudentMainWindow
        return StudentMainWindow(username, StudentRender)

    # ===== 给 title_bar 用 =====
    @staticmethod
    def create_title_bar(title, parent):
        if SKIN == "style1":
            from ui.render.style1.title_render import CustomTitleRender
        else:
            from ui.render.style2.title_render import CustomTitleRender
        return CustomTitleRender(title, parent)