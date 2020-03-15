from flask import Flask, render_template
app = Flask(__name__)
import test

from bs4 import BeautifulSoup
import requests
import sqlite3

TIKI_URL = "https://tiki.vn/"

def get_url(url):
    # time.sleep(1)
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parser')
        return response
    except Exception as err:
            print('ERROR BY REQUEST:', err)

def get_main_categories(save_db=False):
    soup = get_url(TIKI_URL)

    result = []
    for a in soup.findAll('a', {'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        cat_id = None
        name = a.find('span', {'class':'text'}).text
        url = a['href']
        parent_id = None

        cat = test.Category(cat_id, name, url, parent_id)
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
            pro_parent_id = category.cat_id
            pro_id = div['data-seller-product-id']
            pro_price = div['data-price']


            pro = test.Product(proid,pro_name,pro_url,pro_parent_id,pro_id, pro_price)
            if save_db:
                pro.save_into_db()
            result.append(pro)
    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)

    return result
a = get_main_categories(save_db=True)
b= a[0]
get_product(b,save_db=True)
test.select_all('categories')

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 