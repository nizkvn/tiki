from bs4 import BeautifulSoup
import requests
import sqlite3

TIKI = "https://tiki.vn/"

conn = sqlite3.connect('tiki.db')
cur = conn.cursor()

def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INT, 
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        conn = sqlite3.connect('tiki.db')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def create_product_table():
    query = """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INT,
            product_id TEXT, 
            price TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        conn = sqlite3.connect('tiki.db')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def select_all(name):
    return cur.execute(f'SELECT * FROM {name};').fetchall()

def delete_all(name):
    return cur.execute(f'DELETE FROM {name};')


class Category:
    def __init__(self, cat_id, name, url, parent_id):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Parent_id: {}".format(self.cat_id, self.name, self.url, self.parent_id)

    def save_into_db(self):
        query = """
            INSERT INTO categories (name, url, parent_id)
            VALUES (?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id)
        try:
            conn = sqlite3.connect('tiki.db')
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
        except Exception as err:
            print('ERROR BY INSERT:', err)

class Product:
    def __init__(self, cat_id, name, url, parent_id, product_id, price):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id
        self.product_id = product_id
        self.price = price

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Parent_id: {}, Product_id: {},Price: {}".format(self.cat_id, self.name, self.url, self.parent_id, self.product_id, self.price)

    def save_into_db(self):
        query = """
            INSERT INTO product (name, url, parent_id, product_id, price)
            VALUES (?, ?, ?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id, self.product_id, self.price)
        try:
            conn = sqlite3.connect('tiki.db')
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
        except Exception as err:
            print('ERROR BY INSERT:', err)

# create_categories_table()
# create_product_table()

# a = Product(1,"ggg","dfdfd",12,"12252","2222")
# a.save_into_db()
# print(select_all('product'))