import sqlite3


class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_row(self, table_name, values, columns=None):
        if columns:
            placeholders = ", ".join(["?"] * len(values))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        else:
            placeholders = ", ".join(["?"] * len(values))
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
