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

        # 主窗口控件
        self.title_bar = None
        self.stack = None
        self.btn_home = None
        self.btn_record = None

        # 子页面UI（全部在这里创建！）
        self.home_page_ui = None
        self.record_page_ui = None

    def build_ui(self):
        """构建整个学生界面：外壳 + 子页面全部UI"""
        win = self.window
        win.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #ffffff;
                background-color: #202020;
            }
        """)

        central = QWidget()
        central.setStyleSheet("background:#202020; border-radius:12px;")
        win.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # 标题栏
        self.title_bar = CustomTitleBar(f"学生系统 - {self.username}", win)
        main_layout.addWidget(self.title_bar)

        # 分割线
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background:#00d2be;")
        main_layout.addWidget(divider)

        # 内容区 = 导航 + 堆叠页面
        content_layout = QHBoxLayout()
        nav_widget = self._build_nav()
        self.stack = QStackedWidget()
        content_layout.addWidget(nav_widget, stretch=1)
        content_layout.addWidget(self.stack, stretch=6)
        main_layout.addLayout(content_layout)

    def _build_nav(self):
        nav = QWidget()
        nav.setStyleSheet("background-color:#2c3e50;")
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
                color:white;
                background:#34495e;
                border:none;
                border-radius:6px;
                text-align:left;
            }
            QPushButton:checked {
                background:#3498db;
            }
        """
        self.btn_home.setStyleSheet(btn_style)
        self.btn_record.setStyleSheet(btn_style)

        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_record)
        layout.addStretch()
        return nav

    # --------------------- 子页面UI工厂 ---------------------
    def create_home_page_ui(self, parent):
        """创建 首页 所有UI + 样式"""
        ui = HomePageUI(parent)
        return ui

    def create_record_page_ui(self, parent):
        """创建 记录页 所有UI + 样式"""
        ui = RecordPageUI(parent)
        return ui

    def add_page(self, page):
        self.stack.addWidget(page)


# --------------------- 子页面UI全部放在这里 ---------------------
class HomePageUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.welcome_label = None
        self.card_total = None
        self.card_missed = None
        self.card_rate = None
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background:#2c2c2c;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(20)

        # 欢迎文字
        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("font-size:22px; color:#3498db; font-weight:bold;")
        layout.addWidget(self.welcome_label)

        # 卡片行
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        self.card_total = self._make_card("本月已签到", "#2ecc71")
        self.card_missed = self._make_card("异常/缺勤", "#e74c3c")
        self.card_rate = self._make_card("本月出勤率", "#3498db")
        card_layout.addWidget(self.card_total)
        card_layout.addWidget(self.card_missed)
        card_layout.addWidget(self.card_rate)
        layout.addLayout(card_layout)
        layout.addStretch()

    def _make_card(self, title_text, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color:#34495e;
                border-radius:10px;
                border-left:5px solid {color};
            }}
        """)
        layout = QVBoxLayout(card)
        title = QLabel(title_text)
        title.setStyleSheet("color:#bdc3c7; font-size:14px;")
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

        # 标题栏
        top_bar = QHBoxLayout()
        title = QLabel("我的签到流水")
        title.setStyleSheet("font-size:20px; color:#3498db; font-weight:bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        self.refresh_btn = QPushButton("刷新数据")
        self.refresh_btn.setStyleSheet("""
            QPushButton {background:#3498db; color:white; padding:8px 14px; border-radius:5px;}
            QPushButton:hover {background:#2980b9;}
        """)
        top_bar.addWidget(self.refresh_btn)
        layout.addLayout(top_bar)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["日期","签到时间","状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {background:#333; color:white; border-radius:8px;}
            QHeaderView {background:#444; color:white;}
        """)
        layout.addWidget(self.table)