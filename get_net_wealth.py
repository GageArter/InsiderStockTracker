from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

from webdriver_manager.chrome import ChromeDriverManager

url = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_Congress_by_wealth"
table_class = "wikitable.sortable.jquery-tablesorter"


def _get_conn():
    conn = sqlite3.connect('net_wealth.db')
    c = conn.cursor()
    return conn, c

def _close_conn(conn):
    conn.commit()
    conn.close()


def _delete_existing_db(conn):
    try:
        conn.execute("DROP TABLE net_wealth")
    except Exception as e:
        print(f"Could not delete, original error {e}")


def _create_db():
    print("Creating database...")
    conn, c = _get_conn()
    _delete_existing_db(c)
    c.execute("""CREATE TABLE net_wealth(
        first text,
        last text,
        net_worth integer
    )""")

    _close_conn(conn)

def _update_db(first, last, net):
    conn, c = _get_conn()
    c.execute("INSERT INTO net_wealth VALUES (?, ?, ?)",(first, last, net))
    _close_conn(conn)


def _get_table_rows():
    print("Getting table...")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, table_class)
    rows = table.find_elements(By.TAG_NAME, 'tr')
    return rows[1:]


def _parse_row(row):
    item =  row.text.split(" ")
    first = item[1]
    last = item[2]
    amount = item[-1]
    if ")" in amount:
        amount = amount.replace(")", "")
    elif "*" in amount:
        amount = amount.replace("*", "")
    return first, last, amount


def main():
    print("Scraping webpage...")
    _create_db()
    rows = _get_table_rows()
    for r in rows:
        first, last, amount = _parse_row(r)
        _update_db(first, last, amount)

if __name__ == '__main__':
    main()
