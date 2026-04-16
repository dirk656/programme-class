# ui/style1/ui_main.py
import sys
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
    QSizePolicy, QLineEdit, QMessageBox, QStackedWidget, QGroupBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QImage

# 导入拆分后的模块
from config.settings import (ICON_PATH, EDGE_MARGIN, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, WINDOW_ROUND_RADIUS,
                             COLOR_BACKGROUND, COLOR_TEXT_WHITE, COLOR_PRIMARY, FONT_SIZE_TITLE, COLOR_SECONDARY,
                             FONT_SIZE_BUTTON, COLOR_PRIMARY_LIGHT, FONT_MAIN, BUTTON_ROUND_RADIUS, FONT_SIZE_NORMAL)
from components.title_bar import CustomTitleBar
from core.camera_worker import CameraThread
from core.data_manager import DataManager
from manager.style_manager import get_global_style


# ===================== 页面1：签到页面（拆分原有UI） =====================
class CheckInPage(QWidget):
    # 定义切换到统计页面的信号
    switch_to_stat_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_thread = None
        self.parent_window = parent  # 保留对主窗口的引用（用于窗口操作）
        self.init_ui()

    def init_ui(self):
        # 主布局
        total_layout = QVBoxLayout(self)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_layout.setSpacing(0)

        # 2. 主内容布局（原有逻辑完全复用）
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 左侧：签到记录
        left_layout = QVBoxLayout()
        record_label = QLabel("签到记录")
        record_label.setStyleSheet(f"""
            font-size: {FONT_SIZE_TITLE}px; 
            font-weight: bold; 
            margin-bottom: 10px;
            color: {COLOR_TEXT_WHITE};
        """)
        left_layout.addWidget(record_label)

        # 创建三列表格并写好表头
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(3)
        self.record_table.setHorizontalHeaderLabels(["姓名", "签到时间", "状态"])
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.record_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 表格样式
        self.record_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: #333333;
                color: {COLOR_TEXT_WHITE};
                border-radius: 8px;
                border: none;
                gridline-color: #444444;
            }}
            QTableWidget::header {{
                background-color: #444444;
                color: {COLOR_TEXT_WHITE};
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {COLOR_SECONDARY};
            }}
        """)
        left_layout.addWidget(self.record_table)

        # 新增：历史统计按钮 + 清空按钮
        btn_group_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空记录")
        self.stat_btn = QPushButton("历史统计")  # 新增切换按钮
        btn_group_layout.addWidget(self.clear_btn)
        btn_group_layout.addWidget(self.stat_btn)
        left_layout.addLayout(btn_group_layout)

        # 右侧：摄像头 + 功能按钮
        right_layout = QVBoxLayout()
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setText("摄像头未启动")
        # 摄像头标签样式
        self.camera_label.setStyleSheet(f"""
            QLabel {{
                background-color: #111111;
                border-radius: 8px;
                border: 2px solid {COLOR_PRIMARY};
                color: {COLOR_TEXT_WHITE};
            }}
        """)
        right_layout.addWidget(self.camera_label)

        # 创建功能按钮区
        btn_layout = QHBoxLayout()
        # 学生登录账号（用于数据库绑定）
        self.student_username_input = QLineEdit()
        self.student_username_input.setPlaceholderText("输入学生登录账号（如：student1）")
        self.start_checkin_btn = QPushButton("开始签到")
        self.name_input = QLineEdit()  # 创建输入框
        self.name_input.setPlaceholderText("输入姓名（如：张三）")  # 设置输入框内容
        self.register_btn = QPushButton("录入人脸")
        self.stop_btn = QPushButton("停止")

        # 按钮大小适配
        self.start_checkin_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.register_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stop_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 按钮样式（复用原有）
        btn_style = f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_TEXT_WHITE};
                border-radius: {BUTTON_ROUND_RADIUS}px;
                font-size: {FONT_SIZE_BUTTON}px;
                font-family: {FONT_MAIN};
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_PRIMARY_LIGHT};
            }}
            QPushButton:disabled {{
                background-color: #666666;
            }}
        """
        self.start_checkin_btn.setStyleSheet(btn_style)
        self.register_btn.setStyleSheet(btn_style)
        self.stop_btn.setStyleSheet(btn_style)
        self.clear_btn.setStyleSheet(btn_style)
        self.stat_btn.setStyleSheet(btn_style)  # 新增按钮样式

        # 输入框样式
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #333333;
                color: {COLOR_TEXT_WHITE};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: {FONT_SIZE_NORMAL}px;
                border: 2px solid transparent;
            }}
            QLineEdit:focus {{
                border-color: {COLOR_PRIMARY};
            }}
        """)

        # 将输入框按顺序加入btn_layout
        btn_layout.addWidget(self.start_checkin_btn)
        btn_layout.addWidget(self.student_username_input)
        btn_layout.addWidget(self.name_input)
        btn_layout.addWidget(self.register_btn)
        btn_layout.addWidget(self.stop_btn)
        right_layout.addLayout(btn_layout)

        # 加入主布局
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 5)
        total_layout.addLayout(main_layout)

        # 绑定事件（原有+新增）
        self.start_checkin_btn.clicked.connect(self.start_checkin)
        self.stop_btn.clicked.connect(self.stop_camera)
        self.register_btn.clicked.connect(self.start_register)
        self.clear_btn.clicked.connect(self.clear_check_in_record)
        self.stat_btn.clicked.connect(self.emit_switch_stat_signal)  # 绑定切换信号

    # 发射切换到统计页面的信号
    def emit_switch_stat_signal(self):
        try:
            print("开始切换到统计页面...")
            self.switch_to_stat_signal.emit()
            print("切换信号发射成功")
        except Exception as e:
            print(f"切换统计页面出错：{e}")
            import traceback
            traceback.print_exc()  # 打印完整错误栈

    # 以下为原有功能逻辑，完全复用
    def update_camera_frame(self, frame):
        # frame 是 numpy 数组，转为 Qt 图像
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        # BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 注意：此处用 copy() 防止 C++ 层面的数据被 Python 垃圾回收导致崩溃或黑屏
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.camera_label.setPixmap(scaled_pixmap)

    def handle_recognize(self, name):
        if not name or name == "你是个嘚儿":
            return

        try:
            # 格式解析 统一放这里
            if "_" in name:
                real_name, student_username = name.split("_", 1)
            else:
                student_username = name
                real_name = name

            if not DataManager.check_duplicate_sign(student_username):
                DataManager.add_sign_record(
                    self.record_table, real_name, student_username=student_username
                )
                # ✅ 解耦：只调用 service，不直接调用 db
                from core.service import CheckInService
                CheckInService.save_sign_record(student_username, real_name)
        except Exception as e:
            print(f"[UI] 识别异常：{e}")

    def handle_register_done(self, name):
        QMessageBox.information(self, "录入成功", f"{name}的人脸数据已录入1张！\n可进行签到识别")
        self.stop_camera()
        self.start_checkin_btn.setEnabled(True)
        self.register_btn.setEnabled(True)

    def start_checkin(self):
        self.stop_camera()
        self.camera_thread = CameraThread(mode="checkin")
        self.camera_thread.frame_ready.connect(self.update_camera_frame)
        self.camera_thread.recognize_result.connect(self.handle_recognize)
        self.camera_thread.start()
        self.start_checkin_btn.setEnabled(False)
        self.register_btn.setEnabled(False)

    def start_register(self):
        username = self.student_username_input.text().strip()
        name = self.name_input.text().strip()

        if not username or not name:
            QMessageBox.warning(self, "提示", "请输入【学生账号】和【学生姓名】！")
            return

        save_name = f"{name}_{username}"

        self.stop_camera()
        self.camera_thread = CameraThread(mode="register", name=save_name)
        self.camera_thread.frame_ready.connect(self.update_camera_frame)
        self.camera_thread.register_done.connect(self.handle_register_done)
        self.camera_thread.start()

        self.start_checkin_btn.setEnabled(False)
        self.register_btn.setEnabled(False)

    def stop_camera(self):
        try:
            if self.camera_thread is not None:
                self.camera_thread.running = False
                self.camera_thread.wait(200)  # 超短等待
                self.camera_thread = None
        except:
            self.camera_thread = None

        self.start_checkin_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
        self.camera_label.setText("摄像头未启动")

    def clear_check_in_record(self):
        self.record_table.setRowCount(0)
        DataManager.clear_sign_records()


# ===================== 页面2：历史统计页面（绝对不崩溃版） =====================
class StatPage(QWidget):
    switch_to_checkin_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        total_layout = QVBoxLayout(self)
        total_layout.setContentsMargins(20, 20, 20, 20)
        total_layout.setSpacing(20)

        # 标题
        title_label = QLabel("历史签到记录")
        title_label.setStyleSheet("font-size:20px; color:white; font-weight:bold;")
        total_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # 表格（绝对安全）
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["账号", "姓名", "时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        total_layout.addWidget(self.table)

        # 按钮
        btn1 = QPushButton("刷新数据")
        btn2 = QPushButton("返回")
        btn1.clicked.connect(self.load_data)
        btn2.clicked.connect(self.switch_to_checkin_signal.emit)
        total_layout.addWidget(btn1)
        total_layout.addWidget(btn2)

    # 安全加载数据（绝不崩溃）
    def load_data(self):
        try:
            from core.service import CheckInService
            records = CheckInService.get_all_records()
            self.table.setRowCount(0)
            for row, one in enumerate(records):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(one[0]))
                self.table.setItem(row, 1, QTableWidgetItem(one[1]))
                self.table.setItem(row, 2, QTableWidgetItem(one[2]))
        except:
            pass

# ===================== 结束 =====================

# ===================== 主窗口（容器+页面切换） =====================
class FaceRecognitionCheckIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setGeometry(550, 200, 1400, 1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置图标
        self.setWindowIcon(QIcon(ICON_PATH))

        # 初始化变量
        self.resize_edge = None  # 窗口拉伸边缘标记

        # 设置全局样式
        self.setStyleSheet(get_global_style())

        # 初始化UI（重构后）
        self.init_ui()

    def init_ui(self):
        # 中心部件（圆角容器）
        central_widget = QWidget()
        central_widget.setObjectName("main_central_widget")
        central_widget.setStyleSheet(f"""
            QWidget#main_central_widget {{
                background-color: {COLOR_BACKGROUND} !important;
                border-radius: {WINDOW_ROUND_RADIUS}px !important;
                border: none !important;
            }}
        """)
        self.setCentralWidget(central_widget)

        # 主布局
        total_layout = QVBoxLayout(central_widget)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_layout.setSpacing(0)

        # 1. 自定义标题栏（保留）
        self.title_bar = CustomTitleBar("人脸识别签到系统", self)
        self.title_bar.logout_clicked.connect(self.on_logout)
        total_layout.addWidget(self.title_bar)

        #新增：标题栏与主内容区域间的分割线
        divider = QWidget()
        divider.setFixedHeight(2)  # 分割线高度
        divider.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};  /* 和摄像头边框同色 */
            margin: 0;
            padding: 0;
        """)
        total_layout.addWidget(divider)

        # 2. QStackedWidget：页面容器（核心！）
        self.stacked_widget = QStackedWidget()
        total_layout.addWidget(self.stacked_widget)

        # 3. 创建并添加两个页面
        self.checkin_page = CheckInPage(self)
        self.stat_page = StatPage(self)
        self.stacked_widget.addWidget(self.checkin_page)  # 索引0：签到页面
        self.stacked_widget.addWidget(self.stat_page)  # 索引1：统计页面

        # 4. 绑定页面切换信号
        self.checkin_page.switch_to_stat_signal.connect(self.switch_to_stat_page)
        self.stat_page.switch_to_checkin_signal.connect(self.switch_to_checkin_page)

        # 默认显示签到页面
        self.stacked_widget.setCurrentWidget(self.checkin_page)

    # 切换到统计页面
    def switch_to_stat_page(self):
        try:
            print("主窗口接收切换信号，准备显示统计页面")
            self.stacked_widget.setCurrentWidget(self.stat_page)
            # 👇 注释掉这一行，暂时不修改标题
            # self.title_bar.set_title("人脸识别签到系统 - 历史统计")
            print("统计页面显示成功")
        except Exception as e:
            print(f"主窗口切换页面出错：{e}")
            import traceback
            traceback.print_exc()

    # 切换回签到页面
    def switch_to_checkin_page(self):
        self.stacked_widget.setCurrentWidget(self.checkin_page)
        # 👇 注释掉这一行
        # self.title_bar.set_title("人脸识别签到系统")

    #退出登录跳转到初始登录界面
    def on_logout(self):
        res = QMessageBox.question(self, "退出登录", "确定要退出当前账号吗？")
        if res == QMessageBox.Yes:
            # 停止相机
            if hasattr(self.checkin_page, 'camera_thread'):
                try:
                    self.checkin_page.camera_thread.stop()
                    self.checkin_page.camera_thread.wait()
                except:
                    pass
            self.checkin_page.stop_camera()

            # 关键：调用全局管理器回到登录
            from manager.window_manager import WindowManager
            WindowManager().show_login()

    # ==================== 原有全局逻辑（完全保留） ====================
    # 窗口拖动 + 边缘检测
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

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _get_resize_edge(self, pos):
        rect = self.rect()
        if pos.x() < EDGE_MARGIN and pos.y() < EDGE_MARGIN:
            return "top_left"
        elif pos.x() > rect.width() - EDGE_MARGIN and pos.y() < EDGE_MARGIN:
            return "top_right"
        elif pos.x() < EDGE_MARGIN and pos.y() > rect.height() - EDGE_MARGIN:
            return "bottom_left"
        elif pos.x() > rect.width() - EDGE_MARGIN and pos.y() > rect.height() - EDGE_MARGIN:
            return "bottom_right"
        elif pos.x() < EDGE_MARGIN:
            return "left"
        elif pos.x() > rect.width() - EDGE_MARGIN:
            return "right"
        elif pos.y() < EDGE_MARGIN:
            return "top"
        elif pos.y() > rect.height() - EDGE_MARGIN:
            return "bottom"
        else:
            return None

    def _set_resize_cursor(self, edge):
        cursor_map = {
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "top_left": Qt.SizeFDiagCursor,
            "top_right": Qt.SizeBDiagCursor,
            "bottom_left": Qt.SizeBDiagCursor,
            "bottom_right": Qt.SizeFDiagCursor,
            None: Qt.ArrowCursor
        }
        self.setCursor(cursor_map[edge])

    def _resize_window(self, global_pos):
        current_geo = self.geometry()
        if self.resize_edge == "left":
            new_x = global_pos.x()
            new_width = current_geo.right() - new_x
            if new_width >= MIN_WINDOW_WIDTH:
                current_geo.setLeft(new_x)
        elif self.resize_edge == "right":
            new_width = global_pos.x() - current_geo.left()
            if new_width >= MIN_WINDOW_WIDTH:
                current_geo.setWidth(new_width)
        elif self.resize_edge == "top":
            new_y = global_pos.y()
            new_height = current_geo.bottom() - new_y
            if new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setTop(new_y)
        elif self.resize_edge == "bottom":
            new_height = global_pos.y() - current_geo.top()
            if new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setHeight(new_height)
        elif self.resize_edge == "top_left":
            new_x = global_pos.x()
            new_y = global_pos.y()
            new_width = current_geo.right() - new_x
            new_height = current_geo.bottom() - new_y
            if new_width >= MIN_WINDOW_WIDTH and new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setLeft(new_x)
                current_geo.setTop(new_y)
        elif self.resize_edge == "top_right":
            new_width = global_pos.x() - current_geo.left()
            new_y = global_pos.y()
            new_height = current_geo.bottom() - new_y
            if new_width >= MIN_WINDOW_WIDTH and new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setWidth(new_width)
                current_geo.setTop(new_y)
        elif self.resize_edge == "bottom_left":
            new_x = global_pos.x()
            new_width = current_geo.right() - new_x
            new_height = global_pos.y() - current_geo.top()
            if new_width >= MIN_WINDOW_WIDTH and new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setLeft(new_x)
                current_geo.setHeight(new_height)
        elif self.resize_edge == "bottom_right":
            new_width = global_pos.x() - current_geo.left()
            new_height = global_pos.y() - current_geo.top()
            if new_width >= MIN_WINDOW_WIDTH and new_height >= MIN_WINDOW_HEIGHT:
                current_geo.setWidth(new_width)
                current_geo.setHeight(new_height)
        self.setGeometry(current_geo)

    # 关闭窗口处理（新增：停止摄像头）
    def closeEvent(self, event):
        self.checkin_page.stop_camera()  # 停止签到页面的摄像头
        event.accept()

    def clean(self):
        try:
            # 真正杀死线程，不等待、不卡死、不留痕迹
            self.checkin_page.stop_camera()
            if hasattr(self.checkin_page, 'camera_thread'):
                self.checkin_page.camera_thread = None
        except:
            pass

# 测试入口（保留）
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionCheckIn()
    window.show()
    sys.exit(app.exec_())