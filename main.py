import requests
import sqlite3
headers = {
    'authority': 'lucky-jet-a.1play.one',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://lucky-jet-b.1play.one',
    'referer': 'https://lucky-jet-b.1play.one/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'session': 'demo',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}
while 1 ==1:
    try:
        response = requests.get('https://lucky-jet-a.1play.one/public/history/api/history/last', headers=headers)
        data1 = response.json()
        kef = data1.get("coefficient")
        id = data1.get("id")
        connector = sqlite3.connect('history.db')
        cursor = connector.cursor()
        cursor.execute("SELECT id from history where id = ?",(id,))
        a = cursor.fetchone()
        if a == None:
            cursor.execute("INSERT INTO history VALUES(?,?)", (id,kef,))
            connector.commit()
    except:
        1