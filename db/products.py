import psycopg2


def get_all_brands():
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT DISTINCT brand FROM products")
    brands = cur.fetchall()
    con.close()
    return brands


def add_product(name, price, photo, brand):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute("""INSERT INTO products (name, price, photo, brand) VALUES (%s, %s, %s, %s)""",
                (name, price, photo, brand))
    con.commit()
    con.close()


def get_products_by_brand(brand):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute("""SELECT * FROM products WHERE brand = '{brand}'""", (brand,))
    products = cur.fetchall()
    con.close()
    return products


def get_product_by_id(product_id):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM products WHERE id = {product_id}")
    product = cur.fetchone()
    con.close()
    return product


def get_products(count, color, sort_by=None, brand=None):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    if sort_by == "asc":
        cur.execute(f"SELECT * FROM products WHERE color = %s ORDER BY price  LIMIT {5} OFFSET {5 * (count - 1)}",
                    (color,))
    elif sort_by == "desc":
        cur.execute(f"SELECT * FROM products WHERE color = %s ORDER BY price DESC LIMIT {5} OFFSET {5 * (count - 1)}")
    elif sort_by == "brand":
        cur.execute(f"SELECT * FROM products WHERE color = %s  WHERE brand = %s LIMIT 5 OFFSET {5 * (count - 1)}",
                    (brand, color,))
    else:
        cur.execute(f"SELECT * FROM products WHERE color = %s  ORDER BY id LIMIT {5} OFFSET {5 * (count - 1)}",
                    (color,))
    products = cur.fetchmany(5)
    return products


def get_all_colors():
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT DISTINCT color FROM products")
    colors = cur.fetchall()
    con.close()
    return colors
