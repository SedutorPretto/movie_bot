import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


s = Service("C:\\Users\\User\\Desktop\\movie_bot\\movie_bot\\parcer\\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=options)

# Dict name film: url film of 250 best films from kinopoisk
try:
    films_urls = {}
    driver.get('https://www.kinopoisk.ru/')
    if 'utilityfocus' in driver.page_source: # Captcha in manual mode
        time.sleep(60)
    driver.implicitly_wait(6)
    driver.get('https://www.kinopoisk.ru/lists/categories/movies/1/')
    driver.implicitly_wait(6)

    for i in range(1, 6):
        url = f'https://www.kinopoisk.ru/lists/movies/top250/?page={i}'
        driver.get(url=url)
        driver.implicitly_wait(5)
        response = driver.page_source
        data = BeautifulSoup(response, 'lxml')
        driver.implicitly_wait(5)
        films = data.find_all('div', class_='styles_root__ti07r')

        for film in films:
            film_url = 'https://www.kinopoisk.ru' + film.find('a').get('href')
            film_name = film.find('div', class_='base-movie-main-info_mainInfo__ZL_u3').find('span').text
            films_urls[film_name] = film_url

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

with open("films_urls.json", 'w', encoding='utf-8') as file:
    json.dump(films_urls, file, indent=4, ensure_ascii=False)
