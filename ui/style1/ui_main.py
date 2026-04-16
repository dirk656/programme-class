import sys
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QWidget, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

from core.camera_worker import CameraThread
from core.data_manager import DataManager

# 👉 只从工厂导入，不再写死 style1
from ui.factory.factory import UIFactory


class CheckInPage(QWidget):
    switch_to_stat_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_thread = None
        self.parent_window = parent

    # 所有控件通过 self.parent().render 访问
    @property
    def ui(self):
        return self.parent().render

    def bind_all_events(self):
        ui = self.ui
        ui.start_checkin_btn.clicked.connect(self.start_checkin)
        ui.stop_btn.clicked.connect(self.stop_camera)
        ui.register_btn.clicked.connect(self.start_register)
        ui.clear_btn.clicked.connect(self.clear_check_in_record)
        ui.stat_btn.clicked.connect(self.emit_switch_stat_signal)

    def emit_switch_stat_signal(self):
        self.switch_to_stat_signal.emit()

    def update_camera_frame(self, frame):
        ui = self.ui
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(ui.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ui.camera_label.setPixmap(scaled_pixmap)

    def handle_recognize(self, name):
        ui = self.ui
        if not name or name == "你是个嘚儿": return
        try:
            if "_" in name:
                student_username, real_name = name.split("_",1)
            else:
                student_username = name
                real_name = name
            if not DataManager.check_duplicate_sign(student_username):
                DataManager.add_sign_record(ui.record_table, real_name, student_username=student_username)
                from core.service import CheckInService
                CheckInService.save_sign_record(student_username, real_name)
        except: pass

    def handle_register_done(self, name):
        ui = self.ui
        QMessageBox.information(self, "录入成功", f"{name} 人脸录入完成！")
        self.stop_camera()
        ui.start_checkin_btn.setEnabled(True)
        ui.register_btn.setEnabled(True)

    def start_checkin(self):
        ui = self.ui
        self.stop_camera()
        self.camera_thread = CameraThread(mode="checkin")
        self.camera_thread.frame_ready.connect(self.update_camera_frame)
        self.camera_thread.recognize_result.connect(self.handle_recognize)
        self.camera_thread.start()
        ui.start_checkin_btn.setEnabled(False)
        ui.register_btn.setEnabled(False)

    def start_register(self):
        ui = self.ui
        username = ui.student_username_input.text().strip()
        name = ui.name_input.text().strip()
        if not username or not name:
            QMessageBox.warning(self, "提示", "请输入账号和姓名！")
            return
        save_name = f"{username}_{name}"
        self.stop_camera()
        self.camera_thread = CameraThread(mode="register", name=save_name)
        self.camera_thread.frame_ready.connect(self.update_camera_frame)
        self.camera_thread.register_done.connect(self.handle_register_done)
        self.camera_thread.start()
        ui.start_checkin_btn.setEnabled(False)
        ui.register_btn.setEnabled(False)

    def stop_camera(self):
        ui = self.ui
        try:
            if self.camera_thread:
                self.camera_thread.running = False
                self.camera_thread.wait(200)
                self.camera_thread = None
        except:
            self.camera_thread = None
        ui.start_checkin_btn.setEnabled(True)
        ui.register_btn.setEnabled(True)
        ui.camera_label.setText("摄像头未启动")

    def clear_check_in_record(self):
        ui = self.ui
        ui.record_table.setRowCount(0)
        DataManager.clear_sign_records()


# ===================== 统计页面（纯逻辑，仅接收 parent） =====================
class StatPage(QWidget):
    switch_to_checkin_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def ui(self):
        return self.parent().render

    def bind_all_events(self):
        ui = self.ui
        ui.refresh_btn.clicked.connect(self.load_data)
        ui.back_btn.clicked.connect(self.switch_to_checkin_signal.emit)

    def load_data(self):
        ui = self.ui
        try:
            from core.service import CheckInService
            records = CheckInService.get_all_records()
            ui.table.setRowCount(0)
            for row, one in enumerate(records):
                ui.table.insertRow(row)
                ui.table.setItem(row,0, QTableWidgetItem(str(one[0])))
                ui.table.setItem(row,1, QTableWidgetItem(str(one[1])))
                ui.table.setItem(row,2, QTableWidgetItem(str(one[2])))
        except: pass


# ===================== 主窗口（已支持皮肤切换） =====================
class FaceRecognitionCheckIn(QMainWindow):
    # 👉 增加 render_class 参数，支持工厂切换皮肤
    def __init__(self, render_class=None):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setGeometry(550,200,1400,1000)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize_edge = None

        # ========== 核心：从工厂自动获取当前皮肤 ==========
        if render_class is None:
            render_class = UIFactory.get_main_render()
        
        # 👉 使用动态渲染器
        self.render = render_class(self)
        self.render.build_ui()

        # 创建页面（只传 parent，不多传参数）
        self.checkin_page = CheckInPage(self)
        self.stat_page = StatPage(self)

        self.render.add_checkin_page(self.checkin_page)
        self.render.add_stat_page(self.stat_page)

        # 绑定逻辑事件
        self.checkin_page.bind_all_events()
        self.stat_page.bind_all_events()

        self._bind_events()
        self.render.switch_to_page(0)

    def _bind_events(self):
        self.render.title_bar.logout_clicked.connect(self.on_logout)
        self.checkin_page.switch_to_stat_signal.connect(lambda: self.render.switch_to_page(1))
        self.stat_page.switch_to_checkin_signal.connect(lambda: self.render.switch_to_page(0))

    def on_logout(self):
        if QMessageBox.question(self,"退出登录","确定退出？") == QMessageBox.Yes:
            self.checkin_page.stop_camera()
            from manager.window_manager import WindowManager
            WindowManager().show_login()

    def clean(self):
        try:
            self.checkin_page.stop_camera()
        except: pass

    def mousePressEvent(self, event):
        self.resize_edge = self._get_resize_edge(event.pos())
        if self.resize_edge: event.accept(); return
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resize_edge and event.buttons() == Qt.LeftButton:
            self._resize_window(event.globalPos())
            event.accept()
            return
        if event.buttons() == Qt.LeftButton and hasattr(self,'drag_pos'):
            self.move(event.globalPos()-self.drag_pos)
            event.accept()
        self._set_resize_cursor(self._get_resize_edge(event.pos()))

    def mouseReleaseEvent(self, event):
        if hasattr(self,'drag_pos'): delattr(self,'drag_pos')
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)

    def toggle_maximize(self):
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def _get_resize_edge(self, pos):
        r = self.rect()
        d = 8
        if pos.x()<d and pos.y()<d: return "top_left"
        if pos.x()>r.width()-d and pos.y()<d: return "top_right"
        if pos.x()<d and pos.y()>r.height()-d: return "bottom_left"
        if pos.x()>r.width()-d and pos.y()>r.height()-d: return "bottom_right"
        if pos.x()<d: return "left"
        if pos.x()>r.width()-d: return "right"
        if pos.y()<d: return "top"
        if pos.y()>r.height()-d: return "bottom"
        return None

    def _set_resize_cursor(self, edge):
        curs = {
            "left":Qt.SizeHorCursor,"right":Qt.SizeHorCursor,
            "top":Qt.SizeVerCursor,"bottom":Qt.SizeVerCursor,
            "top_left":Qt.SizeFDiagCursor,"top_right":Qt.SizeBDiagCursor,
            "bottom_left":Qt.SizeBDiagCursor,"bottom_right":Qt.SizeFDiagCursor,
        }
        self.setCursor(curs.get(edge, Qt.ArrowCursor))

    def _resize_window(self, gpos):
        geo = self.geometry()
        mw, mh = 800, 600
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

    def closeEvent(self, event):
        self.clean()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FaceRecognitionCheckIn()
    w.show()
    sys.exit(app.exec_())