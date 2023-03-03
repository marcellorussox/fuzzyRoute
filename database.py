import sqlite3


class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = 'CREATE TABLE ' + table_name + ' (' + ', '.join(columns) + ')'
        self.cursor.execute(query)
        self.conn.commit()

    def insert_row(self, table_name, values, columns=None):
        if columns:
            columns = ", ".join(["?"] * len(columns))
            placeholders = ", ".join(["?"] * len(values))
            query = 'INSERT INTO ' + table_name + ' (' + columns + ') VALUES (' + placeholders + ')'
        else:
            placeholders = ", ".join(["?"] * len(values))
            query = 'INSERT INTO ' + table_name + ' VALUES (' + placeholders + ')'
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        self.conn.close()
