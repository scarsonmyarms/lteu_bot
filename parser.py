# import requests
# from bs4 import BeautifulSoup
# import fake_useragent
# import re
# import os
# import json
# from datetime import datetime, timedelta
# import logging
#
# # Налаштування логування
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# CACHE_DIR = 'cache'
# CACHE_EXPIRATION_TIME = timedelta(hours=1)
#
# def _sanitize_filename(url: str) -> str:
#     """Очищує URL для використання в якості імені файлу."""
#     return url.replace('https://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('=', '_') + '.json'
#
# def _fetch_html(url: str) -> str:
#     """Завантажує HTML-контент з вказаного URL з використанням кешування."""
#     os.makedirs(CACHE_DIR, exist_ok=True)
#     cache_file = os.path.join(CACHE_DIR, _sanitize_filename(url))
#
#     if os.path.exists(cache_file):
#         try:
#             with open(cache_file, 'r') as f:
#                 cache_data = json.load(f)
#                 if datetime.now() - datetime.fromisoformat(cache_data['timestamp']) < CACHE_EXPIRATION_TIME:
#                     logging.info(f"Використовується кешована версія для {url}")
#                     return cache_data['content']
#                 else:
#                     logging.info(f"Кеш застарів для {url}, завантажуємо нові дані")
#         except (FileNotFoundError, json.JSONDecodeError):
#             logging.warning(f"Помилка при читанні кеш-файлу для {url}, завантажуємо нові дані")
#
#     user = fake_useragent.UserAgent().random
#     headers = {'user-agent': user}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()  # Перевірка на помилки HTTP
#         content = response.text
#         cache_data = {'timestamp': datetime.now().isoformat(), 'content': content}
#         with open(cache_file, 'w') as f:
#             json.dump(cache_data, f)
#         return content
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Помилка при завантаженні {url}: {e}")
#         return ""
#
# def _extract_phone_numbers(text: str) -> list[str]:
#     """Витягує номери телефонів у форматі +38 з тексту."""
#     return re.findall(r'\+38 \d{9}', text)
#
# def parse_priyomna_numbers() -> list[str]:
#     """Парсить номери телефонів приймальної комісії."""
#     url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
#     html = _fetch_html(url)
#     if not html:
#         return []
#     soup = BeautifulSoup(html, 'html.parser')
#     phone_numbers = []
#     for p in soup.select('p.bodytext'):
#         phone_numbers.extend(_extract_phone_numbers(p.get_text()))
#     logging.info(f"Знайдено номери телефонів приймальної комісії: {phone_numbers}")
#     return phone_numbers
#
# def parse_priyomna_info() -> dict[str, str]:
#     """Парсить контактну інформацію приймальної комісії (адреса, email, соцмережі)."""
#     url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
#     html = _fetch_html(url)
#     if not html:
#         return {}
#     soup = BeautifulSoup(html, 'html.parser')
#     contact_box = soup.find('div', class_='fce-box-orange')
#     if not contact_box:
#         logging.warning("Блок контактної інформації не знайдено.")
#         return {}
#
#     address_span = contact_box.find('span', lang='RU')
#     address = address_span.get_text(strip=True).replace('адреса:', '').strip() if address_span else None
#
#     email_link = contact_box.find('a', class_='mail')
#     email = email_link.get_text(strip=True).replace('(at)', '@') if email_link else None
#
#     facebook_link = contact_box.find('a', href=re.compile(r'facebook\.com'))
#     facebook = facebook_link.get('href') if facebook_link else None
#
#     telegram_link = contact_box.find('a', href=re.compile(r't\.me'))
#     telegram = telegram_link.get('href') if telegram_link else None
#
#     result = {
#         'address': address,
#         'email': email,
#         'facebook': facebook,
#         'telegram': telegram
#     }
#     logging.info(f"Знайдено інформацію про приймальну комісію: {result}")
#     return result
#
# def get_rektor() -> dict[str, str]:
#     """Парсить контактну інформацію ректора."""
#     url = "https://www.lute.lviv.ua/universitet/kontakti/"
#     html = _fetch_html(url)
#     if not html:
#         return {}
#     soup = BeautifulSoup(html, 'html.parser')
#     rektor_divs = soup.select('#c5228')
#     if not rektor_divs:
#         logging.warning("Блок інформації про ректора не знайдено.")
#         return {}
#
#     def _process_contact_data(divs: list) -> dict[str, str]:
#         """Обробляє та форматує контактні дані."""
#         data_dict = {}
#         for div in divs:
#             for p in div.find_all('p'):
#                 text = p.text.strip().replace('\xa0', ' ')
#                 if ":" in text:
#                     key, value = text.split(":", 1)
#                     key = key.strip()
#                     value = value.strip()
#                     if key == 'телефон':
#                         phones = re.findall(r'\(\d{3}\) \d{3}-\d{2}-\d{2}', value)
#                         data_dict[key] = ', '.join(phones)
#                     else:
#                         data_dict[key] = value
#         return data_dict
#
#     rektor_info = _process_contact_data(rektor_divs)
#     logging.info(f"Знайдено інформацію про ректора: {rektor_info}")
#     return rektor_info
#
# def parse_hostel_info() -> dict[str, list[str]]:
#     """Парсить інформацію про гуртожитки."""
#     url = "https://www.lute.lviv.ua/admissions/prozhivannja-studentiv/?L=458"
#     html = _fetch_html(url)
#     if not html:
#         return {}
#     soup = BeautifulSoup(html, 'html.parser')
#     content_div = soup.find('div', class_='csc-textpic-text')
#     if not content_div:
#         logging.warning("Блок інформації про гуртожитки не знайдено.")
#         return {}
#
#     first_paragraph = content_div.find('p', class_='bodytext').get_text(strip=True) if content_div.find('p', class_='bodytext') else None
#     hostel_info = []
#     for li in content_div.find_all('li', limit=3):
#         text = li.get_text(strip=True).replace('\xa0', ' ')
#         text = re.sub(r', кількість місць - \d+\.?', '', text)
#         hostel_info.append(text)
#
#     result = {
#         'description': first_paragraph,
#         'hostels': hostel_info
#     }
#     logging.info(f"Знайдено інформацію про гуртожитки: {result}")
#     return result
#
# def stolova() -> str:
#     """Парсить інформацію про їдальні."""
#     url = "https://www.lute.lviv.ua/structure/other-units/zakladi-kharchuvannja/?L=458"
#     html = _fetch_html(url)
#     if not html:
#         return ""
#     soup = BeautifulSoup(html, 'html.parser')
#     div_content = soup.select('p.bodytext')
#     cleaned_res = [
#         p.get_text(strip=True)
#         for p in div_content
#         if p.get_text(strip=True) and p.get_text(strip=True) != 'Посідає 26 місце в Україні'
#     ]
#     formatted_text = "🍽 <b>Інформація про їдальні:</b>\n\n" + "\n\n".join(
#         f"• {item}" for item in cleaned_res
#     )
#     logging.info("Отримано інформацію про їдальні.")
#     return formatted_text
#
# def magistr_specialitation() -> list[str]:
#     """Парсить список спеціальностей магістра."""
#     url = "https://www.lute.lviv.ua/admissions/osvitnii-riven-magistr/specialnist/?L=7341"
#     html = _fetch_html(url)
#     if not html:
#         return []
#     soup = BeautifulSoup(html, 'html.parser')
#     div_content = soup.select('#c11982')
#     if div_content:
#         raw_text = div_content[0].get_text()
#         specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)
#         cleaned_specialties = [spec.strip() for spec in specialties if spec.strip() and not spec.isspace()]
#         logging.info(f"Знайдено спеціальності магістра: {cleaned_specialties}")
#         return cleaned_specialties
#     else:
#         logging.warning("Блок спеціальностей магістра не знайдено.")
#         return []
#
# def bakalavr_specialitation() -> list[str]:
#     """Парсить список спеціальностей бакалавра."""
#     url = "https://www.lute.lviv.ua/admissions/gss/sp/?L=60"
#     html = _fetch_html(url)
#     if not html:
#         return []
#     soup = BeautifulSoup(html, 'html.parser')
#     div_content = soup.select('#c629')
#     if div_content:
#         raw_text = div_content[0].get_text()
#         specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)
#         cleaned_specialties = [spec.strip() for spec in specialties if spec.strip() and not spec.isspace()]
#         logging.info(f"Знайдено спеціальності бакалавра: {cleaned_specialties}")
#         return cleaned_specialties
#     else:
#         logging.warning("Блок спеціальностей бакалавра не знайдено.")
#         return []
#
# def main():
#     parse_priyomna_numbers()
#     parse_priyomna_info()
#     get_rektor()
#     parse_hostel_info()
#     print(stolova())
#     magistr_specialitation()
#     bakalavr_specialitation()
#
# if __name__ == '__main__':
#     main()

from bs4 import BeautifulSoup
import requests
import fake_useragent
import re
import os
import json
from datetime import datetime, timedelta
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CACHE_DIR = 'cache'
CACHE_EXPIRATION_TIME = timedelta(hours=1)

def _sanitize_filename(url: str) -> str:
    """Очищує URL для використання в якості імені файлу кешу."""
    return url.replace('https://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('=', '_') + '.json'

def _fetch_html_with_cache(url: str) -> str:
    """Завантажує HTML-контент з вказаного URL з використанням кешування."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, _sanitize_filename(url))

    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                if datetime.now() - datetime.fromisoformat(cache_data['timestamp']) < CACHE_EXPIRATION_TIME:
                    logging.info(f"Використовується кешована версія для {url}")
                    return cache_data['content']
                else:
                    logging.info(f"Кеш застарів для {url}, завантажуємо нові дані")
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"Помилка при читанні кеш-файлу для {url}, завантажуємо нові дані")

    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Перевірка на помилки HTTP
        content = response.text
        cache_data = {'timestamp': datetime.now().isoformat(), 'content': content}
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
        return content
    except requests.exceptions.RequestException as e:
        logging.error(f"Помилка при завантаженні {url}: {e}")
        return ""

def parse_priyomna_numbers():
    """Парсить номери телефонів приймальної комісії з використанням кешування."""
    url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
    html = _fetch_html_with_cache(url)
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    all_p = soup.find_all('p', class_='bodytext')
    res = []
    for div in all_p:
        if '+38' in div.get_text():
            numbers = div.find_all(string=True)
            res.extend(numbers)
            filtered = [item for item in res if item.strip() != 'тел.:']
            formatted_numbers = []
            i = 0
            while i < len(filtered):
                if filtered[i] == '+38 ' and i + 1 < len(filtered):
                    formatted_numbers.append(f"+38 {filtered[i + 1]}")
                    i += 2
                else:
                    formatted_numbers.append(filtered[i])
                    i += 1
            final_numbers = [num.strip() for num in formatted_numbers]
            logging.info(f"Знайдено номери телефонів приймальної комісії: {final_numbers}")
            return final_numbers
    return []

def parse_priyomna_info():
    """Парсить контактну інформацію приймальної комісії з використанням кешування."""
    url = "https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274"
    html = _fetch_html_with_cache(url)
    if not html:
        return {}
    soup = BeautifulSoup(html, 'html.parser')
    contact_box = soup.find('div', class_='fce-box-orange')
    if not contact_box:
        logging.warning("Блок контактної інформації не знайдено.")
        return {}
    address = contact_box.find('span', lang='RU').get_text(strip=True).replace('адреса:', '').strip() if contact_box.find('span', lang='RU') else None
    email_section = contact_box.find('a', class_='mail')
    email = email_section.get_text(strip=True).replace('(at)', '@') if email_section else None
    facebook = contact_box.find('a', href=re.compile('facebook.com')).get('href') if contact_box.find('a', href=re.compile('facebook.com')) else None
    telegram = contact_box.find('a', href=re.compile('t.me')).get('href') if contact_box.find('a', href=re.compile('t.me')) else None
    result = {
        'address': address,
        'email': email,
        'facebook': facebook,
        'telegram': telegram
    }
    logging.info(f"Знайдено інформацію про приймальну комісію: {result}")
    return result

def get_rektor():
    """Парсить контактну інформацію ректора з використанням кешування."""
    url = "https://www.lute.lviv.ua/universitet/kontakti/"
    html = _fetch_html_with_cache(url)
    if not html:
        return {}
    soup = BeautifulSoup(html, 'html.parser')
    prinimaet_rektor = soup.find_all('div', id='c5228')

    def process_data(divs):
        data_dict = {}
        for div in divs:
            for p in div.find_all('p'):
                text = p.text.strip().replace('\xa0', ' ')
                if ":" in text:
                    key, value = text.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'телефон':
                        phones = re.findall(r'\(\d{3}\) \d{3}-\d{2}-\d{2}', value)
                        data_dict[key] = ', '.join(phones)
                    else:
                        data_dict[key] = value
        return data_dict

    rektor_info = process_data(prinimaet_rektor)
    logging.info(f"Знайдено інформацію про ректора: {rektor_info}")
    return rektor_info

def parse_hostel_info():
    """Парсить інформацію про гуртожитки з використанням кешування."""
    url = "https://www.lute.lviv.ua/admissions/prozhivannja-studentiv/?L=458"
    html = _fetch_html_with_cache(url)
    if not html:
        return {}
    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find('div', class_='csc-textpic-text')
    if not content_div:
        logging.warning("Блок інформації про гуртожитки не знайдено.")
        return {}
    first_paragraph = content_div.find('p', class_='bodytext').get_text(strip=True) if content_div.find('p', class_='bodytext') else None
    hostel_info = []
    for li in content_div.find_all('li', limit=3):
        text = li.get_text(strip=True).replace('\xa0', ' ')
        text = re.sub(r', кількість місць - \d+\.?', '', text)
        hostel_info.append(text)
    result = {
        'description': first_paragraph,
        'hostels': hostel_info
    }
    logging.info(f"Знайдено інформацію про гуртожитки: {result}")
    return result

def stolova():
    """Парсить інформацію про їдальні з використанням кешування."""
    url = "https://www.lute.lviv.ua/structure/other-units/zakladi-kharchuvannja/?L=458"
    html = _fetch_html_with_cache(url)
    if not html:
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    div_content = soup.find_all('p', class_='bodytext')
    cleaned_res = [
        p.get_text(strip=True)
        for p in div_content
        if p.get_text(strip=True) and p.get_text(strip=True) != 'Посідає 26 місце в Україні'
    ]
    formatted_text = "🍽 <b>Інформація про їдальні:</b>\n\n" + "\n\n".join(
        f"• {item}" for item in cleaned_res
    )
    logging.info("Отримано інформацію про їдальні.")
    return formatted_text

def magistr_specialitation():
    """Парсить список спеціальностей магістра з використанням кешування."""
    url = "https://www.lute.lviv.ua/admissions/osvitnii-riven-magistr/specialnist/?L=7341"
    html = _fetch_html_with_cache(url)
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    div_content = soup.find_all('div', id='c11982')
    if div_content:
        raw_text = div_content[0].get_text()
        specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)
        cleaned_specialties = [spec.strip() for spec in specialties if spec.strip() and not spec.isspace()]
        logging.info(f"Знайдено спеціальності магістра: {cleaned_specialties}")
        return cleaned_specialties
    else:
        logging.warning("Блок спеціальностей магістра не знайдено.")
        return []

def bakalavr_specialitation():
    """Парсить список спеціальностей бакалавра з використанням кешування."""
    url = "https://www.lute.lviv.ua/admissions/gss/sp/?L=60"
    html = _fetch_html_with_cache(url)
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    div_content = soup.find_all('div', id='c629')
    if div_content:
        raw_text = div_content[0].get_text()
        specialties = re.split(r'(?=[A-Z]\d+ - )', raw_text)
        cleaned_specialties = [spec.strip() for spec in specialties if spec.strip() and not spec.isspace()]
        logging.info(f"Знайдено спеціальності бакалавра: {cleaned_specialties}")
        return cleaned_specialties
    else:
        logging.warning("Блок спеціальностей бакалавра не знайдено.")
        return []

def main():
    parse_priyomna_numbers()

if __name__ == '__main__':
    main()