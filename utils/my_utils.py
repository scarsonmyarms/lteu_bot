from faker import Faker
from bs4 import BeautifulSoup
import requests
import fake_useragent
import re
from datetime import datetime
import pytz

def parse_priyomna_numbers():

    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')

    all_p = soup.find_all('p', class_='bodytext')

    res = []

    for div in all_p:
        if '+38' in div.get_text():
            numbers = div.find_all(string=True)  # получаем весь текст
            res.extend(numbers)
            print(res)
            # Удаляем элемент 'тел.:'
            filtered = [item for item in res if item.strip() != 'тел.:']
            # Объединяем '+38' со следующими элементами
            formatted_numbers = []
            i = 0
            while i < len(filtered):
                if filtered[i] == '+38 ' and i + 1 < len(filtered):
                    # Объединяем '+38' со следующим элементом
                    formatted_numbers.append(f"+38 {filtered[i + 1]}")
                    i += 2
                else:
                    # Просто добавляем элемент как есть (уже содержит +38)
                    formatted_numbers.append(filtered[i])
                    i += 1
            final_numbers = [num.strip() for num in formatted_numbers]
            print(final_numbers)

    return final_numbers

def parse_priyomna_info():
    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')

    contact_box = soup.find('div', class_='fce-box-orange')

    # Парсим адрес
    address = contact_box.find('span', lang='RU').get_text(strip=True).replace('адреса:', '').strip()

    # Парсим email
    email_section = contact_box.find('a', class_='mail')
    email = email_section.get_text(strip=True).replace('(at)', '@')

    # Парсим Facebook и Telegram
    facebook = contact_box.find('a', href=re.compile('facebook.com')).get('href')
    telegram = contact_box.find('a', href=re.compile('t.me')).get('href')

    # Формируем результат
    result = {
        'address': address,
        'email': email,
        'facebook': facebook,
        'telegram': telegram
    }
    print(result)
    return result

def get_rektor():
    # Ваш исходный код сбора данных
    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/universitet/kontakti/"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    prinimaet_rektor = soup.find_all('div', id='c5228')
    prinimaet_komisiya = soup.find_all('div', id='c5232')

    # Функция для обработки и форматирования данных
    def process_data(divs):
        result = []
        for div in divs:
            num = div.find_all('p')
            for p in num:
                text = p.text.strip()
                text = text.replace('\xa0', ' ')
                text = ' '.join(text.split())
                result.append(text)

        data_dict = {}
        for item in result:
            key, value = item.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Форматирование телефонных номеров
            if key == 'телефон':
                # Находим все номера в формате (XXX) XXX-XX-XX
                phones = re.findall(r'\(\d{3}\) \d{3}-\d{2}-\d{2}', value)
                value = ', '.join(phones)

            data_dict[key] = value

        return data_dict

    # Обрабатываем данные для ректора и комиссии
    dict_prinimaet_rektor = process_data(prinimaet_rektor)

    return dict_prinimaet_rektor

# інформація про гуртожиток
def parse_hostel_info():
    url = "https://www.lute.lviv.ua/admissions/prozhivannja-studentiv/?L=458"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим основной контентный блок
    content_div = soup.find('div', class_='csc-textpic-text')

    # Извлекаем первый абзац (первый <p> с классом bodytext)
    first_paragraph = content_div.find('p', class_='bodytext').get_text(strip=True)

    # Извлекаем первые 3 пункта списка и обрабатываем их
    list_items = content_div.find_all('li', limit=3)
    hostel_info = []
    for li in list_items:
        text = li.get_text(strip=True)
        # Удаляем информацию о количестве мест
        text = re.sub(r', кількість місць - \d+\.?', '', text)
        # Заменяем неразрывные пробелы
        text = text.replace('\xa0', ' ')
        hostel_info.append(text)

    # Форматируем результат
    result = {
        'description': first_paragraph,
        'hostels': hostel_info
    }
    print(result)
    return result


# Інформація про їдальню
def stolova():

    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/structure/other-units/zakladi-kharchuvannja/?L=458"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')

    div_content = soup.find_all('p', class_='bodytext')
    res = []

    for p in div_content:
        text = p.get_text(strip=True)
        res.append(text)

    cleaned_res = [
        item for item in res
        if item and item != 'Посідає 26 місце в Україні'
    ]

    # Объединение в строку с форматированием
    formatted_text = "🍽 <b>Інформація про їдальні:</b>\n\n" + "\n\n".join(
        f"• {item}" for item in cleaned_res
    )

    return formatted_text  # Возвращаем строку, а не список

#інформація про спеціальності магістр
def magistr_specialitation():

    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/admissions/osvitnii-riven-magistr/specialnist/?L=7341"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    div_content = soup.find_all('div', id='c11982')
    # Извлекаем весь текст и обрабатываем
    raw_text = div_content[0].get_text() if div_content else ""

    # Разделяем по шаблону "БукваЦифра -"
    import re
    specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)

    # Фильтруем пустые строки и очищаем
    cleaned_specialties = [
        spec.strip()
        for spec in specialties
        if spec.strip() and not spec.isspace()
    ]
    print(cleaned_specialties)
    return cleaned_specialties

#інформація про спеціальності бакалавр
def bakalavr_specialitation():

    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = "https://www.lute.lviv.ua/admissions/gss/sp/?L=60"
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    div_content = soup.find_all('div', id='c629')
    # Извлекаем весь текст и обрабатываем
    raw_text = div_content[0].get_text() if div_content else ""

    # Разделяем по шаблону "БукваЦифра -"
    import re
    specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)

    # Фильтруем пустые строки и очищаем
    cleaned_specialties = [
        spec.strip()
        for spec in specialties
        if spec.strip() and not spec.isspace()
    ]
    print(cleaned_specialties)
    return cleaned_specialties

def get_now_time():
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    return now.replace(tzinfo=None)


# def main():
#     magistr_specialitation()
#
# if __name__ == '__main__':
#     main()