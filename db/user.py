import psycopg2


def add_user(telegram_id):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    try:
        cur.execute(f"INSERT INTO users (telegram_id, balance, is_admin) VALUES (%s, 0, %s)", (telegram_id, False))
        con.commit()
    except Exception:
        pass
    con.close()


def get_user(telegram_id):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE telegram_id = {telegram_id}")
    user = cur.fetchone()
    con.close()
    return user


def add_balance(telegram_id, amount):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT balance FROM users WHERE telegram_id = %s", [telegram_id])
    balance = cur.fetchone()
    cur.execute(f"UPDATE users SET balance = %s + %s WHERE telegram_id = %s", [balance, amount, telegram_id])
    con.commit()
    con.close()


def check_admin(telegram_id):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT is_admin FROM users WHERE telegram_id = {telegram_id}")
    is_admin = cur.fetchone()
    con.close()
    return is_admin[0]


def get_all_users():
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT telegram_id FROM users WHERE is_admin = False")
    users = cur.fetchall()
    return users


def get_all_admins():
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT telegram_id FROM users WHERE is_admin = True")
    admins = cur.fetchall()
    return admins
