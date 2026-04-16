# ui/render/style2/main_render.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QLabel,
    QHeaderView, QSizePolicy, QLineEdit,
    QStackedWidget
)
from PyQt5.QtCore import Qt
from src.login.ui.style1.title_bar import CustomTitleBar

class MainRender:
    def __init__(self, window):
        self.window = window
        self.stacked_widget = None

        self.camera_label = None
        self.record_table = None
        self.start_checkin_btn = None
        self.student_username_input = None
        self.name_input = None
        self.register_btn = None
        self.stop_btn = None
        self.clear_btn = None
        self.stat_btn = None

        self.table = None
        self.refresh_btn = None
        self.back_btn = None

        self.title_bar = None

    def build_ui(self):
        win = self.window
        win.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #303133;
                background-color: #F0F2F5;
                border: none;  /* 全局去黑边框 */
            }
        """)

        central_widget = QWidget()
        central_widget.setObjectName("main_central_widget")
        central_widget.setStyleSheet("""
            QWidget#main_central_widget {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E4E7ED;
                border: none;
            }
        """)
        win.setCentralWidget(central_widget)

        total_layout = QVBoxLayout(central_widget)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_layout.setSpacing(0)

        self.title_bar = CustomTitleBar("人脸识别签到系统", win)
        total_layout.addWidget(self.title_bar)

        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background:#409EFF; border: none;")
        total_layout.addWidget(divider)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("border: none;")
        total_layout.addWidget(self.stacked_widget)

    def add_checkin_page(self, page):
        widget = QWidget()
        widget.setStyleSheet("border: none;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        left_layout = QVBoxLayout()
        record_label = QLabel("签到记录")
        record_label.setStyleSheet("font-size:18px; font-weight:bold; color:#303133; border: none;")
        left_layout.addWidget(record_label)

        self.record_table = QTableWidget()
        self.record_table.setColumnCount(3)
        self.record_table.setHorizontalHeaderLabels(["姓名","签到时间","状态"])
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.record_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.record_table.setStyleSheet("""
            QTableWidget {
                background-color:#F8F9FA; 
                color:#303133; 
                border-radius:8px; 
                border:1px solid #E4E7ED; 
                gridline-color:#F0F0F0;
                border: none;  /* 去掉表格默认黑框 */
            }
            QTableWidget::header {
                background-color:#F0F2F5; 
                color:#606266; 
                font-weight:bold;
                border-bottom:1px solid #E4E7ED;
                border: none;
            }
            QTableWidget::item {padding:8px;}
            QTableWidget::item:selected {background-color:#ECF5FF; color:#409EFF;}
        """)
        left_layout.addWidget(self.record_table)

        btn_layout1 = QHBoxLayout()
        self.clear_btn = QPushButton("清空记录")
        self.stat_btn = QPushButton("历史统计")
        btn_layout1.addWidget(self.clear_btn)
        btn_layout1.addWidget(self.stat_btn)
        left_layout.addLayout(btn_layout1)

        right_layout = QVBoxLayout()
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640,480)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setText("摄像头未启动")
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color:#F8F9FA; 
                border-radius:8px; 
                border:1px solid #409EFF; 
                color:#606266;
                border: none;
            }
        """)
        right_layout.addWidget(self.camera_label)

        btn_layout2 = QHBoxLayout()
        self.student_username_input = QLineEdit()
        self.student_username_input.setPlaceholderText("输入学生登录账号")
        self.start_checkin_btn = QPushButton("开始签到")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入姓名")
        self.register_btn = QPushButton("录入人脸")
        self.stop_btn = QPushButton("停止")

        btn_style = """
            QPushButton {
                background-color:#409EFF; 
                color:#FFFFFF; 
                border-radius:15px;
                font-size:14px; 
                padding:8px 16px;
                border:none;
                border: none;
            }
            QPushButton:hover {background-color:#66B1FF;}
            QPushButton:disabled {background-color:#C0C4CC;}
        """
        self.start_checkin_btn.setStyleSheet(btn_style)
        self.register_btn.setStyleSheet(btn_style)
        self.stop_btn.setStyleSheet(btn_style)
        self.clear_btn.setStyleSheet(btn_style)
        self.stat_btn.setStyleSheet(btn_style)

        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color:#F8F9FA; 
                color:#303133; 
                border-radius:8px; 
                padding:8px 12px;
                border:1px solid #DCDFE6;
                border: none;
            }
            QLineEdit:focus {border-color:#409EFF; background-color:#FFFFFF;}
        """)
        self.student_username_input.setStyleSheet("""
            QLineEdit {
                background-color:#F8F9FA; 
                color:#303133; 
                border-radius:8px; 
                padding:8px 12px;
                border:1px solid #DCDFE6;
                border: none;
            }
            QLineEdit:focus {border-color:#409EFF; background-color:#FFFFFF;}
        """)

        btn_layout2.addWidget(self.start_checkin_btn)
        btn_layout2.addWidget(self.student_username_input)
        btn_layout2.addWidget(self.name_input)
        btn_layout2.addWidget(self.register_btn)
        btn_layout2.addWidget(self.stop_btn)
        right_layout.addLayout(btn_layout2)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 5)
        layout.addLayout(main_layout)

        self.stacked_widget.addWidget(widget)

    def add_stat_page(self, page):
        widget = QWidget()
        widget.setStyleSheet("border: none;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        title = QLabel("历史签到记录")
        title.setStyleSheet("font-size:20px; color:#303133; font-weight:bold; border: none;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["账号","姓名","时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color:#F8F9FA; 
                color:#303133; 
                border-radius:8px; 
                border:1px solid #E4E7ED; 
                gridline-color:#F0F0F0;
                border: none;
            }
            QTableWidget::header {
                background-color:#F0F2F5; 
                color:#606266; 
                font-weight:bold;
                border-bottom:1px solid #E4E7ED;
                border: none;
            }
            QTableWidget::item {padding:8px;}
            QTableWidget::item:selected {background-color:#ECF5FF; color:#409EFF;}
        """)
        layout.addWidget(self.table)

        self.refresh_btn = QPushButton("刷新数据")
        self.back_btn = QPushButton("返回")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color:#409EFF; 
                color:#FFFFFF; 
                border-radius:8px;
                font-size:14px; 
                padding:8px 16px;
                border:none;
                border: none;
            }
            QPushButton:hover {background-color:#66B1FF;}
        """)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color:#F8F9FA; 
                color:#606266; 
                border:1px solid #DCDFE6;
                border-radius:8px;
                font-size:14px; 
                padding:8px 16px;
                border: none;
            }
            QPushButton:hover {background-color:#ECF5FF; border-color:#409EFF;}
        """)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.back_btn)

        self.stacked_widget.addWidget(widget)

    def switch_to_page(self, index):
        self.stacked_widget.setCurrentIndex(index)