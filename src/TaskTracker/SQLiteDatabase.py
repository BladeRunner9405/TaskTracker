import sqlite3


class SQLiteDatabase:
    """
    Класс, который устанавливает соединение с базой данных
    """
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, *columns):
        """
        Создает таблицу в базе данных.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, *data):
        """
        Вставляет данные в таблицу.
        """
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_data(self, table_name, key_column, key_value, keys, values, key_column2=None, key_value2=None):
        """
        Обновляет данные в строке, где значение в `key_column` равно `key_value`.
        """
        placeholders = ', '.join(f"{column}=?" for column in keys)
        query = f"UPDATE {table_name} SET {placeholders} WHERE {key_column}=?"
        if key_column2 is not None:
            query += f" AND {key_column2}=?"
        values = list(values) + [key_value]
        if key_value2 is not None:
            values += [key_value2]
        self.cursor.execute(query, values)
        self.conn.commit()

    def fetch_all(self, table_name, where_clause=None):
        """
        Возвращает все данные из таблицы.
        """
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, table_name, where_clause=None):
        """
        Возвращает одну строку из таблицы.
        """
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_column(self, table_name, column_name):
        """
                Возвращает один столбец из таблицы.
                """
        query = f"SELECT {column_name} FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_data(self, table_name, key_column, key_value, key_column2=None, key_value2=None):
        """
        Удаляет все строки из таблицы, где значение в `key_column` равно `key_value`.
        """
        query = f"DELETE FROM {table_name} WHERE {key_column}=?"
        values = [key_value]
        if key_column2 is not None:
            query += f" AND {key_column2}=?"
            values += [key_value2]
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()

