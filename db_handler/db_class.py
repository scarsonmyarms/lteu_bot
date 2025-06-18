from sqlalchemy import String, BigInteger, TIMESTAMP
from create_bot import db_manager
import asyncio


# функция, которая создаст таблицу с пользователями
async def create_table_users(table_name='users_reg'):
    async with db_manager as client:
        columns = [
            {"name": "user_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}}, # user_id – телеграм ID пользователя (берем с объекта message)
            {"name": "full_name", "type": String}, # full_name – полное имя пользователя (берем с объекта message)
            {"name": "user_login", "type": String}, # user_login – логин в телеграмм (берем с объекта message)
            {"name": "date_reg", "type": TIMESTAMP}, # date_reg – дата и время регистрации, будет заполняться автоматически
        ]
        await client.create_table(table_name=table_name, columns=columns)


# функция, для получения информации по конкретному пользователю
async def get_user_data(user_id: int, table_name='users_reg'):
    async with db_manager as client:
        user_data = await client.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
    return user_data


# функция, для получения всех пользователей (для админки)
async def get_all_users(table_name='users_reg', count=False):
    async with db_manager as client:
        all_users = await client.select_data(table_name=table_name)
    if count:
        return len(all_users)
    else:
        return all_users


# функция, для добавления пользователя в базу данных
async def insert_user(user_data: dict, table_name='users_reg'):
# Изначально идет базовый синтаксис добавления пользователя, но после запускается проверка был ли передан refer_id (понятнее будет далее).
#  Если это так – то мы запускаем процесс обновления количества пользователей
    async with db_manager as client:
        await client.insert_data_with_update(table_name=table_name, records_data=user_data, conflict_column='user_id')

# нужно выполнить для создания таблицы иначе будем получать ошибку при подключении так как таблицы не существует
# asyncio.run(create_table_users())
