import requests
from bs4 import BeautifulSoup
import translators as ts
import textwrap
import os


os.system("clear")
print('=' * 50)
print("New Yourk Times")
print('=' * 50)
nav = input("1 = Мировые новости \n" 
            "2 = U.S. \n"
            "3 = Политика \n"
            "4 = N.Y \n"
            "5 = Бизнесс \n")

if nav == '1':
    os.system("clear")
    nav = input("1 = Африка \n"
                "2 = Америка \n"
                "3 = Азия \n"
                "4 = Австралия \n"
                "5 = Канада \n"
                "6 = Европа \n"
                "7 = Средний Восток \n")
    if nav == '1':
        link = "https://www.nytimes.com/section/world/africa"
    elif nav == '2':
        link = "https://www.nytimes.com/section/world/americas"
    elif nav == '3':
        link = "https://www.nytimes.com/section/world/asia"
    elif nav == '4':
        link = "https://www.nytimes.com/section/world/australia"
    elif nav == '5':
        link = "https://www.nytimes.com/section/world/canada"
    elif nav == '6':
        link = "https://www.nytimes.com/section/world/europe"
    elif nav == '7':
        link = "https://www.nytimes.com/section/world/middleeast"
elif nav == '2':
    link = "https://www.nytimes.com/section/us"
elif nav == '3':
    os.system("clear")
    link = "https://www.nytimes.com/section/politics"
elif nav == '4':
    link = "https://www.nytimes.com/section/nyregion"
elif nav == '5':
    os.system("clear")
    nav = input("1 = Книга сделок \n"
                "2 = Экономика \n"
                "3 = Энергия \n"
                "4 = Рынки \n"
                "5 = СМИ \n"
                "6 = Предпринимательство \n"
                "7 = Ваши Деньги \n"
                "8 = Автомобили \n")
    if nav == '1':
        link = "https://www.nytimes.com/section/business/dealbook"
    elif nav == '2':
        link = "https://www.nytimes.com/section/business/economy"
    elif nav == '3':
        link = "https://www.nytimes.com/section/business/energy-environment"
    elif nav == '4':
        link = "https://www.nytimes.com/section/markets-overview"
    elif nav == '5':
        link = "https://www.nytimes.com/section/business/media"
    elif nav == '6':
        link = "https://www.nytimes.com/section/business/smallbusiness"
    elif nav == '7':
        link = "https://www.nytimes.com/section/your-money"
    elif nav == '8':
        link = "https://www.nytimes.com/section/automobiles"

def cprint(text, color='def'):
    str = ''
    fc = '\033['
    colors = {'def': '0m',
              'red': '91m',
              'under': '04m',
              'green': '32m',
              'blue': '94m',
              'cyan': '96m',
              'yellow': '93m',
              'magenta': '95m',
              'grey': '90m'
              }
    if color not in colors:
        print(str + fc + colors['def'] + text)
    else:
        if color == 'under':
            print(str + fc + colors['under'] + text)
        else:
            print(str + fc + colors[color] + text)

session = requests.session()

link1 = 'https://www.nytimes.com/'

header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
}

responce = session.post(link1, headers=header)


def get_page_data(link):
    profile_responce = session.get(link, headers=header).text

    soup = BeautifulSoup(profile_responce, "html.parser")
    post = soup.find_all('li', class_='css-ye6x8s')
    for item in post:
        title = item.find('h2', class_='css-1j9dxys e1xfvim30').get_text(strip=True)
        title = ts.bing(title, to_language='ru', if_use_cn_host=False)
        href = item.find('a').get('href')
        try:
            post = item.find('p', class_='css-1echdzn').get_text(strip=True)
            post = ts.bing(post, to_language='ru', if_use_cn_host=False)
            title = textwrap.fill(title, width=90)
            print('-' * 50)
            cprint("["+title+"]", color='green')
        except AttributeError:
            print('Нет описания')
        print('-' * 50)
        post = textwrap.fill(post, width=90)
        cprint(post)
        print(' ' + '\n' + 'https://www.nytimes.com' + href)



os.system("clear")
get_page_data(link)