# core/data_manager.py
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem

# 防重复签到集合
SIGNED_RECORDS = set()
# 【新增】用来临时存储所有签到数据的列表，方便学生端查询
ALL_RECORDS = []

class DataManager:
    @staticmethod
    def check_duplicate_sign(name):
        """检查是否重复签到（按姓名+日期）"""
        key = f"{name}_{datetime.now().strftime('%Y-%m-%d')}" #精确到日防止重复签到
        if key in SIGNED_RECORDS:
            return True
        SIGNED_RECORDS.add(key)
        return False

    @staticmethod
    def clear_sign_records():
        """清空签到记录"""
        SIGNED_RECORDS.clear()
        ALL_RECORDS.clear() # 【新增】同步清空列表

    @staticmethod
    def add_sign_record(table_widget, name, status="正常", student_username=None):
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        full_time_str = f"{date_str} {time_str}"

        # 兼容：没传账号就用姓名当账号
        if not student_username:
            student_username = name

        ALL_RECORDS.append({
            "name": name,
            "username": student_username,  # 👈 保存账号
            "date": date_str,
            "time": time_str,
            "status": status
        })

        # 下面 UI 逻辑完全不动

        # 保留你原本的 UI 表格插入逻辑（如果有 table_widget 传进来）
        if table_widget:
            row = table_widget.rowCount()
            table_widget.insertRow(row)
            table_widget.setItem(row, 0, QTableWidgetItem(name))
            table_widget.setItem(row, 1, QTableWidgetItem(full_time_str))
            table_widget.setItem(row, 2, QTableWidgetItem(status))

    # 【新增】专门给学生端用的查询接口
    @staticmethod
    def get_student_records(name):
        """根据姓名过滤出该学生的所有签到记录"""
        return [record for record in ALL_RECORDS if record["name"] == name]