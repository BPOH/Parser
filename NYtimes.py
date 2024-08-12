import os
import requests
import textwrap
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def cprint(text, color='def'):
    colors = {
        'def': 'white', 'red': 'red', 'under': 'underline',
        'green': 'green', 'blue': 'blue', 'cyan': 'cyan',
        'yellow': 'yellow', 'magenta': 'magenta', 'grey': 'grey'
    }
    print(f'[{colors.get(color, "white")}]{text}[/]')

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Welcome message
print(Panel(Text("New York Times", justify="center", style="bold blue"), title="Новости", width=50))

nav_options = {
    '1': {'name': "Мировые новости", 'sub': {
        '1': "africa", '2': "americas", '3': "asia", '4': "australia",
        '5': "canada", '6': "europe", '7': "middleeast"
    }},
    '2': {'name': "U.S.", 'link': "us"},
    '3': {'name': "Политика", 'link': "politics"},
    '4': {'name': "N.Y", 'link': "nyregion"},
    '5': {'name': "Бизнес", 'sub': {
        '1': "dealbook", '2': "economy", '3': "energy-environment",
        '4': "markets-overview", '5': "media", '6': "smallbusiness",
        '7': "your-money", '8': "automobiles"
    }}
}

# Display navigation options in panels
for k, v in nav_options.items():
    panel = Panel(Text(f"{k} - {v['name']}", style="bold green"), width=50)
    console.print(panel)

nav = input("\nВведите номер категории: ")
if nav not in nav_options:
    cprint("Неверный выбор. Пожалуйста, попробуйте снова.", color='red')
    exit()
if 'sub' in nav_options[nav]:
    os.system('cls' if os.name == 'nt' else 'clear')
    # Добавляем заголовок для меню подкатегорий
    print(Panel(Text(f"Выбрана категория: {nav_options[nav]['name']}", justify="center", style="bold blue"), title="Подкатегории", width=50))
    # Отображение подкатегорий с использованием панелей
    for k, v in nav_options[nav]['sub'].items():
        # Используем словарь для перевода названий подкатегорий
        translated_subcategories = {
            "africa": "Африка",
            "americas": "Америка",
            "asia": "Азия",
            "australia": "Австралия",
            "canada": "Канада",
            "europe": "Европа",
            "middleeast": "Ближний Восток"
        }
        subcategory_name = translated_subcategories.get(v, v)
        panel = Panel(Text(f"{k} - {subcategory_name}", style="bold green"), width=50)
        console.print(panel)

    sub_nav = input("\nВведите номер подкатегории: ")
    if sub_nav not in nav_options[nav]['sub']:
        cprint("Неверный выбор. Пожалуйста, попробуйте снова.", color='red')
        exit()
    link = f"https://www.nytimes.com/section/world/{nav_options[nav]['sub'][sub_nav]}"
else:
    link = f"https://www.nytimes.com/section/{nav_options[nav]['link']}"

session = requests.session()
header = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"}

def get_page_data(link):
    try:
        response = session.get(link, headers=header)
        response.raise_for_status()
    except requests.RequestException as e:
        cprint(f"Ошибка при запросе страницы: {e}", color='red')
        return

    soup = BeautifulSoup(response.text, "html.parser")
    translator = GoogleTranslator(source='auto', target='ru')

    for item in soup.find_all('li', class_='css-18yolpw'):
        title = item.find('h3', class_='css-1j88qqx').get_text(strip=True)
        
        try:
            title_ru = translator.translate(title)
        except Exception as e:
            cprint(f"Ошибка при переводе заголовка: {e}", color='red')
            title_ru = title

        href = item.find('a').get('href')
        full_url = f"https://www.nytimes.com{href}"
        
        try:
            post = item.find('p', class_='css-1pga48a').get_text(strip=True)
            try:
                post_ru = translator.translate(post)
            except Exception as e:
                cprint(f"Ошибка при переводе поста: {e}", color='red')
                post_ru = post

            console.print(Panel(Text(textwrap.fill(post_ru, width=80), justify="left"), title=f"[bold green]{title_ru}[/]", expand=False))
        except AttributeError:
            console.print(Panel(Text("Нет описания", justify="left"), title=f"[bold green]{title_ru}[/]", expand=False))

        markdown_link = Markdown(f"[Читать далее]({full_url})")
        console.print(markdown_link)

        print("\n")

os.system('cls' if os.name == 'nt' else 'clear')
get_page_data(link)
