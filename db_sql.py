import sqlite3

connection = sqlite3.connect('accounts.db')

c = connection.cursor()

class CustomerTableCommands():
    def __init__(self, user) -> None:
        self.user = user
    
    def create_table():
        c.execute("""CREATE TABLE customer (
                    customer_id int,
                    first_name text,
                    last_name text,
                    address text,
                    phone_num text,
                    email text,
                    username text,
                    password text
                )""")
        
    def insert_values():
        c.execute("INSERT INTO customer VALUES()")



connection.commit()



connection.close() 