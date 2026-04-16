from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget,
    QFrame, QTableWidget, QHeaderView, QLineEdit
)
from PyQt5.QtCore import Qt
from ui.style1.title_bar import CustomTitleBar

class StudentRender:
    def __init__(self, window):
        self.window = window
        self.username = window.username

        self.title_bar = None
        self.stack = None
        self.btn_home = None
        self.btn_record = None

        self.home_page_ui = None
        self.record_page_ui = None

    def build_ui(self):
        win = self.window
        win.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #303133;
                background-color: #F8F9FA;
                border: none;
            }
        """)

        central = QWidget()
        central.setStyleSheet("background:#FFFFFF; border-radius:12px; border: none;")
        win.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(f"学生系统 - {self.username}", win)
        main_layout.addWidget(self.title_bar)

        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background:#409eff; border: none;")
        main_layout.addWidget(divider)

        content_layout = QHBoxLayout()
        nav_widget = self._build_nav()
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("border: none;")
        content_layout.addWidget(nav_widget, stretch=1)
        content_layout.addWidget(self.stack, stretch=6)
        main_layout.addLayout(content_layout)

    def _build_nav(self):
        nav = QWidget()
        nav.setStyleSheet("background-color:#F8F9FA; border-right: 1px solid #E4E7ED; border: none;")
        layout = QVBoxLayout(nav)
        layout.setContentsMargins(10,20,10,20)
        layout.setSpacing(15)

        self.btn_home = QPushButton("📊 数据看板")
        self.btn_record = QPushButton("📋 签到记录")
        self.btn_home.setCheckable(True)
        self.btn_record.setCheckable(True)

        btn_style = """
            QPushButton {
                padding: 10px;
                font-size:14px;
                color:#606266;
                background:#ffffff;
                border: 1px solid #DCDFE6;
                border-radius:6px;
                text-align:left;
                border: none;
            }
            QPushButton:checked {
                background:#ecf5ff;
                color:#409eff;
                border-color:#409eff;
            }
        """
        self.btn_home.setStyleSheet(btn_style)
        self.btn_record.setStyleSheet(btn_style)

        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_record)
        layout.addStretch()
        return nav

    def create_home_page_ui(self, parent):
        ui = HomePageUI(parent)
        return ui

    def create_record_page_ui(self, parent):
        ui = RecordPageUI(parent)
        return ui

    def add_page(self, page):
        self.stack.addWidget(page)


class HomePageUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.welcome_label = None
        self.card_total = None
        self.card_missed = None
        self.card_rate = None
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background:#FFFFFF; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(20)

        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("font-size:22px; color:#409eff; font-weight:bold;")
        layout.addWidget(self.welcome_label)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        self.card_total = self._make_card("本月已签到", "#67c23a")
        self.card_missed = self._make_card("异常/缺勤", "#f56c6c")
        self.card_rate = self._make_card("本月出勤率", "#409eff")
        card_layout.addWidget(self.card_total)
        card_layout.addWidget(self.card_missed)
        card_layout.addWidget(self.card_rate)
        layout.addLayout(card_layout)
        layout.addStretch()

    def _make_card(self, title_text, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color:#ffffff;
                border-radius:10px;
                border-left:5px solid {color};
                border: none;
            }}
        """)
        layout = QVBoxLayout(card)
        title = QLabel(title_text)
        title.setStyleSheet("color:#606266; font-size:14px;")
        value = QLabel("加载中...")
        value.setStyleSheet(f"color:{color}; font-size:28px; font-weight:bold;")
        value.setObjectName("card_value")
        layout.addWidget(title)
        layout.addWidget(value)
        return card


class RecordPageUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.table = None
        self.refresh_btn = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        title = QLabel("我的签到流水")
        title.setStyleSheet("font-size:20px; color:#409eff; font-weight:bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.refresh_btn = QPushButton("刷新数据")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background:#409eff;
                color:white;
                padding:8px 14px;
                border-radius:5px;
                border: none;
            }
            QPushButton:hover {
                background:#66b1ff;
            }
        """)
        top_bar.addWidget(self.refresh_btn)
        layout.addLayout(top_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["日期","签到时间","状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background:#ffffff;
                color:#303133;
                border-radius:8px;
                border: none;
            }
            QHeaderView {
                background:#f5f7fa;
                color:#606266;
                border: none;
            }
        """)
        layout.addWidget(self.table)