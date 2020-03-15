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
        cur.execute(query)
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
            category TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def select_all(name):
    a = cur.execute(f'SELECT * FROM {name};').fetchall()
    return a

def delete_all(name):
    a = cur.execute(f'DELETE FROM {name};')
    return a



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
            cur.execute(query,val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

class Product:
    def __init__(self, cat_id, name, url, parent_id, product_id, price, category_name):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id
        self.product_id = product_id
        self.price = price
        self.category_name = category_name

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Parent_id: {}, Product_id: {},Price: {}, Category_name: {}".format(self.cat_id, self.name, self.url, self.parent_id, self.product_id, self.price,self.category_name)

    def save_into_db(self):
        query = """
            INSERT INTO product (name, url, parent_id, product_id, price, category)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id, self.product_id, self.price, self.category_name)
        try:
            cur.execute(query,val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

def get_url(url):
    # time.sleep(1)
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parser')
        return response
    except Exception as err:
            print('ERROR BY REQUEST:', err)

def get_main_categories(save_db=False):
    soup = get_url(TIKI)

    result = []
    for a in soup.findAll('a', {'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        cat_id = None
        name = a.find('span', {'class':'text'}).text
        url = a['href']
        parent_id = None

        cat = Category(cat_id, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        result.append(cat)
    return result

# print(get_main_categories(save_db=True))

def get_product(category, save_db=False):
    name = category.name
    url = category.url
    parent_id = category.parent_id
    result = []
    try:
        soup = get_url(url)
        div_containers = soup.findAll('div', {'class':'product-item'}, limit=480)
        for div in div_containers:
            proid = None
            pro_name = div['data-title']
            pro_url = div.a['href']
            pro_parent_id = parent_id
            pro_id = div['data-seller-product-id']
            pro_price = div['data-price']
            pro_cat_name = name
            
            pro = Product(proid,pro_name,pro_url,pro_parent_id,pro_id, pro_price,pro_cat_name)
            if save_db:
                pro.save_into_db()
            result.append(pro)
    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)

    return result


create_categories_table()
create_product_table()
# delete_all('categories')
# a = Product(1,"ggg","dfdfd",12,"12252","2222")
# a.save_into_db()
# print(select_all('product'))
# delete_all('product')
# get_main_categories(save_db=True)

# a = get_main_categories()
# for product in a:
#     get_product(product,save_db=True)

print(select_all('categories'))