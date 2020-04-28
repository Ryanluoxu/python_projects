import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

# database
conn = sqlite3.connect('raw.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS cases
    (id INTEGER PRIMARY KEY
    , confirmed_date TEXT
    , age INTEGER
    , gender TEXT
    , nationality TEXT
    , status TEXT
    , infection_source TEXT
    , origin_country TEXT
    , days_to_recover TEXT
    )
     ''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url="https://againstcovid19.com/singapore/cases/search"
web_conn = urlopen(url, context=ctx)
html = web_conn.read()
soup = BeautifulSoup(html, "html.parser")

# .../table/tbody/tr/td
rows = soup.find_all('tr')

for row in rows:
    data = row.find_all("td")
    if len(data) == 0: continue

    case_id = data[0].text.strip()
    age = data[2].text.strip()
    gender = data[3].text.strip()
    nationality = data[4].text.strip()
    status = data[5].text.strip()
    infection_source = data[6].text.strip()
    origin_country = data[7].text.strip()
    days_to_recover = data[9].text.strip()
    confirmed_date = data[11].text.strip()

    cur.execute("INSERT OR IGNORE INTO cases (id,confirmed_date,age,gender,nationality,status,infection_source,origin_country,days_to_recover) VALUES (?,?,?,?,?,?,?,?,?)", (case_id,confirmed_date,age,gender,nationality,status,infection_source,origin_country,days_to_recover))
conn.commit()
cur.close()
