import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.login.manager.window_manager import WindowManager

if __name__ == "__main__":
    # 关闭高DPI缩放 → 解决界面突然变大的问题！
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)

    app = QApplication(sys.argv)

    # 全局窗口管理器
    wm = WindowManager(app)
    wm.show_login()

    sys.exit(app.exec_())