from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from src.login.manager.window_manager import WindowManager

from src.login.ui.factory.factory import UIFactory

import traceback


# ===================== 线程 =====================
class DbQueryThread(QThread):
    records_ready = pyqtSignal(list)
    stats_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, query_type, username=None, parent=None):
        super().__init__(parent)
        self.query_type = query_type
        self.username = username

    def run(self):
        try:
            from src.login.core.service import CheckInService, StudentService
            if self.query_type == "my_records":
                records = CheckInService.get_my_records(self.username)
                self.records_ready.emit(records)
            elif self.query_type == "my_stats":
                stat = StudentService.get_student_stat(self.username)
                self.stats_ready.emit(stat)
        except Exception as e:
            self.error_occurred.emit(f"错误：{e}")


# ===================== 首页逻辑（无任何UI代码） =====================
class StudentHomePage(QWidget):
    def __init__(self, username, render_ui, parent=None):
        super().__init__(parent)
        self.username = username
        self.ui = render_ui  # UI 完全由外部注入
        self.query_thread = None

        # 布局绑定
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)

        self.ui.welcome_label.setText(f"欢迎回来，{username}！")

    def refresh_stats(self):
        if self.query_thread and self.query_thread.isRunning():
            self.query_thread.terminate()
            self.query_thread.wait()

        self.query_thread = DbQueryThread("my_stats", self.username, self)
        self.query_thread.stats_ready.connect(self.on_load)
        self.query_thread.error_occurred.connect(self.on_err)
        self.query_thread.start()

    def on_load(self, stat):
        self.ui.card_total.findChild(QtWidgets.QLabel, "card_value").setText(f"{stat.get('total',0)}次")
        self.ui.card_missed.findChild(QtWidgets.QLabel, "card_value").setText(f"{stat.get('missed',0)}次")
        self.ui.card_rate.findChild(QtWidgets.QLabel, "card_value").setText(stat.get('rate','0%'))

    def on_err(self, msg):
        QMessageBox.warning(self, "错误", msg)


# ===================== 记录页逻辑（无任何UI代码） =====================
class StudentRecordPage(QWidget):
    def __init__(self, username, render_ui, parent=None):
        super().__init__(parent)
        self.username = username
        self.ui = render_ui
        self.query_thread = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)

        self.ui.refresh_btn.clicked.connect(self.refresh)

    def refresh(self):
        if self.query_thread and self.query_thread.isRunning():
            return

        self.ui.table.setRowCount(0)
        self.ui.refresh_btn.setEnabled(False)
        self.query_thread = DbQueryThread("my_records", self.username, self)
        self.query_thread.records_ready.connect(self.on_load)
        self.query_thread.error_occurred.connect(self.on_err)
        self.query_thread.finished.connect(lambda: self.ui.refresh_btn.setEnabled(True))
        self.query_thread.start()

    def on_load(self, records):
        tbl = self.ui.table
        tbl.setUpdatesEnabled(False)
        tbl.setRowCount(len(records))
        for row, (user, real_name, t) in enumerate(records):
            date_str, time_str = (t.split() + [""])[:2]
            tbl.setItem(row,0, QTableWidgetItem(date_str))
            tbl.setItem(row,1, QTableWidgetItem(time_str))
            item = QTableWidgetItem("正常")
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(Qt.green)
            tbl.setItem(row,2, item)
        tbl.setUpdatesEnabled(True)

    def on_err(self, msg):
        QMessageBox.warning(self, "错误", msg)


# ===================== 主窗口（纯逻辑 + 支持皮肤切换） =====================
class StudentMainWindow(QMainWindow):
    # 👉 增加 render_class，支持工厂切换
    def __init__(self, username="学生", render_class=None):
        super().__init__()
        self.username = username
        self.resize_edge = None

        self.setGeometry(550,200,1000,650)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ========== 从工厂获取渲染器（支持切换 style1/style2） ==========
        if render_class is None:
            render_class = UIFactory.get_student_render()
        
        self.render = render_class(self)
        self.render.build_ui()

        # ========== UI由渲染器创建，逻辑只负责绑定 ==========
        home_ui = self.render.create_home_page_ui(self)
        record_ui = self.render.create_record_page_ui(self)

        self.home_page = StudentHomePage(username, home_ui)
        self.record_page = StudentRecordPage(username, record_ui)

        self.render.add_page(self.home_page)
        self.render.add_page(self.record_page)

        self._bind_events()
        self.render.stack.setCurrentIndex(0)
        self.render.btn_home.setChecked(True)

    def _bind_events(self):
        self.render.title_bar.logout_clicked.connect(self.logout)
        self.render.btn_home.clicked.connect(lambda: self.switch(0))
        self.render.btn_record.clicked.connect(lambda: self.switch(1))

    def switch(self, idx):
        self.render.stack.setCurrentIndex(idx)
        self.render.btn_home.setChecked(idx == 0)
        self.render.btn_record.setChecked(idx == 1)
        if idx == 0:
            self.home_page.refresh_stats()

    def logout(self):
        if QMessageBox.question(self,"退出","确定退出？") == QMessageBox.Yes:
            WindowManager().show_login()

    def clean(self):
        pass


    # ==================== 以下是窗口拖动逻辑 ====================
    def mousePressEvent(self, event):
        self.resize_edge = self._get_resize_edge(event.pos())
        if self.resize_edge: event.accept(); return
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resize_edge and event.buttons() == Qt.LeftButton:
            self._resize(event.globalPos())
            event.accept()
            return
        if event.buttons() == Qt.LeftButton and hasattr(self,'drag_pos'):
            self.move(event.globalPos()-self.drag_pos)
            event.accept()
        self._set_cursor(self._get_resize_edge(event.pos()))

    def mouseReleaseEvent(self, event):
        if hasattr(self,'drag_pos'): delattr(self,'drag_pos')
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)

    def toggle_maximize(self):
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def _get_resize_edge(self,pos):
        r = self.rect()
        d=8
        if pos.x()<d and pos.y()<d: return "top_left"
        if pos.x()>r.width()-d and pos.y()<d: return "top_right"
        if pos.x()<d and pos.y()>r.height()-d: return "bottom_left"
        if pos.x()>r.width()-d and pos.y()>r.height()-d: return "bottom_right"
        if pos.x()<d: return "left"
        if pos.x()>r.width()-d: return "right"
        if pos.y()<d: return "top"
        if pos.y()>r.height()-d: return "bottom"
        return None

    def _set_cursor(self,edge):
        curs = {
            "left":Qt.SizeHorCursor,"right":Qt.SizeHorCursor,
            "top":Qt.SizeVerCursor,"bottom":Qt.SizeVerCursor,
            "top_left":Qt.SizeFDiagCursor,"top_right":Qt.SizeBDiagCursor,
            "bottom_left":Qt.SizeBDiagCursor,"bottom_right":Qt.SizeFDiagCursor,
        }
        self.setCursor(curs.get(edge, Qt.ArrowCursor))

    def _resize(self,gpos):
        geo = self.geometry()
        mw,mh=600,400
        if self.resize_edge=="left":
            nx = gpos.x()
            if geo.right()-nx >= mw: geo.setLeft(nx)
        elif self.resize_edge=="right":
            nw = gpos.x()-geo.left()
            if nw>=mw: geo.setWidth(nw)
        elif self.resize_edge=="top":
            ny = gpos.y()
            if geo.bottom()-ny >= mh: geo.setTop(ny)
        elif self.resize_edge=="bottom":
            nh = gpos.y()-geo.top()
            if nh>=mh: geo.setHeight(nh)
        self.setGeometry(geo)