import psycopg2


def create_order(tg_id, product_id):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute("""INSERT INTO orders(telegram_id, product_id, status) VALUES (%s, %s, %s)""",
                (tg_id, product_id, "active"))
    con.commit()
    cur.execute("SELECT id FROM orders WHERE telegram_id = %s AND product_id = %s AND status = 'active' "
                "ORDER BY id DESC LIMIT 1",
                (tg_id, product_id))
    order_id = cur.fetchone()[0]
    con.close()

    return order_id


def get_orders(tg_id, page=1):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM orders WHERE telegram_id = {tg_id} LIMIT 5 OFFSET {5 * (page - 1)}")
    orders = cur.fetchall()
    con.close()
    return orders


def get_order(order_id):
    try:
        con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
        cur = con.cursor()
        cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cur.fetchone()
        con.close()
        return order
    except Exception as e:
        print(e)


def change_order_status(order_id, status):
    con = psycopg2.connect(dbname="ShopDB", host="localhost", user="postgres", password="QwerTY", port="5432")
    cur = con.cursor()
    cur.execute(f"UPDATE orders SET status = '{status}' WHERE id = {order_id}")
    con.commit()
    con.close()
