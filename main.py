import telebot
import pymysql
from telebot.types import CallbackQuery, Message

import inline_keyboards
import Message_Settings
import Image_Settings

import sqlite3

chanel_id = -1002224769146

connection = sqlite3.connect('telegrambot.db')

cursor = connection.cursor()

# Создание таблицы users, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                       ID INTEGER PRIMARY KEY,
                       Referal VARCHAR,
                       Balance INTEGER,
                       Wallet TEXT
                   )''')

connection.commit()
connection.close()
print('Таблица users создана или уже существует')

bot = telebot.TeleBot("6502174873:AAGOgV4qSkYO_eW455MOTjMa8JNaARLDzhk")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Проверка на наличие пользователя в базе данных
    connection = sqlite3.connect('telegrambot.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT ID FROM users WHERE ID = {message.from_user.id}")
    existing_user = cursor.fetchone()[0]
    print(existing_user)
    if not existing_user:
        print('tut')
        # Регистрация нового пользователя
        cursor.execute(f"INSERT INTO users (`ID`, `Referal`, `Balance`, `Wallet`) VALUES ({message.from_user.id},'32233223' , 0, 'Отсутствует')")
        connection.commit()

    connection.close()
    member = bot.get_chat_member(chanel_id, message.chat.id)
    # Условия подписки
    if member.status in ['member', 'administrator', 'creator']:
        # Проверка наличия реферального айди
        if len(message.text.split()) > 1:
            referral_id = message.text.split()[-1]
            connection = sqlite3.connect('telegrambot.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT ID FROM users WHERE ID = {referral_id}")
            invited_user = cursor.fetchone()[0]
            connection.close()
            if invited_user:
                connection = sqlite3.connect('telegrambot.db')
                cursor = connection.cursor()
                cursor.execute(f"SELECT Referal FROM users WHERE ID = {referral_id}")
                referals = cursor.fetchone()[0]
                connection.close()
                if str(message.from_user.id) not in referals.split('_'):
                    referals+=f'_{message.from_user.id}'
                    print(referals)
                    with sqlite3.connect('telegrambot.db') as connection:
                        cursor = connection.cursor()
                        cursor.execute("UPDATE users SET Referal = ? WHERE ID = ?", (referals, int(referral_id)))
                        connection.commit()



        bot.send_message(message.chat.id, "🔝 Главное Меню", reply_markup=inline_keyboards.MainMenu())
        bot.send_photo(message.chat.id, photo=Image_Settings.PhotoTake['Welcome'],
                       caption=Message_Settings.MENU_message, parse_mode='Markdown',
                       reply_markup=inline_keyboards.InviteButton())
    else:
        # Handle case where chat ID is missing or invalid
        bot.reply_to(message, "❌Вы не подписаны на канал")
@bot.message_handler(func=lambda message: True)
def error_message(message: Message):
    if message.text == 'Условия\\Terms 📃':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Terms'], caption=Message_Settings.Terms_message,parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
    elif message.text == 'Баланс\\Balance 🙂':
        connection = sqlite3.connect('telegrambot.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT Referal FROM users WHERE ID = {message.from_user.id}")
        referals = cursor.fetchone()[0]
        connection.close()
        text = f'Ваш баланс:\n_{len(referals.split('_'))} ref. = {len(referals.split('_')) * 200} $SMILE_\n\nДля получения больше токенов, пригласите больше друзей, 1 реферал - 200 токенов\n\n_Пригласить больше друзей 👇🏼_'
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Balance'], caption=text,parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
    elif message.text == 'Кошелек\\Wallet 👛':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Wallet'], caption=Message_Settings.Wallet_message,parse_mode='Markdown',reply_markup=inline_keyboards.CancleMenu())
        sent = bot.send_message(message.chat.id, "Введите ваш кошелек:")
        bot.register_next_step_handler(sent, save_wallet)
    elif message.text == 'Twitter[BONUS] 🕊':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Twitter'], caption=Message_Settings.Twitter_message,parse_mode='Markdown')
    elif message.text == 'Terms [ENG] 📌':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['TermsENG'], caption=Message_Settings.TermsENG_message,parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
    elif message.text == "GETID":
        bot.send_message(message.chat.id, message.chat.id)    
    else:
        bot.reply_to(message, Message_Settings.ERROR_message, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data == "check":
        #Условия подписки
        UserBoxID = call.message.chat.id
        member = bot.get_chat_member(chanel_id, UserBoxID)
        if member.status in ['member', 'administrator', 'creator']:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🔝 Главное Меню", reply_markup=inline_keyboards.MainMenu())
            bot.send_photo(call.message.chat.id, photo = Image_Settings.PhotoTake['Welcome'], caption= Message_Settings.MENU_message, parse_mode='Markdown',reply_markup=inline_keyboards.InviteButton())
            connection.ping()
            with connection.cursor() as cursor:
            # Create a new record
                sql = "INSERT INTO `users`(`ID`, `Referal`, `Balance`, `Wallet`) VALUES (%s, %s, %s, %s)" %(UserBoxID, 123, 0, '"Отсутствует"')
                print(cursor.execute(sql))
            connection.commit()
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, Message_Settings.WELCOME_message, reply_markup = inline_keyboards.welcome_keys())
    elif call.data == 'Invite':
        bot.send_message(chat_id=call.message.chat.id ,text = f"Ваша реферальная ссылка: {generate_telegram_bot_referral_link(call.from_user.id)}")


def save_wallet(message):
    if message.text == 'Отмена❌':
        bot.send_message(message.chat.id, "🔝 Главное Меню", reply_markup=inline_keyboards.MainMenu())
        bot.send_photo(message.chat.id, photo = Image_Settings.PhotoTake['Welcome'], caption= Message_Settings.MENU_message, parse_mode='Markdown',reply_markup=inline_keyboards.InviteButton())
    else:
        wallet_to_save = message.text
        answer_to_wallet = "Отлично! Вы добавили кошелек: %s\nМы отправим токены $SMILE на данный адрес по окончанию AIRDROP\n\n_Если вы ввели неправильно адрес кошелька, или же хотите его сменить, просто перейдите снова во вкладку Wallet_"%wallet_to_save
        bot.send_message(message.chat.id, answer_to_wallet, parse_mode="Markdown",reply_markup=inline_keyboards.MainMenu())
        UserBoxID = message.chat.id

        sql = "UPDATE users SET Wallet = ? WHERE ID = ?"
        data = (wallet_to_save, UserBoxID)

        # Исполнение запроса UPDATE с использованием контекстного менеджера
        with connection:
            cursor = connection.cursor()
            cursor.execute(sql, data)
            print(cursor.rowcount)  # Возвращает количество затронутых строк

        # Коммит изменений
        connection.commit()


def generate_telegram_bot_referral_link(referral_code):
    return f"https://t.me/testhepler444kaka_bot?start={referral_code}"


bot.infinity_polling()
