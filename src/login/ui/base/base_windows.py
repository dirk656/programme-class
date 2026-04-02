# ui/base/base_windows.py
from PyQt5.QtCore import QObject, pyqtSignal

class BaseLoginWindow(QObject):
    login_success = pyqtSignal(str, str)
    def show(self): pass
    def close(self): pass
    def clean(self): pass

class BaseMainWindow(QObject):
    def show(self): pass
    def close(self): pass
    def clean(self): pass

class BaseStudentWindow(QObject):
    def show(self): pass
    def close(self): pass
    def clean(self): pass