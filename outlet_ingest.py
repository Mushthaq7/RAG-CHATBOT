import requests
from bs4 import BeautifulSoup
import sqlite3
import openai


def scrape_outlets():
    url = 'https://zuscoffee.com/category/store/kuala-lumpur-selangor/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    outlets = []
    for item in soup.select('.store-listing'):
        name = item.select_one('.store-title').get_text(strip=True)
        address = item.select_one('.store-address').get_text(strip=True)
        hours = item.select_one(
            '.store-hours').get_text(strip=True) if item.select_one('.store-hours') else ''
        services = item.select_one(
            '.store-services').get_text(strip=True) if item.select_one('.store-services') else ''
        outlets.append({'name': name, 'address': address,
                       'hours': hours, 'services': services})
    return outlets


def populate_db(outlets, db_path='outlets.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS outlets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        hours TEXT,
        services TEXT
    )''')
    c.executemany('''INSERT INTO outlets (name, address, hours, services) VALUES (?, ?, ?, ?)''',
                  [(o['name'], o['address'], o['hours'], o['services']) for o in outlets])
    conn.commit()
    conn.close()
    print(f"Inserted {len(outlets)} outlets into DB.")


if __name__ == '__main__':
    outlets = scrape_outlets()
    populate_db(outlets)
