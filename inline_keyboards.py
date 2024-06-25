import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

#Стартовая кнопка для проверки участия в канале
def welcome_keys():
    WelcomeKeyboard = InlineKeyboardMarkup()
    WelcomeKeyboard.row_width = 1
    WelcomeKeyboard.add(InlineKeyboardButton("Проверить✅", callback_data="check"))
    return WelcomeKeyboard

#Основное меню
def MainMenu():
    Menu = ReplyKeyboardMarkup(row_width=8, resize_keyboard=True)
    Menu.row(r'Условия\Terms 📃',r'Баланс\Balance 🙂')
    Menu.row(r'Кошелек\Wallet 👛')
    Menu.row('Terms [ENG] 📌')
    return Menu

def InviteButton():
    ReferalKeyboard = InlineKeyboardMarkup()
    ReferalKeyboard.row_width = 1
    ReferalKeyboard.add(InlineKeyboardButton(r"Пригласить друга \ invite 👥",callback_data='Invite'))
    return ReferalKeyboard

def CancleMenu():
    Cancle = ReplyKeyboardMarkup(row_width=8, resize_keyboard=True)
    Cancle.row('Отмена❌')
    return Cancle