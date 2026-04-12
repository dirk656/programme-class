from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.factory.factory import UIFactory

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
        self.logout_label.mousePressEvent = lambda e: self.logout_clicked.emit()
        self.min_label.mousePressEvent = lambda e: self.parent().showMinimized()
        self.max_label.mousePressEvent = lambda e: self.parent().toggle_maximize()
        self.close_label.mousePressEvent = lambda e: self.parent().close()