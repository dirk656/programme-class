# components/title_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from config.settings import TITLE_BAR_HEIGHT, COLOR_BACKGROUND, WINDOW_ROUND_RADIUS

class CustomTitleBar(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self._init_ui(title)
        self._bind_events()

    def _init_ui(self, title):
        self.setStyleSheet(f"""
            background-color: {COLOR_BACKGROUND}; 
            border-bottom: 1px solid #333;
            border-top-left-radius: {WINDOW_ROUND_RADIUS}px;
            border-top-right-radius: {WINDOW_ROUND_RADIUS}px;
        """)

        title_layout = QHBoxLayout(self)
        title_layout.setContentsMargins(20, 10, 20, 15)
        title_layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        self.logout_label = QLabel("退出登录")
        self.logout_label.setFixedSize(80, 40)
        self.logout_label.setStyleSheet("""
            QLabel {
                color: #ffffff; font-size: 16px; text-align: center; border: none; padding-top: 4px;
            }
            QLabel:hover {
                background-color: #ff4444; border-radius: 5px;
            }
        """)
        self.logout_label.setAlignment(Qt.AlignCenter)
        self.logout_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.logout_label)

        self.min_label = QLabel("—")
        self.min_label.setFixedSize(50, 50)
        self.min_label.setStyleSheet("""
            QLabel { color: #ffffff; font-size: 24px; text-align: center; border: none; }
            QLabel:hover { background-color: #444444; border-radius: 5px; }
        """)
        self.min_label.setAlignment(Qt.AlignCenter)
        self.min_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.min_label)

        self.max_label = QLabel("□")
        self.max_label.setFixedSize(50, 50)
        self.max_label.setStyleSheet("""
            QLabel { color: #ffffff; font-size: 24px; text-align: center; border: none; }
            QLabel:hover { background-color: #444444; border-radius: 5px; }
        """)
        self.max_label.setAlignment(Qt.AlignCenter)
        self.max_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.max_label)

        self.close_label = QLabel("×")
        self.close_label.setFixedSize(50, 50)
        self.close_label.setStyleSheet("""
            QLabel { color: #ffffff; font-size: 24px; text-align: center; border: none; }
            QLabel:hover { background-color: #ff4444; border-radius: 5px; }
        """)
        self.close_label.setAlignment(Qt.AlignCenter)
        self.close_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.close_label)

    def _bind_events(self):
        self.logout_label.mousePressEvent = lambda e: self.logout_clicked.emit()
        self.min_label.mousePressEvent = lambda e: self.parent.showMinimized()
        self.max_label.mousePressEvent = lambda e: self.parent.toggle_maximize()
        self.close_label.mousePressEvent = lambda e: self.parent.close()

