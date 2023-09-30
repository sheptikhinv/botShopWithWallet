import sqlite3


class Product:
    def __init__(self, title: str, description: str, amount: int, price: int, currency_code: str, created_by: int,
                 status: str, link: str, file_id: str = None):
        self.title = title
        self.description = description
        self.amount = amount
        self.price = price
        self.currency_code = currency_code
        self.file_id = file_id
        self.created_by = created_by
        self.status = status
        self.link = link

    def add_to_database(self) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "INSERT INTO products (title, description, amount, price, currency_code, created_by, status, link, file_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            data = (
                self.title, self.description, self.amount, self.price, self.currency_code, self.created_by, self.status,
                self.link, self.file_id)

            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return True
            return False

    def change_cell(self, column: str, new_value: str | int):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "UPDATE products SET ? = ? WHERE link = ?"
            data = (column, new_value, self.link)

            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                ## TODO: ПОДУМАТЬ КАК ВЕРНУТЬ ОБНОВЛЕННЫЙ ОБЪЕКТ
                return
            return
