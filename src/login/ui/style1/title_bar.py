from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from src.login.ui.factory.factory import UIFactory

class CustomTitleBar(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        
        # 从工厂创建对应皮肤的标题栏
        self.render = UIFactory.create_title_bar(title, self)

        # 把渲染的标题栏放进自己的布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.render)

        # 暴露按钮
        self.logout_label = self.render.logout_label
        self.min_label = self.render.min_label
        self.max_label = self.render.max_label
        self.close_label = self.render.close_label

        self._bind_events()

    def _bind_events(self):
        def _host_window():
            return self.window() if self.window() is not None else self.parent()

        self.logout_label.mousePressEvent = lambda e: self.logout_clicked.emit()
        self.min_label.mousePressEvent = lambda e: _host_window().showMinimized()
        self.max_label.mousePressEvent = lambda e: _host_window().toggle_maximize() if hasattr(_host_window(), "toggle_maximize") else _host_window().showMaximized()
        self.close_label.mousePressEvent = lambda e: _host_window().close()