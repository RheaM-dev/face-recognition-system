import sqlite3
from user import Userinfo
from datetime import datetime


class FaceDatabase:
    def __init__(self, db_name="face_database.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                roll_no text UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date text NOT NULL,
                time text NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    # ---------------------------------------- USERS ---------------------------------------------------

    def add_user(self, user):
        conn = self.connect()

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, roll_no) VALUES (?, ?)",
                (user.name, user.roll_no)
            )
            conn.commit()
            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            return None
        
        finally:
            conn.close()

    def get_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT id, name, roll_no 
            FROM users WHERE id = ?''',
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return Userinfo(row[1], row[2], row[0])

    def get_all_users(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, roll_no FROM users")
        rows = cursor.fetchall()
        conn.close()

        users = []
        for row in rows:
            users.append(Userinfo(row[1], row[2], row[0]))
        return users

    def delete_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM attendance WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

        conn.commit()
        conn.close()

    # --------------------------------------- ATTENDANCE ---------------------------------------------------

    def mark_attendance(self, user_id):
        """Returns True if marked now, False if already marked today."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        clock = now.strftime("%H:%M:%S")

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM attendance WHERE user_id = ? AND date = ?",
            (user_id, today)
        )
        already_marked = cursor.fetchone()

        if already_marked:
            conn.close()
            return False

        cursor.execute(
            "INSERT INTO attendance (user_id, date, time) VALUES (?, ?, ?)",
            (user_id, today, clock)
        )
        conn.commit()
        conn.close()
        return True
    

    def get_attendance(self):
        """Return rows of (name, roll_no, date, time), newest first."""

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT users.name, users.roll_no, attendance.date, attendance.time
            FROM attendance
            JOIN users ON attendance.user_id = users.id
            ORDER BY attendance.date DESC, attendance.time DESC
        ''')

        
        rows = cursor.fetchall()
        conn.close()
        return rows
