import telebot
import pymysql
import inline_keyboards
import Message_Settings
import Image_Settings

import sqlite3
connection = sqlite3.connect('telegrambot.db')


with connection:
    cursor = connection.cursor()

    # Создание таблицы users, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        ID INTEGER PRIMARY KEY,
                        Referal TEXT,
                        Balance INTEGER,
                        Wallet TEXT
                    )''')

    connection.commit()

    # После создания таблицы, выполните ваш запрос SELECT
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

bot = telebot.TeleBot("7338083536:AAHqzQenO42JdSAiM5gjgWP-hAQgs8gS4FQ")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat and message.chat.id:
        member = bot.get_chat_member(-1002151936509, message.chat.id)
        #Условия подписки
        if member.status in ['member', 'administrator', 'creator']:
            bot.send_message(message.chat.id, "🔝 Главное Меню", reply_markup=inline_keyboards.MainMenu())
            bot.send_photo(message.chat.id, photo=Image_Settings.PhotoTake['Welcome'], caption=Message_Settings.MENU_message, parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
        else:
            bot.reply_to(message, Message_Settings.WELCOME_message, reply_markup=inline_keyboards.welcome_keys())
    else:
        # Handle case where chat ID is missing or invalid
        bot.reply_to(message, "Invalid chat ID")
@bot.message_handler(func=lambda message: True)
def error_message(message):
    if message.text == 'Условия\\Terms 📃':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Terms'], caption=Message_Settings.Terms_message,parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
    elif message.text == 'Баланс\\Balance 🙂':
        bot.send_photo(message.chat.id, Image_Settings.PhotoTake['Balance'], caption=Message_Settings.Balance_message,parse_mode='Markdown', reply_markup=inline_keyboards.InviteButton())
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
def callback_query(call):
    if call.data == "check":
        #Условия подписки
        UserBoxID = call.message.chat.id
        member = bot.get_chat_member(-1002151936509, UserBoxID)
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



bot.infinity_polling()
