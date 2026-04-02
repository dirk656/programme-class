from core.db_manager import (
    add_sign_record,
    get_all_sign_records,
    get_my_sign_records
)


class CheckInService:
    """签到相关业务服务层"""

    @staticmethod
    def save_sign_record(username: str, real_name: str) -> bool:
        """
        保存签到记录（UI 只调用这个，不碰 DB）
        :return: 成功返回 True，失败返回 False
        """
        try:
            add_sign_record(username, real_name)
            return True
        except Exception as e:
            print(f"[CheckInService] 保存签到记录失败：{str(e)}")
            return False

    @staticmethod
    def get_all_records() -> list:
        """获取所有签到记录"""
        try:
            return get_all_sign_records()
        except Exception as e:
            print(f"[CheckInService] 获取全部记录失败：{str(e)}")
            return []

    @staticmethod
    def get_my_records(username: str) -> list:
        """获取个人签到记录"""
        try:
            return get_my_sign_records(username)
        except Exception as e:
            print(f"[CheckInService] 获取个人记录失败：{str(e)}")
            return []


class StudentService:
    """学生统计业务服务层"""

    @staticmethod
    def get_student_stat(username: str) -> dict:
        """
        获取学生签到统计
        :return: { total: 总数, missed: 缺勤次数, rate: 签到率 }
        """
        try:
            records = get_my_sign_records(username)
            total = len(records)
            # 假设所有记录都是正常签到，缺勤次数暂时设为 0
            missed = 0
            rate = 100.0 if total > 0 else 0.0

            return {
                "total": total,
                "missed": missed,
                "rate": f"{rate}%"
            }
        except Exception as e:
            print(f"[StudentService] 获取统计数据失败：{str(e)}")
            return {
                "total": 0,
                "missed": 0,
                "rate": "0%"
            }