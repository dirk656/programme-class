# core/db_manager.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student'
    )''')

    # 👇 只加这一段
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sign_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        sign_time TEXT NOT NULL
    )''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?)", (1,"admin","123456","teacher"))
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?)", (2,"student1","123456","student"))
    conn.commit()
    conn.close()

def add_user(username, password, role="student"):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                      (username, password, role))
        conn.commit()
        conn.close()
        return True, "注册成功"
    except sqlite3.IntegrityError:
        return False, "用户名已存在"


# ================== 【密码重置/删除函数】 ==================
def reset_password(username, new_password):
    """
    重置用户密码（删除旧密码，设置新密码）
    :param username: 要重置的用户名
    :param new_password: 新密码
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # 直接更新密码（相当于删除旧密码，设置新密码）
        cursor.execute("""
            UPDATE users 
            SET password = ? 
            WHERE username = ?
        """, (new_password, username))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            print(f"✅ 用户【{username}】密码已重置为：{new_password}")
        else:
            print(f"❌ 未找到用户：{username}")

    except Exception as e:
        print(f"❌ 重置失败：{e}")


# ================== 【删除用户函数】 ==================
def delete_user(username):
    """删除用户（整个账号都删掉）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print(f"🗑️ 用户【{username}】已删除")

def add_sign_record(username, name):
    """保存一条签到记录到数据库"""
    try:
        from datetime import datetime
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO sign_records (username, name, sign_time)
            VALUES (?, ?, ?)
        """, (username, name, now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("签到记录保存失败：", e)
        return False

def get_all_sign_records():
    """老师：查询所有签到记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, name, sign_time 
        FROM sign_records 
        ORDER BY sign_time DESC
    """)
    records = cursor.fetchall()
    conn.close()
    return records

def get_my_sign_records(username):
    """学生：查询自己的签到记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 删掉 SQL 里的 # 注释！！！
    cursor.execute("""
        SELECT username, name, sign_time 
        FROM sign_records 
        WHERE username = ?
        ORDER BY sign_time DESC
    """, (username,))
    records = cursor.fetchall()
    conn.close()
    return records

# ================== 【查看所有用户】 ==================
def show_all_users():
    """打印数据库里所有的 用户名、密码、角色"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role FROM users")
    users = cursor.fetchall()

    print("\n" + "=" * 50)
    print("📋 数据库中所有用户信息")
    print("=" * 50)
    for username, password, role in users:
        print(f"用户名：{username:10} | 密码：{password:12} | 角色：{role}")
    print("=" * 50 + "\n")

    conn.close()


if __name__ == "__main__":
    init_db()
    show_all_users()
    # reset_password("admin", "123456")
    # delete_user("student1")