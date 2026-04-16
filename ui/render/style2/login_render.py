# ui/render/style2/login_render.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from ui.style1.title_bar import CustomTitleBar

class LoginRender:
    def __init__(self, window):
        self.win = window
        self.username_input = None
        self.password_input = None
        self.login_btn = None
        self.reset_btn = None
        self.register_btn = None

    def build(self):
        """柔和护眼登录页（已去黑边框）"""
        self.win.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #303133;
                background-color: #F0F2F5;
                border: none;  /* 全局去掉默认黑边框 */
            }
        """)

        central_widget = QWidget()
        central_widget.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #E4E7ED;
            border: none;  /* 去掉容器自身黑框 */
        """)
        self.win.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.win.title_bar = CustomTitleBar("人脸识别签到系统 - 登录", self.win)
        main_layout.addWidget(self.win.title_bar)

        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: #409EFF; border: none;")
        main_layout.addWidget(divider)

        content = QWidget()
        content.setStyleSheet("border: none;")  # 去掉内容区黑框
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(100, 50, 100, 50)
        content_layout.setSpacing(30)
        content_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("用户登录")
        title.setStyleSheet("font-size:28px; font-weight:bold; color:#409EFF; border: none;")
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)

        # ===================== 用户名输入 =====================
        user_widget = QWidget()
        user_widget.setStyleSheet("border: none;")  # 去掉行黑框
        user_layout = QHBoxLayout(user_widget)
        user_layout.setSpacing(15)

        user_label = QLabel("用户名：")
        user_label.setStyleSheet("font-size:16px; color:#606266; width:70px; border: none;")
        user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setMinimumHeight(60)
        self.username_input.setStyleSheet("""
            QLineEdit { 
                background-color:#F8F9FA; 
                color:#303133; 
                padding:12px 15px; 
                border:1px solid #DCDFE6; 
                border-radius:8px;
                border: none;  /* 去掉输入框默认黑边 */
            }
            QLineEdit:focus { 
                border:1px solid #409EFF; 
                background-color:#FFFFFF; 
            }
        """)

        user_layout.addWidget(user_label)
        user_layout.addWidget(self.username_input)
        content_layout.addWidget(user_widget)

        # ===================== 密码输入 =====================
        pwd_widget = QWidget()
        pwd_widget.setStyleSheet("border: none;")
        pwd_layout = QHBoxLayout(pwd_widget)
        pwd_layout.setSpacing(15)

        pwd_label = QLabel("密　码：")
        pwd_label.setStyleSheet("font-size:16px; color:#606266; width:70px; border: none;")
        pwd_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setMinimumHeight(60)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit { 
                background-color:#F8F9FA; 
                color:#303133; 
                padding:12px 15px; 
                border:1px solid #DCDFE6; 
                border-radius:8px;
                border: none;
            }
            QLineEdit:focus { 
                border:1px solid #409EFF; 
                background-color:#FFFFFF; 
            }
        """)

        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.password_input)
        content_layout.addWidget(pwd_widget)

        # ===================== 按钮组 =====================
        btn_widget = QWidget()
        btn_widget.setStyleSheet("border: none;")
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)

        self.login_btn = QPushButton("登录")
        self.reset_btn = QPushButton("重置")
        self.login_btn.setStyleSheet("""
            QPushButton { 
                background-color:#409EFF; 
                color:white; 
                border:none; 
                padding:12px 40px; 
                border-radius:8px; 
                font-size:16px;
                border: none;
            }
            QPushButton:hover { 
                background-color:#66B1FF; 
            }
        """)
        self.reset_btn.setStyleSheet("""
            QPushButton { 
                background-color:#F8F9FA; 
                color:#606266; 
                border:1px solid #DCDFE6; 
                padding:12px 40px; 
                border-radius:8px; 
                font-size:16px;
                border: none;
            }
            QPushButton:hover { 
                background-color:#ECF5FF; 
                border-color:#409EFF;
            }
        """)

        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.reset_btn)
        content_layout.addWidget(btn_widget)

        self.register_btn = QPushButton("没有账号？点击注册")
        self.register_btn.setStyleSheet("""
            QPushButton { color:#409EFF; border:none; font-size:14px; border: none; }
            QPushButton:hover { color:#66B1FF; text-decoration:underline; }
        """)
        content_layout.addWidget(self.register_btn, alignment=Qt.AlignCenter)

        main_layout.addWidget(content)

    def bind_events(self, login_click, reset_click, register_click):
        self.login_btn.clicked.connect(login_click)
        self.reset_btn.clicked.connect(reset_click)
        self.register_btn.clicked.connect(register_click)