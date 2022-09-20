from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
start = types.ReplyKeyboardMarkup(resize_keyboard=True)
info = types.KeyboardButton('📔Информация')
time= types.KeyboardButton('⏰Расписание')
horoscope = types.KeyboardButton("✅Мой гороскоп")
# # и статистика СДЕЛАТЬ КОМАНДАМИ
# stats = types.KeyboardButton('Статистика')
# # и разработчик
# razrab = types.KeyboardButton("Разработчик")
# start.add(razrab)
start.add(horoscope, time, info)
#
answer_1 = InlineKeyboardMarkup()  # разметка inline-кнопок
answer_1.add(InlineKeyboardButton('👌', callback_data='yes_1'))  # создание кнопки "Да" c колбеком join
answer_1.add(InlineKeyboardButton('Спасибо, пока нет', callback_data='no_1'))  # создание кнопки "Нет" с колбеком cancel


stats = InlineKeyboardMarkup(row_width=2)  # разметка inline-кнопок
stats.add(InlineKeyboardButton('Да', callback_data='join'))  # создание кнопки "Да" c колбеком join
stats.add(InlineKeyboardButton('Нет', callback_data='cancel'))  # создание кнопки "Нет" с колбеком cancel

sign_zodiac = InlineKeyboardMarkup(row_width=4)
sign_zodiac.add(InlineKeyboardButton('Овен♈', callback_data='aries'))
sign_zodiac.add(InlineKeyboardButton('Телец♉', callback_data='taurus'))
sign_zodiac.add(InlineKeyboardButton('Близнецы♊', callback_data='gemini'))
sign_zodiac.add(InlineKeyboardButton('Рак♋', callback_data='cancer'))
sign_zodiac.add(InlineKeyboardButton('Лев♌', callback_data='leo'))
sign_zodiac.add(InlineKeyboardButton('Дева♍', callback_data='virgo'))
sign_zodiac.add(InlineKeyboardButton('Весы♎', callback_data='libra'))
sign_zodiac.add(InlineKeyboardButton('Скорпион♏', callback_data='scorpio'))
sign_zodiac.add(InlineKeyboardButton('Стрелец♐', callback_data='sagittarius'))
sign_zodiac.add(InlineKeyboardButton('Козерог♑', callback_data='capricom'))
sign_zodiac.add(InlineKeyboardButton('Водолей♒', callback_data='aquarius'))
sign_zodiac.add(InlineKeyboardButton('Рыб♓', callback_data='pisces'))


yes =InlineKeyboardMarkup(row_width=1)
yes.add(InlineKeyboardButton('Да', callback_data='yes_2'))

