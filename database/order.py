import sqlite3


class Order:
    def __init__(self, external_id: str, order_id: str, title: str, product_link: str, user_id: int, price: int,
                 currency_code: str, status: str):
        pass
        self.external_id = external_id
        self.order_id = order_id
        self.title = title
        self.product_link = product_link
        self.user_id = user_id
        self.price = price
        self.currency_code = currency_code
        self.status = status

    @staticmethod
    def get_by_order_id(order_id: str):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM orders WHERE order_id = ?"
            data = (order_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result:
                return Order(external_id=result[0], order_id=result[1], title=result[2], product_link=result[3],
                             user_id=result[4], price=result[5], currency_code=result[6], status=result[7])
            return None


    def add_to_database(self):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "INSERT INTO orders (external_id, order_id, title, product_link, user_id, price, currency_code, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            data = (self.external_id, self.order_id, self.title, self.product_link, self.user_id, self.price,
                    self.currency_code, self.status)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()

    def change_cell(self, column, new_value):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = f"UPDATE orders SET {column} = ? WHERE external_id = ?"
            data = (new_value, self.external_id)

            cursor.execute(query, data)
            db_connection.commit()

            query = "SELECT * FROM orders WHERE external_id = ?"
            data = (self.external_id,)

            cursor.execute(query, data)
            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result:
                return Order(external_id=result[0], order_id=result[1], title=result[2], product_link=result[3],
                             user_id=result[4], price=result[5], currency_code=result[6], status=result[7])
            return None
