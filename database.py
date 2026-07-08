import sqlite3

DB_FILE = "discounts.db"


class DatabaseManager:

    def __init__(self):
        self.conn = None

    def init_db(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL NOT NULL,
                discounts TEXT,
                tax REAL,
                final_price REAL,
                saved REAL,
                image_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_record(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO history "
                "(price, discounts, tax, final_price, saved, image_path) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    data["price"],
                    data["discounts"],
                    data["tax"],
                    data["final_price"],
                    data["saved"],
                    data["image_path"],
                )
            )
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        return cursor.fetchall()

    def update_record(self, record_id, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE history SET price=?, discounts=?, tax=?, "
                "final_price=?, saved=?, image_path=? WHERE id=?",
                (
                    data["price"],
                    data["discounts"],
                    data["tax"],
                    data["final_price"],
                    data["saved"],
                    data["image_path"],
                    record_id,
                )
            )
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

    def delete_record(self, record_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

    def close(self):
        if self.conn:
            self.conn.close()