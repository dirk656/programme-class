from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from src.login.ui.factory.factory import UIFactory, skin_signal

class CustomTitleBar(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        
        self.render = UIFactory.create_title_bar(title, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.render)

        self.logout_label = self.render.logout_label
        self.min_label = self.render.min_label
        self.max_label = self.render.max_label
        self.close_label = self.render.close_label
        self.skin_btn = self.render.skin_btn

        self._bind_events()

    def _bind_events(self):
        def _host_window():
            return self.window() or self.parent()

        self.logout_label.mousePressEvent = lambda e: self.logout_clicked.emit()
        self.min_label.mousePressEvent = lambda e: _host_window().showMinimized()
        self.max_label.mousePressEvent = lambda e: _host_window().toggle_maximize() if hasattr(_host_window(), "toggle_maximize") else _host_window().showMaximized()
        self.close_label.mousePressEvent = lambda e: _host_window().close()

        def _toggle_skin(e):
            if e.button() == Qt.LeftButton:
                res = QMessageBox.question(
                    self,
                    "切换皮肤",
                    "确定要切换皮肤吗？\n确认后将返回登录界面并切换样式",
                    QMessageBox.Yes | QMessageBox.No
                )
                if res == QMessageBox.Yes:
                    # 只切换皮肤变量，发信号让管理器自己跳登录页
                    UIFactory.toggle_skin()
                    skin_signal.toggle.emit()

        self.skin_btn.mousePressEvent = _toggle_skin