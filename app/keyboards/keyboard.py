from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def keyboard__():
    keyboard_s = InlineKeyboardBuilder()
    keyboard_s.button(text="Перекладач", callback_data='translate')
    keyboard_s.button(text="Допомога", callback_data='help')
    return keyboard_s.as_markup()

def keyboard_return():
    keyboard_r = InlineKeyboardBuilder()
    keyboard_r.button(text="Список мов", callback_data='list')
    keyboard_r.button(text="Вернутись назад", callback_data='return')
    return keyboard_r.as_markup()

def keyboard_return2():
    keyboard_rr = InlineKeyboardBuilder()
    keyboard_rr.button(text="Вернутись назад", callback_data='return')
    return keyboard_rr.as_markup()

def pick_lang():
    lang_keyboard = InlineKeyboardBuilder()
    lang_keyboard.row(InlineKeyboardButton(text="Українська", callback_data="uk"), InlineKeyboardButton(text="Англійська", callback_data="en"), InlineKeyboardButton(text="Німецька", callback_data="de"), InlineKeyboardButton(text="Арабська", callback_data="ar"))

    #lang_keyboard.button(text="Українська", callback_data="uk")
    #lang_keyboard.button(text="Англійська", callback_data="en")
    #lang_keyboard.button(text="Німецька", callback_data="de")
    #lang_keyboard.button(text="Арабська", callback_data="ar")
    #lang_keyboard.button(text="Ввести вручну", callback_data="other")

    lang_keyboard.row(InlineKeyboardButton(text="Ввести вручну", callback_data="other"))
    return lang_keyboard.as_markup()