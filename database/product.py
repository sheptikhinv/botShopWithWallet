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

    @staticmethod
    def get_active_products():
        products = []
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM products WHERE status = 'active'"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            for product in result:
                products.append(Product(title=product[0], description=product[1], amount=product[2], price=product[3],
                                        currency_code=product[4], created_by=product[5], status=product[6],
                                        link=product[7],
                                        file_id=product[8]))

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            return products

    @staticmethod
    def get_all_products():
        products = []
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM products"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            for product in result:
                products.append(Product(title=product[0], description=product[1], amount=product[2], price=product[3],
                                        currency_code=product[4], created_by=product[5], status=product[6],
                                        link=product[7],
                                        file_id=product[8]))

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            return products

    @staticmethod
    def get_by_link(link: str):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM products WHERE link = ?"
            data = (link,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                if result is not None:
                    return Product(title=result[0], description=result[1], amount=result[2], price=result[3],
                                   currency_code=result[4], created_by=result[5], status=result[6], link=result[7],
                                   file_id=result[8])
            return None

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

    def change_cell(self, column: str, new_value):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = f"UPDATE products SET {column} = ? WHERE link = ?"
            data = (new_value, self.link)

            cursor.execute(query, data)
            db_connection.commit()

            query = "SELECT * FROM products WHERE link = ?"
            data = (self.link,)

            cursor.execute(query, data)
            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return Product(title=result[0], description=result[1], amount=result[2], price=result[3],
                               currency_code=result[4], created_by=result[5], status=result[6], link=result[7],
                               file_id=result[8])
            return None

    def change_status(self):
        if self.status == "active":
            self.change_cell("status", "inactive")
            self.status = "inactive"
        else:
            self.change_cell("status", "active")
            self.status = "active"
        return True
