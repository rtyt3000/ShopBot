import psycopg2


def create_tables():
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    create_products = """CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price FLOAT,
    color TEXT,
    photo TEXT, 
    brand TEXT)"""

    create_users = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    balance FLOAT,
    telegram_id bigserial UNIQUE,
    is_admin BOOLEAN)"""

    create_orders = """CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    telegram_id bigserial,
    product_id INTEGER,
    status TEXT)"""

    cur.execute(create_products)
    cur.execute(create_users)
    cur.execute(create_orders)
    con.commit()
    con.close()


def add_product(name, price, photo, brand):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute("""INSERT INTO products (name, price, photo, brand) VALUES (%s, %s, %s, %s)""",
                (name, price, photo, brand))
    con.commit()
    con.close()
