#ui/style1/register_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from config.settings import COLOR_BACKGROUND
from manager.style_manager import get_global_style
from core.db_manager import add_user

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户注册")
        self.setGeometry(650, 300, 500, 450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet(get_global_style())
        self.drag_pos = None

        central = QWidget()
        central.setStyleSheet(f"background:{COLOR_BACKGROUND};border-radius:10px;")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(40,40,40,40)
        layout.setSpacing(25)

        title = QLabel("用户注册")
        title.setStyleSheet("font-size:26px; font-weight:bold; color:#00d2be;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.user_input = self.make_input_row("账号：", layout)
        self.pwd_input = self.make_input_row("密码：", layout, pwd=True)
        self.pwd2_input = self.make_input_row("确认密码：", layout, pwd=True)

        # 角色
        role_row = QWidget()
        role_layout = QHBoxLayout(role_row)
        role_layout.setSpacing(15)
        role_label = QLabel("身份：")
        role_label.setStyleSheet("color:white; font-size:15px; width:60px;")
        role_label.setAlignment(Qt.AlignRight)
        self.role_combo = QComboBox()
        self.role_combo.addItem("学生", "student")
        self.role_combo.addItem("老师", "teacher")
        self.role_combo.setStyleSheet("""
            QComboBox { background-color:#333; color:white; padding:10px; border-radius:8px; font-size:14px; }
        """)
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addWidget(role_row)

        self.reg_btn = QPushButton("注册")
        self.reg_btn.setStyleSheet("""
            QPushButton { background:#00d2be; color:white; padding:12px; border-radius:8px; font-size:15px; }
            QPushButton:hover { background:#00f0e0; }
        """)
        layout.addWidget(self.reg_btn)

        self.close_btn = QPushButton("取消")
        self.close_btn.setStyleSheet("""
            QPushButton { background:#444; color:white; padding:10px; border-radius:8px; }
            QPushButton:hover { background:#555; }
        """)
        layout.addWidget(self.close_btn)

        self.reg_btn.clicked.connect(self.do_register)
        self.close_btn.clicked.connect(self.close)

    def make_input_row(self, text, layout, pwd=False):
        w = QWidget()
        h = QHBoxLayout(w)
        h.setSpacing(15)
        lab = QLabel(text)
        lab.setStyleSheet("color:white; font-size:15px; width:60px;")
        lab.setAlignment(Qt.AlignRight)
        ipt = QLineEdit()
        if pwd:
            ipt.setEchoMode(QLineEdit.Password)
        ipt.setStyleSheet("""
            QLineEdit { background:#333; color:white; padding:10px; border-radius:8px; }
            QLineEdit:focus { border:2px solid #00d2be; }
        """)
        h.addWidget(lab)
        h.addWidget(ipt)
        layout.addWidget(w)
        return ipt

    def do_register(self):
        u = self.user_input.text().strip()
        p1 = self.pwd_input.text().strip()
        p2 = self.pwd2_input.text().strip()
        role = self.role_combo.currentData()

        if not u or not p1 or not p2:
            QMessageBox.warning(self, "错误", "请填写完整")
            return
        if p1 != p2:
            QMessageBox.warning(self, "错误", "两次密码不一致")
            return

        ok, msg = add_user(u, p1, role)
        if ok:
            QMessageBox.information(self, "成功", "注册成功！")
            self.close()
        else:
            QMessageBox.warning(self, "失败", msg)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None