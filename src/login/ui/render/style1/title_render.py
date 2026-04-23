from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CustomTitleRender(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self._init_ui(title)

    def _init_ui(self, title):
        self.setStyleSheet("""
            background-color: #202020; 
            border-bottom: 1px solid #333;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        """)

        title_layout = QHBoxLayout(self)
        title_layout.setContentsMargins(20, 10, 20, 15)
        title_layout.setSpacing(10)

        # ========== 左边标题：彻底无边框 + 透明背景 ==========
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            color: white; 
            font-size: 18px; 
            font-weight: bold;
            border: none;
            background-color: transparent;
        """)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        # ========== 退出登录 ==========
        self.logout_label = QLabel("退出登录")
        self.logout_label.setFixedSize(80, 40)
        self.logout_label.setStyleSheet("""
            QLabel {
                color: #ffffff; 
                font-size: 16px; 
                text-align: center; 
                border: none; 
                background-color: transparent;
                padding-top: 4px;
            }
            QLabel:hover {
                background-color: #ff4444; 
                border-radius: 5px;
            }
        """)
        self.logout_label.setAlignment(Qt.AlignCenter)
        self.logout_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.logout_label)

        # ========== 最小化 ==========
        self.min_label = QLabel("—")
        self.min_label.setFixedSize(50, 50)
        self.min_label.setStyleSheet("""
            QLabel { 
                color: #ffffff; 
                font-size: 24px; 
                text-align: center; 
                border: none; 
                background-color: transparent;
            }
            QLabel:hover { 
                background-color: #444444; 
                border-radius: 5px; 
            }
        """)
        self.min_label.setAlignment(Qt.AlignCenter)
        self.min_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.min_label)

        # ========== 最大化 ==========
        self.max_label = QLabel("□")
        self.max_label.setFixedSize(50, 50)
        self.max_label.setStyleSheet("""
            QLabel { 
                color: #ffffff; 
                font-size: 24px; 
                text-align: center; 
                border: none; 
                background-color: transparent;
            }
            QLabel:hover { 
                background-color: #444444; 
                border-radius: 5px; 
            }
        """)
        self.max_label.setAlignment(Qt.AlignCenter)
        self.max_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.max_label)

        # ========== 关闭 ==========
        self.close_label = QLabel("×")
        self.close_label.setFixedSize(50, 50)
        self.close_label.setStyleSheet("""
            QLabel { 
                color: #ffffff; 
                font-size: 24px; 
                text-align: center; 
                border: none; 
                background-color: transparent;
            }
            QLabel:hover { 
                background-color: #ff4444; 
                border-radius: 5px; 
            }
        """)
        self.close_label.setAlignment(Qt.AlignCenter)
        self.close_label.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(self.close_label)