import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
import keyboard
import parsing_horoscope

# Хранилище состояний
storage = MemoryStorage()
# Инициализация бота и установка режима парсинга для сообщений бота (инструмент
# для оформления текста выбирается аргументом функции parse_mode
bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
# Инициализация диспетчера (Dispatcher - принимает все и обрабатывает), при этом указываем ему на хранилище состояний
dp = Dispatcher(bot, storage=storage)
# Подключаем логирование
logging.basicConfig(filename='log.txt', level=logging.INFO, format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
                                                                   u'[%(asctime)s] %(message)s')


# Прописываем состояния
class info_about_user(StatesGroup):
    info_about_user_1 = State()
    info_about_user_2 = State()
    info_about_user_3 = State()


@dp.message_handler(commands='about_me', state=None)
async def enter_admin_info(message: types.Message):
    await bot.send_message(message.chat.id, "Сколько тебе лет?")
    await info_about_user.info_about_user_1.set()


@dp.message_handler(state=info_about_user.info_about_user_1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Напиши свой пол")
    await info_about_user.info_about_user_2.set()


@dp.message_handler(state=info_about_user.info_about_user_2)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Напиши свой род деятельности")
    await info_about_user.info_about_user_3.set()


@dp.message_handler(state=info_about_user.info_about_user_3)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer("Текст сохранен. Спасибо!")

    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")

    joinFile = open("age.txt", "w", encoding="utf-8")
    joinFile.write(str(answer1))
    joinFile = open("gender.txt", "w", encoding="utf-8")
    joinFile.write(str(answer2))
    joinFile = open("work.txt", "w", encoding="utf-8")
    joinFile.write(str(answer2))

    await message.answer(f"Ваш ответ: {answer1},{answer2}, {answer3}")
    await state.finish()


# Прописываем состояния
class admin_info(StatesGroup):
    admin_info_1 = State()
    admin_info_2 = State()


@dp.message_handler(commands='me', state=None)
async def enter_admin_info(message: types.Message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, "Начинаем настройку Введите ссылку на ваш профиль")
        await admin_info.admin_info_1.set()


@dp.message_handler(state=admin_info.admin_info_1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Линк сохранен. \n" "Введите текст.")
    await admin_info.admin_info_2.set()


@dp.message_handler(state=admin_info.admin_info_2)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Текст сохранен")

    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")

    joinFile = open("link.txt", "w", encoding="utf-8")
    joinFile.write(str(answer1))
    joinFile = open("text.txt", "w", encoding="utf-8")
    joinFile.write(str(answer2))

    await message.answer(f"Ссылка: {answer1}. Ваш текст {answer2}")
    await state.finish()


# Обработчик для команд
@dp.message_handler(commands='start', state=None)
async def welcome(message: types.Message):
    # открываем файл user.txt в режиме чтения
    joined_file = open('user.txt', 'r')
    # создаем множество для хранения имен всех пользователей
    joined_users = set()
    # проходим циклом по каждому пользователю в user.txt
    for line in joined_file:
        # добавляем их в наше множество пользователей
        joined_users.add(line.strip())
    # если пользователь, который нажал /start
    # находится во множестве пользователей
    if not str(message.chat.id) in joined_users:
        # открываем файл user.txt на дозапись
        joined_file = open('user.txt', 'a')
        # записываем в него id нашего пользователя
        joined_file.write(str(message.chat.id) + '\n')
        # добавляем его во множество пользователей
        joined_users.add(message.chat.id)
        # говорим боту отправить сообщение, при этом
    await bot.send_message(
        # обращаемся к id пользователя
        message.chat.id,
        # указываем отправляемое сообщение hello + имя пользователя
        f'Привет {message.from_user.first_name}🖐, \nхочешь узнать гороскоп на сегодня?',
        # подключаем кнопки из файла keyboard, обратившись к переменной start
        reply_markup=keyboard.start)
    await message.answer('Эти знания помогут тебе правильно спланировать свой день😇',
                         reply_markup=keyboard.answer_1)


# Обработчик для команд
@dp.message_handler(commands='stat', state=None)
async def welcome(message: types.Message):
    if message.chat.id == config.admin:
        await bot.send_message(
            message.chat.id,
            text='Хочешь посмотреть статистику бота?',
            reply_markup=keyboard.stats)


# Обработчик для команд
@dp.message_handler(commands='develop', state=None)
async def welcome(message: types.Message):
    if message.chat.id == config.admin:
        # открываем наш файл link.txt
        with open("link.txt", encoding="UTF-8") as link_txt:
            # считываем его содержимое в переменную link
            link = link_txt.read()
        with open("text.txt", encoding="UTF-8") as text_txt:
            text = text_txt.read()
        await bot.send_message(message.chat.id, text=f"Разработчик: {link} \n {text}", reply_markup=keyboard.start)


# Обработчик для команд
@dp.message_handler(commands='mailing_list_1', state=None)
# задаем функцию обработчик
async def mailing_list(message: types.Message):
    # сверяем id пославшего сообщение с id админа
    if message.chat.id == config.admin:
        # отправляем сообщение
        await bot.send_message(message.chat.id, f'Рассылка началась')
    # задаем переменные для хранения принявших и заблокировавших
    recieve_users, block_users = 0, 0
    # открываем user.txt в режиме чтения
    with open('user.txt', 'r') as file:
        # создаем множество всех пользователей
        joined_users = set()
        # проходим циклу по всем id в файле
        for line in file:
            # добавляем во множество id
            joined_users.add(line.strip())
        # запускаем цикл
        for user in joined_users:
            try:
                await bot.send_message(user,
                                       text="Раскажешь про себя? Благодаря этой информации я смогу подготовить еще больше полезной информации. Набери и отправь сообщение /about_me, чтобы пройти опрос.")
                await bot.send_photo(user, open('photo_2.jpg', 'rb'))
                recieve_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, f'Рассылка завершена \n'
                                                f'Сообщение получили: *{recieve_users}* пользователей \n'
                                                f'Заблокировали бота: *{block_users}*')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="yes_1")
async def look_total_horo(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для всех знаков на сегодня🌠* \n\n{parsing_horoscope.total_horo_list}",
                                parse_mode='Markdown')
    await bot.send_message(call.message.chat.id, "Продолжим?", reply_markup=keyboard.yes)


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="no_1")
async def not_look_total_horo(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Понятно🙂. Как только захочешь узнать гороскоп - жми на  кнопку 'Мой гороскоп'⤵ ",
                                parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="yes_2")
async def choose_sign(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Выбери свой знак зодиака", reply_markup=keyboard.sign_zodiac)


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="aries")
async def horo_for_aries(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Овна♈* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="taurus")
async def horo_for_taurus(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Тельца♉* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="gemini")
async def horo_for_gemini(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Близнецов♊* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="cancer")
async def horo_for_cancer(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Рака♋* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="leo")
async def horo_for_leo(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Льва♌* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="virgo")
async def horo_for_virgo(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Девы♍* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="libra")
async def horo_for_libra(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Весов♎* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="scorpio")
async def horo_for_scorpio(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Скорпиона♏* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="sagittarius")
async def horo_for_sagittarius(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Стрельца♐* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="capricom")
async def horo_for_capricom(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Козерога♑* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="aquarius")
async def horo_for_aquarius(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Водолея♒* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="pisces")
async def horo_for_pisces(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Гороскоп для Рыб♓* \n\nсюда надо спарсить инфу с сайта", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="join")
async def send_stat_about_bot(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open("user.txt"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Вот статистика бота: *{d}* человек", parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"У тебя нет админки", parse_mode='Markdown')


# Обработчик инлайн кнопок
@dp.callback_query_handler(text_contains="cancel")
async def horo_for_pisces(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Ты вернулся в главное меню", parse_mode='Markdown')


# Обработка текстовых сообщений (кнопки клавиатуры)
@dp.message_handler(content_types=['text'])
# задаем функцию-обработчик
async def info_static(message: types.Message):
    # если переданное боту сообщение = 'Информация'
    if message.text == '📔Информация':
        # бот отправляет сообщение пользователю, отправившего его
        await bot.send_message(message.chat.id,
                               # с текстом
                               text='Ты можешь получать гороскоп по запросу или настроить расписание - и я буду ежедневно присылать тебе гороскоп.',
                               # режим форматирования
                               parse_mode='Markdown')
    if message.text == '⏰Расписание':
        # бот отправляет сообщение пользователю, отправившего его
        await bot.send_message(message.chat.id,
                               # с текстом
                               text='Временно настройка расписания недоступна, попробуй позже',
                               # режим форматирования
                               parse_mode='Markdown')
    if message.text == '✅Мой гороскоп':
        await message.answer(f"*Гороскоп для всех знаков на сегодня🌠* \n\n{parsing_horoscope.total_horo_list}",
                             parse_mode='Markdown')
        await message.answer("Продолжим?", reply_markup=keyboard.yes)


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
