import sqlite3
import logging
import aiogram
import time
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import datetime, threading, time
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from datetime import timedelta
import config
import json



# Конфигурация logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token='5440610599:AAFUgh0Jb1NzplaD8FBUayj0Zdj6RWhUBPY')
dp = Dispatcher(bot)

p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImYyY2h4ZS0wMCIsInVzZXJfaWQiOiI3OTE5MTYzMjUyNyIsInNlY3JldCI6IjVjYzI0NDIyZjBiY2FiYzYwMTRkMzc4YzFkMmQxMDRmNTQ3ODA2ZDBjOGE5N2MzYTcyZDJiY2FiYmY1NGUyNDEifX0=")
now = datetime.datetime.now()


keyboard = types.InlineKeyboardMarkup()
url_button = types.InlineKeyboardButton(text="💸Перейти к оплате", url="https://my.qiwi.com/Nykyta-K83U2auRLw")
keyboard.add(url_button)

button_1 = KeyboardButton('🛒Категории')
button_2 = KeyboardButton('📃Описание')
button_3 = KeyboardButton('📍Главное меню')


##################################################################################
button_buy1 = KeyboardButton('💲Купить Nitro (1 месяц + 2 буста)')
but_back1 = KeyboardButton('⬅Нaзад') #"Назад" полностью на русском
buy1_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy1_kb.row(button_buy1, but_back1)


button_buy2 = KeyboardButton('💲Купить Nitro (3 месяца + 2 буста)')
but_back2 = KeyboardButton('⬅Нaзад') #"Назад" полностью на русском
buy2_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy2_kb.row(button_buy2, but_back2)

button_buy3 = KeyboardButton('💲Купить Nitro (1 год + 2 буста)')
but_back3= KeyboardButton('⬅Нaзад') #"Назад" полностью на русском
buy3_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy3_kb.row(button_buy3, but_back3)
##################################################################################
button_buy4 = KeyboardButton('💲Купить Nitro Classic (1 месяц)')
but_back4= KeyboardButton('⬅Haзад') #"Назад" H = h на англ.
buy4_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy4_kb.row(button_buy4, but_back4)

button_buy5 = KeyboardButton('💲Купить Nitro Classic (3 месяца)')
but_back5= KeyboardButton('⬅Haзад') #"Назад" H = h на англ.
buy5_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy5_kb.row(button_buy5, but_back5)

button_buy6 = KeyboardButton('💲Купить Nitro Classic (3 месяца)')
but_back6= KeyboardButton('⬅Haзад') #"Назад" H = h на англ.
buy6_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy6_kb.row(button_buy6, but_back6)
##################################################################################
button_buy7 = KeyboardButton('💲Купить Бусты для сервера (2 шт.)')
but_back7= KeyboardButton('⬅Нaзад') #"Назад" первая "a" на англ.
buy7_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy7_kb.row(button_buy7, but_back7)

button_buy8 = KeyboardButton('💲Купить Бусты для сервера (7 шт.)')
but_back8= KeyboardButton('⬅Нaзад') #"Назад" первая "a" на англ.
buy8_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy8_kb.row(button_buy8, but_back8)

button_buy9 = KeyboardButton('💲Купить Бусты для сервера (14 шт.)')
but_back9= KeyboardButton('⬅Нaзад') #"Назад" первая "a" на англ.
buy9_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buy9_kb.row(button_buy9, but_back9)
##################################################################################


start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.row(button_1, button_2)
start_kb.row(button_3)

button_back = KeyboardButton('⬅Назад')
back_kat = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_back)


#инлайн кнопки категорий
kat_nitro = InlineKeyboardButton('Nitro', callback_data='kat_nitro')
kat_boost = InlineKeyboardButton('Nitro server boosting', callback_data='kat_boost')
kat_nitro_cl = InlineKeyboardButton('Nitro classic', callback_data='kat_nitro_cl')
back = InlineKeyboardButton('⬅Назaд', callback_data='back')
inline_kat1 = InlineKeyboardMarkup().add(kat_nitro, kat_nitro_cl, kat_boost)
inline_kat1.add(back)


#Нитро
nitro_kb = InlineKeyboardMarkup()
nitro_t1 = InlineKeyboardButton('🔹Nitro (1 месяц + 2 буста)', callback_data='nitro_t1')
nitro_kb.add(nitro_t1)
nitro_t2 = InlineKeyboardButton('🔹Nitro (3 месяца + 2 буста)', callback_data='nitro_t2')
nitro_kb.add(nitro_t2)
nitro_t3 = InlineKeyboardButton('🔹Nitro (1 год + 2 буста)', callback_data='nitro_t3')
nitro_kb.add(nitro_t3)
back2 = InlineKeyboardButton('⬅Нaзад', callback_data = 'back2')
nitro_kb.add(back2)
#Бусты
boost_kb = InlineKeyboardMarkup()
boost_t1 = InlineKeyboardButton('🔹Буст сервера (2 шт.)', callback_data='boost_t1')
boost_kb.add(boost_t1)
boost_t2 = InlineKeyboardButton('🔹Буст сервера (7 шт.)', callback_data='boost_t2')
boost_kb.add(boost_t2)
boost_t3 = InlineKeyboardButton('🔹Буст сервера (14 шт.)', callback_data='boost_t3')
boost_kb.add(boost_t3)
back3 = InlineKeyboardButton('⬅Нaзад', callback_data = 'back3')
boost_kb.add(back3)
#Нитро классик
nitrocl_kb = InlineKeyboardMarkup()
nitrocl_t1 = InlineKeyboardButton('🔹Nitro (1 месяц)', callback_data='nitrocl_t1')
nitrocl_kb.add(nitrocl_t1)
nitrocl_t2 = InlineKeyboardButton('🔹Nitro (3 месяца)', callback_data='nitrocl_t2')
nitrocl_kb.add(nitrocl_t2)
nitrocl_t3 = InlineKeyboardButton('🔹Nitro (1 год)', callback_data='nitrocl_t3')
nitrocl_kb.add(nitrocl_t3)
back4 = InlineKeyboardButton('⬅Нaзад', callback_data = 'back4')
nitrocl_kb.add(back4)



@dp.message_handler(commands = ['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет, здесь ты можешь купить подписку Discord Nitro/Nitro classic и бусты для своего сервера по самым выгодным ценам! Желаем удачных покупок", reply_markup = start_kb)
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER
        name TEXT
    )''')

    connect.commit()

    people_id = message.chat.id
    cursor.execute(f'SELECT id FROM login_id WHERE id = {people_id}')
    data = cursor.fetchone()
    if data is None:
        user_id = [message.chat.id]
        cursor.execute('INSERT INTO login_id VALUES(?);', user_id)
        connect.commit()
    else:
        print('Такой пользователь уже существует')



    @dp.message_handler(text='🛒Категории')
    async def categories(message: types.Message):
        await bot.send_message(chat_id=message.chat.id, text=' Что из этого вы хотите приобрести?', reply_markup=inline_kat1)

    @dp.message_handler(text='⬅Нaзад')
    async def categories(message: types.Message):
        await bot.send_message(chat_id=message.chat.id, text=' Что из этого вы хотите приобрести?', reply_markup=nitro_kb)

    @dp.message_handler(text='⬅Нaзад в Nitro')
    async def categories(message: types.Message):
        await bot.send_message(chat_id=message.chat.id, text=' Что из этого вы хотите приобрести?', reply_markup=nitro_kb)


    @dp.message_handler(text='📃Описание')
    async def help(message: types.Message):
            chat_id = message.chat.id
            await bot.send_message(chat_id=message.chat.id, text='''Сразу после оплаты вы получаете подарочную ссылку Discord Nitro/Nitro Classic/Nitro Server Boosting. Все ссылки делаются вручную и проверяются. Гарантия до окончания сроков активации(середина ноября 2022 года)
️

Условия активации Discrord Nitro
-Если появляется ошибка «Похоже, что этот код не сработал…», то включите ВПН(Советую использовать бесплатное расширение для Google Chrome, называется ZenMate, выбираем страну Румыния. Если вы в России, то без ВПН у вас всегда будет данная ошибка)
-Данная подписка подходит для всех аккаунтов Discord (Даже если у вас до этого была подписка)

Что дает подписка?
В Nitro включены следующие потрясающие функции:
анимированные аватары и настраиваемый тег
2 буста сервера и скидка 30% на дополнительные бусты
возможность собирать и создавать собственные эмодзи
тематические значки профиля, чтобы выразить вашу поддержку
загрузка более крупных файлов (аж 100 МБ!)
видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live

В Nitro Classic есть все выше перечисленное кроме бустов и скидки на них''', reply_markup = start_kb)

@dp.message_handler(text = '⬅Назaд') #Вторая а англ.
async def categories(message: types.Message):
    await bot.send_message(chat_id = message.chat.id, text='✔Ты вернулся в главное меню.', reply_markup = start_kb)

@dp.message_handler(text = '📍Главное меню')
async def categories(message: types.Message):
    await bot.send_message(chat_id = message.chat.id, text='✔Ты вернулся в главное меню.', reply_markup = start_kb)


@dp.callback_query_handler()
async def handler_call(call: types.CallbackQuery):

        global inline_buy
        chat_id = call.from_user.id
        #категория Нитро
        if call.data == 'kat_nitro':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📌Выберите товар', reply_markup=nitro_kb)
        if call.data == 'nitro_t1':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro (1 месяц + 2 буста) 49р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• 2 буста сервера и скидка 30% на дополнительные бусты
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy1_kb)
        if call.data == 'nitro_t2':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro (3 месяцa + 2 буста) 129р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• 2 буста сервера и скидка 30% на дополнительные бусты
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy2_kb)
        if call.data == 'nitro_t3':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro (1 год + 2 буста) 499р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• 2 буста сервера и скидка 30% на дополнительные бусты
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy3_kb)
        if call.data == 'back2':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📃Вы вернулись в категории', reply_markup=inline_kat1)

        #категория Нитро классик
        if call.data == 'kat_nitro_cl':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📌Выберите товар', reply_markup=nitrocl_kb)
        if call.data == 'nitrocl_t1':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro Classic(1 месяц) 29р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro Classic включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy4_kb)
        if call.data == 'nitrocl_t2':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro Classic(3 месяцa) 49р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro Classic включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy5_kb)
        if call.data == 'nitrocl_t3':
            photopod = open("Discord nitro/2.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Nitro Classic(1 год) 149р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• В Nitro Classic включены следующие потрясающие функции:
• Анимированные аватары и настраиваемый тег
• Возможность собирать и создавать собственные эмодзи
• Тематические значки профиля, чтобы выразить вашу поддержку
• Загрузка более крупных файлов (аж 100 МБ!)
• Видео в высоком разрешении, демонстрация экрана и потоковое вещание Go Live''', reply_markup=buy6_kb)
        if call.data == 'back3':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📃Вы вернулись в категории', reply_markup=inline_kat1)

        #Категория Бустов
        if call.data == 'kat_boost':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📌Выберите товар', reply_markup=boost_kb)
        if call.data == 'boost_t1':
            photopod = open("Discord nitro/1.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Бусты для сервера (2 шт.) 49р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
2 буста для активации 1 уровня
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• +50 слотов для эмодзи (суммарно 100 эмодзи)
• Качество аудио 128 Кбит/с 
• Качество стримов Go Live улучшено до 720P 60FPS
• Кастомизированный фон приглашения сервера
• Анимированная иконка сервера''', reply_markup=buy7_kb)
        if call.data == 'boost_t2':
            photopod = open("Discord nitro/1.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Бусты для сервера (7 шт.) 199р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
7 бустов для активации 2 уровня
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• Всё, что доступно на 1 уровне, и ...
• +50 слотов для эмодзи (суммарно 150 эмодзи)
• Качество аудио 256 Кбит/с
• Качество стримов Go Live улучшено до 1080P 60FPS
• Баннер сервера
• Лимит загрузки файлов для всех пользователей увеличен до 50Мб (только на сервере)''', reply_markup=buy8_kb)
        if call.data == 'boost_t3':
            photopod = open("Discord nitro/1.png", "rb")
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_photo(chat_id, photopod, caption = '''🔷Бусты для сервера (14 шт.) 249р🔷
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
📃Описание:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
14 бустов для активации 3 уровня
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
• Всё, что доступно на 1 и 2 уровнях, а также...
• +100 слотов для эмодзи (суммарно 250 эмодзи)
• Качество аудио 384 Кбит/с
• Лимит загрузки для всех пользователей увеличен до 100Мб (только на сервере)
• Персонализированный URL сервера''', reply_markup=buy9_kb)
        if call.data == 'back4':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, '📃Вы вернулись в категории', reply_markup=inline_kat1)
        elif call.data == 'back':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.send_message(chat_id, 'Вы вернулись в главное меню.', reply_markup=start_kb)


@dp.message_handler(text=['💲Купить Nitro (1 месяц + 2 буста)'])
async def buy(message: types.Message):
    global bill
    price = 1 #Цена которая будет запрашиваться у пользователя | здесь сломалась табуляция, обязательно поставьте таб!
    lifetime = 3 #Время действия ссылки
    comment = 'NitroShop' #Комментарий к платежу, может быть абсолютно любым
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment) #Создаем счет
    link_oplata = bill.pay_url #Получаем ссылку на оплату из нашего счета
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,)) #Target - данный параметр принимает переменную, а в нашем варианте функцию которая будет проверять оплату. Args - аргументы, допустим для отправки сообщения.
    x.start() #Запуск потока
def functionoplata(message: types.Message): #Функция, ее можно создавать даже не асинхронной - ведь эта функция выполняется в потоке для пользователя.
    oplata_time = datetime.datetime.now() #Получаем текущее время
    datetime_delta = oplata_time + timedelta(minutes=3) #Получаем разницу между датами.
    while True: #Создание цикла
        status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты
        if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta: #Делаем проверку, на время оплаты. То есть в случае неоплаты в течении 7-ми минут, цикл прекращается.
            print('мужик, ты че не оплатил')
            break #Завершение цикла
    time.sleep(0.1) #Спим некое время, чтобы бот не крашнулся.

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Nitro (3 месяца + 2 буста)'])
async def buy2(message: types.Message):
    global bill
    price = 129
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata2(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Nitro (1 год + 2 буста)'])
async def buy3(message: types.Message):
    global bill
    price = 499
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata3(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Nitro Classic (1 месяц)'])
async def buy4(message: types.Message):
    global bill
    price = 29
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata4(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Nitro Classic (3 месяца)'])
async def buy5(message: types.Message):
    global bill
    price = 49
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata5(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Nitro Classic (1 год)'])
async def buy6(message: types.Message):
    global bill
    price = 149
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata6(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Бусты для сервера (2 шт.)'])
async def buy7(message: types.Message):
    global bill
    price = 49
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata7(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')

            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Бусты для сервера (7 шт.)'])
async def buy8(message: types.Message):
    global bill
    price = 199
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata8(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)

################################################################################################################################################################################

@dp.message_handler(text=['💲Купить Бусты для сервера (14 шт.)'])
async def buy9(message: types.Message):
    global bill
    price = 249
    lifetime = 7
    comment = 'NitroShop'
    bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment)
    link_oplata = bill.pay_url
    await message.answer(f'''
📌Счет
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵Сумма оплаты: {price} рублей
💳Способ оплаты: QIWI, Банковская карта
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
Счет действителен 7 минут
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖ 
    Для оплаты перейдите по ссылке: {link_oplata}''')
    x = threading.Thread(target=functionoplata, args=(message,))
def functionoplata9(message):
    oplata_time = datetime.datetime.now()
    datetime_delta = oplata_time + timedelta(minutes=7)
    while True:
        status = p2p.check(bill_id=bill.bill_id).status
        if status == 'PAID':
            print('Оплата дошла до нас! Ауе')
            break #Завершение цикла
        elif datetime.datetime.now() > datetime_delta:
            print('мужик, ты че не оплатил')
            break
    time.sleep(0.1)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

