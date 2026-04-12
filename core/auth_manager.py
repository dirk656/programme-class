# core/auth_manager.py
from .db_manager import DB_PATH
import sqlite3


class AuthManager:
    @staticmethod
    def validate_login(username: str, password: str):
        """
        从数据库验证登录
        返回: (success: bool, message: str, role: str)
        """
        if not username or not password:
            return False, "用户名或密码不能为空！", ""

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT role FROM users WHERE username = ? AND password = ?
        """, (username, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            return True, f"欢迎回来，{username}！", role
        else:
            return False, "用户名或密码错误！", ""

