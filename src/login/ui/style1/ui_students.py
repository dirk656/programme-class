# ui/style1/ui_students.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
    QStackedWidget, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

# 假设这些是你原本的配置
from config.settings import (ICON_PATH, WINDOW_ROUND_RADIUS,
                             COLOR_BACKGROUND, COLOR_PRIMARY, FONT_SIZE_TITLE,
                             BUTTON_ROUND_RADIUS)
from components.title_bar import CustomTitleBar
from manager.style_manager import get_global_style

from PyQt5.QtCore import QThread, pyqtSignal
import traceback

# 异步查询线程：避免阻塞主线程
class DbQueryThread(QThread):
    # 信号：查询完成、查询出错
    records_ready = pyqtSignal(list)  # 我的考勤数据
    stats_ready = pyqtSignal(dict)     # 数据看板统计
    error_occurred = pyqtSignal(str)

    def __init__(self, query_type, username=None, parent=None):
        super().__init__(parent)
        self.query_type = query_type  # "my_records" / "my_stats"
        self.username = username

    def run(self):
        try:
            from core.service import CheckInService, StudentService
            if self.query_type == "my_records":
                # 查询个人签到记录
                records = CheckInService.get_my_records(self.username)
                self.records_ready.emit(records)
            elif self.query_type == "my_stats":
                # 查询个人统计数据
                stat = StudentService.get_student_stat(self.username)
                self.stats_ready.emit(stat)
        except Exception as e:
            err_msg = f"查询失败：{str(e)}\n{traceback.format_exc()}"
            self.error_occurred.emit(err_msg)


# ===================== 学生首页 (仪表盘) =====================
class StudentHomePage(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.query_thread = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 欢迎标语
        welcome_lbl = QLabel(f"欢迎回来，{self.username}！")
        welcome_lbl.setStyleSheet(f"font-size:{FONT_SIZE_TITLE}px; color:{COLOR_PRIMARY}; font-weight:bold;")
        layout.addWidget(welcome_lbl)

        # 数据卡片布局
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # 卡片1：总签到次数
        self.card_total = self.create_stat_card("本月已签到", "加载中...", "#2ecc71")
        # 卡片2：缺勤次数
        self.card_missed = self.create_stat_card("异常/缺勤", "加载中...", "#e74c3c")
        # 卡片3：出勤率
        self.card_rate = self.create_stat_card("本月出勤率", "加载中...", "#3498db")

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_missed)
        cards_layout.addWidget(self.card_rate)
        layout.addLayout(cards_layout)
        layout.addStretch()

    def create_stat_card(self, title_text, value_text, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2c3e50; 
                border-radius: 10px; 
                border-left: 5px solid {color};
            }}
        """)
        vbox = QVBoxLayout(card)
        title = QLabel(title_text)
        title.setStyleSheet("color: #bdc3c7; font-size: 14px;")
        value = QLabel(value_text)
        value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        # 👇 给数值 Label 设对象名，方便后面精准找到它
        value.setObjectName("card_value")
        vbox.addWidget(title)
        vbox.addWidget(value)
        return card

    # 异步刷新统计（不阻塞）
    def refresh_stats(self):
        if self.query_thread and self.query_thread.isRunning():
            self.query_thread.terminate()
            self.query_thread.wait()

        # 👇 只重置数值 Label，不碰标题
        self.card_total.findChild(QLabel, "card_value").setText("加载中...")
        self.card_missed.findChild(QLabel, "card_value").setText("加载中...")
        self.card_rate.findChild(QLabel, "card_value").setText("加载中...")

        self.query_thread = DbQueryThread("my_stats", self.username)
        self.query_thread.stats_ready.connect(self.on_stats_loaded)
        self.query_thread.error_occurred.connect(self.on_query_error)
        self.query_thread.start()

    # 统计数据加载完成
    def on_stats_loaded(self, stat):
        total = stat.get("total", 0)
        missed = stat.get("missed", 0)
        rate = stat.get("rate", "0%")

        # 👇 精准找到每个卡片里的数值 Label（对象名是 card_value）
        self.card_total.findChild(QLabel, "card_value").setText(f"{total} 次")
        self.card_missed.findChild(QLabel, "card_value").setText(f"{missed} 次")
        self.card_rate.findChild(QLabel, "card_value").setText(rate)

    # 查询出错
    def on_query_error(self, msg):
        QMessageBox.warning(self, "统计失败", msg)
        self.card_total.findChild(QLabel).setText("查询失败")
        self.card_missed.findChild(QLabel).setText("查询失败")
        self.card_rate.findChild(QLabel).setText("查询失败")


# ===================== 学生签到记录页 =====================
class StudentRecordPage(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.query_thread = None  # 异步线程
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 顶部工具栏
        top_bar = QHBoxLayout()
        title = QLabel("我的签到流水")
        title.setStyleSheet(f"font-size:20px; color:{COLOR_PRIMARY}; font-weight:bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        refresh_btn = QPushButton("刷新数据")
        refresh_btn.setStyleSheet(f"""
            QPushButton{{background:{COLOR_PRIMARY};color:white; padding:8px 15px; border-radius:5px;}}
            QPushButton:hover{{background:#00f0e0;}}
        """)
        refresh_btn.clicked.connect(self.start_async_load)
        top_bar.addWidget(refresh_btn)
        layout.addLayout(top_bar)

        # 表格配置
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["日期", "签到时间", "状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {background:#333; color:white; border-radius:8px; gridline-color: #444;}
            QTableWidget::header {background:#444; color:white; font-weight: bold;}
            QHeaderView::section {background-color: #444; border: 1px solid #555; padding: 5px;}
        """)
        layout.addWidget(self.table)


    # 数据加载完成（主线程安全更新UI）
    def on_records_loaded(self, records):
        # 性能优化：暂停表格更新
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(len(records))

        for row, data in enumerate(records):
            try:
                username_db, real_name, sign_time = data
                # 拆分日期+时间
                date_str = sign_time.split(" ")[0] if " " in sign_time else sign_time
                time_str = sign_time.split(" ")[1] if " " in sign_time else ""

                # 创建单元格
                date_item = QTableWidgetItem(date_str)
                time_item = QTableWidgetItem(time_str)
                status_item = QTableWidgetItem("正常")

                # 居中+颜色
                date_item.setTextAlignment(Qt.AlignCenter)
                time_item.setTextAlignment(Qt.AlignCenter)
                status_item.setTextAlignment(Qt.AlignCenter)
                status_item.setForeground(Qt.green)

                # 赋值
                self.table.setItem(row, 0, date_item)
                self.table.setItem(row, 1, time_item)
                self.table.setItem(row, 2, status_item)
            except Exception as e:
                print(f"行{row}数据异常：{e}，数据：{data}")
                continue

        # 恢复更新+刷新
        self.table.setUpdatesEnabled(True)
        self.table.update()

    # 查询出错提示
    def on_query_error(self, msg):
        QMessageBox.warning(self, "查询失败", msg)
        print(msg)

    def start_async_load(self):
        if self.query_thread and self.query_thread.isRunning():
            return
        self.table.setRowCount(0)
        self.findChild(QPushButton).setEnabled(False)  # 已修复

        self.query_thread = DbQueryThread("my_records", self.username)
        self.query_thread.records_ready.connect(self.on_records_loaded)
        self.query_thread.error_occurred.connect(self.on_query_error)
        self.query_thread.finished.connect(lambda: self.findChild(QPushButton).setEnabled(True))
        self.query_thread.start()


# ===================== 学生主窗口 =====================
class StudentMainWindow(QMainWindow):
    def __init__(self, username="学生"):
        super().__init__()
        self.username = username
        self.setGeometry(550, 200, 1000, 650)  # 稍微调整了默认尺寸，显得更紧凑
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setStyleSheet(get_global_style())
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        central.setStyleSheet(f"background:{COLOR_BACKGROUND}; border-radius:{WINDOW_ROUND_RADIUS}px;")
        self.setCentralWidget(central)

        # 最外层 VBox（包住标题栏和下方内容）
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        self.title_bar = CustomTitleBar(f"学生系统 - {self.username}", self)
        self.title_bar.logout_clicked.connect(self.on_logout)
        main_layout.addWidget(self.title_bar)

        # 分割线
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet(f"background:{COLOR_PRIMARY};")
        main_layout.addWidget(divider)

        # 下半部分：左侧导航 + 右侧内容
        content_layout = QHBoxLayout()

        # --- 左侧导航栏 ---
        nav_widget = QWidget()
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("background-color: #2c3e50; border-bottom-left-radius: 10px;")
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(15)

        self.btn_home = self.create_nav_button("📊 数据看板")
        self.btn_record = self.create_nav_button("📅 我的考勤")

        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_record)
        nav_layout.addStretch()  # 弹簧，把按钮顶上去

        # --- 右侧堆叠窗口 ---
        self.stack = QStackedWidget()
        self.home_page = StudentHomePage(self.username)
        self.record_page = StudentRecordPage(self.username)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.record_page)

        # 组装下半部分
        content_layout.addWidget(nav_widget)
        content_layout.addWidget(self.stack)
        main_layout.addLayout(content_layout)

        # 绑定按钮点击与页面切换
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_record.clicked.connect(lambda: self.switch_page(1))

        # 默认选中第一页（禁止自动刷新数据）
        self.stack.setCurrentIndex(0)
        self.btn_home.setChecked(True)

    def create_nav_button(self, text):
        """创建统一风格的导航按钮"""
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: #ecf0f1; 
                font-size: 15px;
                border-radius: 5px;
                text-align: left;
                padding-left: 15px;
            }}
            QPushButton:hover {{
                background: {COLOR_PRIMARY};
            }}
            QPushButton:checked {{
                background: {COLOR_PRIMARY};
                font-weight: bold;
            }}
        """)
        btn.setCheckable(True)
        return btn

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_home.setChecked(index == 0)
        self.btn_record.setChecked(index == 1)

        # 每次切换页面时，拉取最新数据
        if index == 0:
            self.home_page.refresh_stats()  # 保留，异步不卡



    # ==================== 退出登录 ====================
    def on_logout(self):
        res = QMessageBox.question(self, "退出登录", "确定要退出当前账号吗？", QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            from manager.window_manager import WindowManager
            WindowManager().show_login()

    # ==================== 完整窗口拖动 + 拉伸 + 最大化 ====================
    def mousePressEvent(self, event):
        self.resize_edge = self._get_resize_edge(event.pos())
        if self.resize_edge is not None:
            event.accept()
            return
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resize_edge is not None and event.buttons() == Qt.LeftButton:
            self._resize_window(event.globalPos())
            event.accept()
            return
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
        edge = self._get_resize_edge(event.pos())
        self._set_resize_cursor(edge)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'drag_pos'):
            del self.drag_pos
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)

    # 最大化切换（必须加！否则点了没反应）
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 边缘检测
    def _get_resize_edge(self, pos):
        rect = self.rect()
        em = 8
        if pos.x() < em and pos.y() < em:
            return "top_left"
        elif pos.x() > rect.width() - em and pos.y() < em:
            return "top_right"
        elif pos.x() < em and pos.y() > rect.height() - em:
            return "bottom_left"
        elif pos.x() > rect.width() - em and pos.y() > rect.height() - em:
            return "bottom_right"
        elif pos.x() < em:
            return "left"
        elif pos.x() > rect.width() - em:
            return "right"
        elif pos.y() < em:
            return "top"
        elif pos.y() > rect.height() - em:
            return "bottom"
        else:
            return None

    # 鼠标样式
    def _set_resize_cursor(self, edge):
        cursor_map = {
            "left": Qt.SizeHorCursor, "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor, "bottom": Qt.SizeVerCursor,
            "top_left": Qt.SizeFDiagCursor, "top_right": Qt.SizeBDiagCursor,
            "bottom_left": Qt.SizeBDiagCursor, "bottom_right": Qt.SizeFDiagCursor,
            None: Qt.ArrowCursor
        }
        self.setCursor(cursor_map[edge])

    # 窗口缩放
    def _resize_window(self, global_pos):
        geo = self.geometry()
        min_w = 600
        min_h = 400
        if self.resize_edge == "left":
            new_x = global_pos.x()
            if geo.right() - new_x >= min_w:
                geo.setLeft(new_x)
        elif self.resize_edge == "right":
            new_w = global_pos.x() - geo.left()
            if new_w >= min_w: geo.setWidth(new_w)
        elif self.resize_edge == "top":
            new_y = global_pos.y()
            if geo.bottom() - new_y >= min_h:
                geo.setTop(new_y)
        elif self.resize_edge == "bottom":
            new_h = global_pos.y() - geo.top()
            if new_h >= min_h: geo.setHeight(new_h)
        self.setGeometry(geo)

    #ui 重构部分
    def clean(self):
        # 学生端无相机，无需释放
        pass