from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from src.login.ui.style1.title_bar import CustomTitleBar

class LoginRender:
    def __init__(self, window):
        self.win = window
        # 保存所有控件，供业务层使用
        self.username_input = None
        self.password_input = None
        self.login_btn = None
        self.reset_btn = None
        self.register_btn = None

    def build(self):
        """构建整个登录界面：布局、控件、样式"""
        self.win.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei UI", "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                color: #ffffff;
                background-color: #202020;
            }
        """)

        # 中心圆角部件
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #202020; border-radius: 10px;")
        self.win.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        self.win.title_bar = CustomTitleBar("人脸识别签到系统 - 登录", self.win)
        main_layout.addWidget(self.win.title_bar)

        # 分割线
        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: #00d2be;")
        main_layout.addWidget(divider)

        # 内容区域
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(100, 50, 100, 50)
        content_layout.setSpacing(30)
        content_layout.setAlignment(Qt.AlignCenter)

        # 标题
        title = QLabel("用户登录")
        title.setStyleSheet("font-size:28px; font-weight:bold; color:#00d2be;")
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)

        # ===================== 用户名输入 =====================
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setSpacing(15)

        user_label = QLabel("用户名：")
        user_label.setStyleSheet("font-size:16px; color:white; width:70px;")
        user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setMinimumHeight(60)
        self.username_input.setStyleSheet("""
            QLineEdit { background-color:#333; color:white; padding:12px 15px; border:none; border-radius:8px; }
            QLineEdit:focus { border:2px solid #00d2be; background-color:#3a3a3a; }
        """)

        user_layout.addWidget(user_label)
        user_layout.addWidget(self.username_input)
        content_layout.addWidget(user_widget)

        # ===================== 密码输入 =====================
        pwd_widget = QWidget()
        pwd_layout = QHBoxLayout(pwd_widget)
        pwd_layout.setSpacing(15)

        pwd_label = QLabel("密　码：")
        pwd_label.setStyleSheet("font-size:16px; color:white; width:70px;")
        pwd_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setMinimumHeight(60)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit { background-color:#333; color:white; padding:12px 15px; border:none; border-radius:8px; }
            QLineEdit:focus { border:2px solid #00d2be; background-color:#3a3a3a; }
        """)

        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.password_input)
        content_layout.addWidget(pwd_widget)

        # ===================== 按钮组 =====================
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)

        self.login_btn = QPushButton("登录")
        self.reset_btn = QPushButton("重置")
        self.login_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00d2be,stop:1 #009990); color:white; border:none; padding:12px 40px; border-radius:8px; font-size:16px; }
            QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00f0e0,stop:1 #00aaaa); }
        """)
        self.reset_btn.setStyleSheet("""
            QPushButton { background-color:#444; color:white; border:none; padding:12px 40px; border-radius:8px; font-size:16px; }
            QPushButton:hover { background-color:#555; }
        """)

        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.reset_btn)
        content_layout.addWidget(btn_widget)

        # 注册按钮
        self.register_btn = QPushButton("没有账号？点击注册")
        self.register_btn.setStyleSheet("""
            QPushButton { color:#00d2be; border:none; font-size:14px; }
            QPushButton:hover { color:#00f0e0; text-decoration:underline; }
        """)
        content_layout.addWidget(self.register_btn, alignment=Qt.AlignCenter)

        main_layout.addWidget(content)

        # 光标自动放在用户名输入框
        self.username_input.setFocus()

    def bind_events(self, login_click, reset_click, register_click):
        """绑定事件，由业务层传入"""
        self.login_btn.clicked.connect(login_click)
        self.reset_btn.clicked.connect(reset_click)
        self.register_btn.clicked.connect(register_click)
        # 用户名行enter跳转 和 密码行enter触发登录
        self.username_input.returnPressed.connect(self.password_input.setFocus) 
        self.password_input.returnPressed.connect(login_click)