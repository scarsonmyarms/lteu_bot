from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from kb.all_kb import main_kb, vstupnik_kb, magistr_kb
from kb.inline_kbs import ease_link_kb, get_inline_kb, create_qst_inline_kb
from parser import (get_rektor, parse_hostel_info, parse_priyomna_numbers, parse_priyomna_info, stolova, bakalavr_specialitation, magistr_specialitation)
                            # get_hostel)
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

start_router = Router()

# список контактів приймальної комісії
@start_router.message(F.text.lower().contains('контакти'))
async def contacts_info(message: Message):
    contacts = parse_priyomna_numbers()
    info = parse_priyomna_info()

    contacts_text = "<b>📞 Контактні телефони:</b>\n" + "\n".join(
        f"<code>{number}</code>" for number in contacts
    )

    schduel_link = hlink('Натисніть щоб переглянути графік роботи приймальної комісії' ,'https://www.lute.lviv.ua/admissions/priimalna-komisija/?L=274')
    secretary_link = hlink('Відповідальний секретар приймальної комісії','https://www.lute.lviv.ua/kafedri/kafedra-bukhgalterskogo-obliku/boiko-ruslan-volodimirovich/?L=350')

    formated_message = (
        f"🏛 <b>Приймальна комісія LUTE:</b>\n\n"
        f"🏛 <b>{secretary_link}\n</b>"
        f"\n📍 <b>Адрес:</b> {info['address']}\n"
        f"\n📧 <b>E-mail: </b><code>{info['email']}\n</code>"
        f'\n{contacts_text}\n'
        f"\n📍 <b>{hlink('Facebook',info['facebook'])}\n</b>"
        f"\n📍 <b>{hlink('Telegram', info['telegram'])}\n</b>"
        f"\n<b>{schduel_link}\n</b>"
    )

    await message.answer(formated_message, reply_markup=main_kb())

#список контактів приймальної ректора
@start_router.message(F.text.lower().contains('ректор'))
async def rektor_info(message: Message):
    prinimaet_rektor = get_rektor()

    # Функция для форматирования телефонных номеров в HTML
    def format_phones(phone_str):
        phones = phone_str.split(', ')
        return '\n'.join([f'<code>{phone}</code>' for phone in phones])

    # Форматируем сообщение для ректора
    formated_prinimaet_rektor = (
        f"🏛 <b>Приймальна ректора LUTE:</b>\n\n"
        f"📍 <b>Адрес:</b> {prinimaet_rektor['адреса']}\n"
        f"📞 <b>Телефон:</b>\n {format_phones(prinimaet_rektor['телефон'])}\n"
        f"📠 <b>Факс:</b> <code>{prinimaet_rektor['факс']}\n</code>"
        f"📧 <b>E-mail: </b>{prinimaet_rektor['e-mail']}"
    )

    # Отправляем сообщения
    await message.answer("Ось список контактів (якщо на них настиснеш то вони скопіюються)")
    await message.answer(formated_prinimaet_rektor)


@start_router.message(F.text.lower().contains('назад'))
async def start_command(message: Message):
    await message.answer("Привіт! Використай клавіатуру знизу щоб знайти потрібну інформацію.",
                         reply_markup=main_kb())

@start_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привіт! Використай клавіатуру знизу щоб знайти потрібну інформацію.",
                         reply_markup=main_kb())

# клавіатура вступника
@start_router.message(F.text.lower().contains('вступ'))
async def start_command(message: Message):
    await message.answer("ось",
                         reply_markup=vstupnik_kb())

@start_router.message(F.text.lower().contains('документ'))
async def start_command(message: Message):

    docs_link = 'https://www.lute.lviv.ua/admissions/documents/dokumenti-neobkhidni-dlja-vstupu/?L=598'

    await message.answer(f'За посиланням ви можете ознайомитись з документами які потрібні для вступу: \n{docs_link}',
                         reply_markup=vstupnik_kb())

@start_router.message(F.text.lower().contains('спеціальност'))
async def start_command(message: Message):

    specialties = bakalavr_specialitation()

    spec_link = 'https://www.lute.lviv.ua/admissions/gss/sp/?L=350'

    # Форматируем в красивый список
    formatted_text = "🎓 <b>Спеціальності:</b>\n\n" + "\n".join(
        f"▪️ {spec}" for spec in specialties
    )

    await message.answer(formatted_text)
    await message.answer(f'Детальніше про кожну з них за посиланням\n{spec_link}',
                         reply_markup=vstupnik_kb())

@start_router.message((F.text.lower().contains('вартість')) | (F.text.lower().contains('ціна')))
async def price(message: Message):

    price_link = 'https://www.lute.lviv.ua/fileadmin/www.lac.lviv.ua/data/Abitura/LAC_Documents/Pravyla_Pryyomu/2022_Unifikovane/DODATOK_1.pdf'

    text = f'За цим посилання м ти можеш ознайомитись з вартістю навчання за Освітній ступінь бакалавр та магістр: {price_link}\n'

    await message.answer(text, reply_markup=vstupnik_kb())

#інформація про грутожиток
@start_router.message(F.text.lower().contains('гуртожит'))
async def hostel(message: Message):
    hostel_info = parse_hostel_info()

    hostel_link = hlink("Детальніша інформація", 'https://www.lute.lviv.ua/admissions/prozhivannja-studentiv/?L=458')

    formated_text = (
        f"🏠 <b>Інформація про гуртожитки:</b>\n\n"
        f"{hostel_info['description']}\n\n"
        f"<b>Гуртожитки:</b>\n"
    )

    for i, hostel in enumerate(hostel_info['hostels'], 1):
        formated_text += f"{i}. {hostel}\n"

    await message.answer(formated_text)
    await message.answer(hostel_link, reply_markup=vstupnik_kb())


@start_router.message(F.text == 'їдальня')
async def dinnig_room(message: Message):

    dinner_info = stolova()
    link = 'https://www.lute.lviv.ua/structure/other-units/zakladi-kharchuvannja/?L=458'

    await message.answer(dinner_info)
    await message.answer(link)

#аспіратн
@start_router.message(F.text.lower().contains('аспірантура'))
async def start_command(message: Message):

    linl_aspir = 'https://www.lute.lviv.ua/fileadmin/www.lac.lviv.ua/data/Abitura/LAC_Documents/Pravyla_Pryyomu/2022_Unifikovane/DODATOK_8.pdf'

    'правилами прийому до аспірантури та докторантури'

    await message.answer(f"По силанням ви можете ознайомитись з правилами прийому до аспірантури та докторантури:\n{linl_aspir}",
                         reply_markup=vstupnik_kb())

#магістр
@start_router.message(F.text == 'Магістратура')
async def start_command(message: Message):

    price_link = hlink('Натисніть щоб переглянути вартсіть Навчання','https://www.lute.lviv.ua/fileadmin/www.lac.lviv.ua/data/Abitura/LAC_Documents/Pravyla_Pryyomu/2022_Unifikovane/DODATOK_1.pdf')

    # text = f'За цим посилання м ти можеш ознайомитись з вартістю навчання за Освітній ступінь бакалавр та магістр: {price_link}\n'

    specialties = magistr_specialitation()

    specialties_link = 'https://www.lute.lviv.ua/admissions/gss/sp/?L=350'

    # Форматируем в красивый список
    formatted_text = "🎓 <b>Спеціальності:</b>\n\n" + "\n".join(
        f"▪️ {spec}" for spec in specialties
    )

    await message.answer(f'{formatted_text}\n\nДетальніше про кожну з спеціальностей за посиланням:\n{specialties_link}')
    await message.answer(price_link)

#іноземці
@start_router.message(F.text == 'спеціальні потреби')
async def start_command(message: Message):

    link = 'https://www.lute.lviv.ua/universitet/informacija-dlja-osib-z-obmezhenimi-mozhlivostjami/?L=458'

    await message.answer(f'Умови навчання для осіб з особливими освітніми потребами: \n\n{link}')

@start_router.message(F.text == 'Іноземним студентам')
async def start_command(message: Message):

    link = 'https://www.lute.lviv.ua/admissions/dovuzivska-pidgotovka-inozemciv-ta-osib-bez-gromadjanstva/?L=2'
    await message.answer(f'Детальніше про навчання інощемних студентів за посиланням: \n{link}')

