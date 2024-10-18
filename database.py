# database.py
import sqlite3
import config

class Database:
    def __init__(self, db_name=config.DATABASE_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name):
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            timestamp INTEGER PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL
        );
        """
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        insert_query = f"INSERT OR IGNORE INTO {table_name} (timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(insert_query, data)
        self.conn.commit()

    def fetch_data(self, table_name):
        fetch_query = f"SELECT * FROM {table_name} ORDER BY timestamp ASC"
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
