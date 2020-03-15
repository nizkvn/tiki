from bs4 import BeautifulSoup
import requests
import sqlite3

TIKI = "https://tiki.vn/"

conn = sqlite3.connect('product.db')
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
            img_url TEXT,
            data_id TEXT,
            product_id TEXT,
            brand TEXT,
            tiki_now VARCHAR(10),
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
        return "ID: {}, Name: {}, URL:{}, Parent_id: {}".format(self.cat_id, self.name, self.url, self.parent_id)

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
    def __init__(self, pro_id, name, url,img_url, data_id, product_id,brand,tiki_now, price, category_name):
        self.pro_id = pro_id
        self.name = name
        self.url = url
        self.img_url = img_url
        self.data_id = data_id
        self.product_id = product_id
        self.brand = brand
        self.tiki_now = tiki_now
        self.price = price
        self.category_name = category_name

    def __repr__(self):
        return "ID: {}, Name: {}, URL: {}, Img_Url: {}, Data_Id: {}, Product_id: {}, Brand: {}, Tiki_Now: {}, Price: {},Category: {}".format(self.pro_id, self.name, self.url, self.img_url, self.data_id, self.product_id,self.brand,self.tiki_now,self.price,self.category_name)

    def save_into_db(self):
        query = """
            INSERT INTO product (name, url,img_url, data_id, product_id, brand, tiki_now, price, category)
            VALUES (?, ?, ?, ?, ?, ?,?,?,?);
        """
        val = (self.name, self.url, self.img_url, self.data_id, self.product_id,self.brand,self.tiki_now,self.price,self.category_name)
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
    result = []
    try:
        soup = get_url(url)
        div_containers = soup.findAll('div', {'class':'product-item'})
        for div in div_containers:
            proid = None
            pro_name = div['data-title']
            pro_url = div.a['href']
            pro_img_url = div.img['src']
            pro_data_id = div['data-id']
            pro_id = div['data-seller-product-id']
            pro_brand = div['data-brand']
            pro_tiki_now = 'Yes' if div.find('i', {'class':'icon-tikinow'}) else 'No'
            pro_price = div['data-price']
            pro_cat_name = name
            
            pro = Product(proid,pro_name,pro_url,pro_img_url,pro_data_id,pro_id,pro_brand,pro_tiki_now, pro_price,pro_cat_name)
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

a = get_main_categories()
for product in a:
    get_product(product,save_db=True)

# print(select_all('categories'))