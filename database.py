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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_record(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO history (price, discounts, tax, final_price, saved) VALUES (?, ?, ?, ?, ?)",
            (data["price"], data["discounts"], data["tax"], data["final_price"], data["saved"])
        )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        return cursor.fetchall()

    def update_record(self, record_id, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE history SET price=?, discounts=?, tax=?, final_price=?, saved=? WHERE id=?",
            (data["price"], data["discounts"], data["tax"], data["final_price"], data["saved"], record_id)
        )
        self.conn.commit()

    def delete_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()