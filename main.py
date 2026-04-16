#main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from manager.window_manager import WindowManager

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    # 全局窗口管理器
    wm = WindowManager(app)
    wm.show_login()

    sys.exit(app.exec_())

