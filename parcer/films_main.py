import json
import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

header = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


def get_page_info(url):
    driver.get(url=url)
    if 'utilityfocus' in driver.page_source:
        time.sleep(30)
    response = driver.page_source
    driver.implicitly_wait(5)
    return BeautifulSoup(response, 'lxml')


def duration_minutes_int():
    dur = data.find_all('div', class_='styles_value__g6yP4')[-1].text
    return int(dur.split()[0])


def get_ganre():
    res = []
    ganres = data.find('div', class_=re.compile(r'(.)+ styles_value__g6yP4 styles_root__5PEXQ')).find_all('a')
    for g in ganres[:-1]:
        res.append(g.text)
    return ', '.join(res)


def get_description():
    desc = data.find('p', class_='styles_paragraph__wEGPz').text
    return re.sub(r'(\xa0)', r'', desc)


with open('films_urls.json', 'r', encoding='utf-8') as file:
    films_urls = json.load(file)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

s = Service("C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\parcer\\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)

base = sqlite3.connect('C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\content\\kino_bot.db')
cur = base.cursor()
if base:
    print('Database is ok!')
base.execute("CREATE TABLE IF NOT EXISTS "
             "main("
             "number INTEGER PRIMARY KEY AUTOINCREMENT, "
             "name_ru, "
             "name_eng, "
             "raitng_kp, "
             "raiting_imdb, "
             "duration, "
             "year_of_production, "
             "ganre, "
             "description)"
             )
base.commit()

films_dict = {}
try:
    for n, film in enumerate(films_urls.items(), start=1):
        name_ru, film_url = film
        data = get_page_info(film_url)

        name_eng = data.find('span', class_='styles_originalTitle__JaNKM')
        if name_eng:
            name_eng = name_eng.text

        raiting_kp = data.find('span', class_=re.compile(r'styles_rating.+')).text

        raiting_imdb = data.find('span', class_='styles_valueSection__0Tcsy')
        if raiting_imdb:
            raiting_imdb = raiting_imdb.text.split()[-1]
        else:
            raiting_imdb = 0

        duration = f'{str(duration_minutes_int() // 60)} ч. {str(duration_minutes_int() % 60)} мин.'

        year_of_production = data.find('a', class_='styles_link__3QfAk').text

        ganre = get_ganre()

        description = get_description()

        films_dict[n] = {'Фильм': name_ru, 'Оригинальное название': name_eng, 'Рейтинг КП': raiting_kp,
                         'Рейтинг имдб': raiting_imdb, 'Продолжительность': duration,
                         'Год производства': year_of_production, 'Жанр': ganre, 'Описание': description}

        cur.execute(
            "INSERT INTO main(name_ru, name_eng, raitng_kp, raiting_imdb, duration, year_of_production, ganre, description) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)", tuple(films_dict[n].values()))
        base.commit()

        poster_url = 'https:' + data.find('img', class_=re.compile(r'film-poster styles_root__24Jga (.)+ styles_root__DZigd')).get('src')
        poster = requests.get(poster_url, headers=header).content
        with open(f'C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\content\\{name_ru.replace(":", "-")}.jpg', 'wb') as file:
            file.write(poster)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
base.close()
