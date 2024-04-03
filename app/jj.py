import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F, filters
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Audio
from aiogram.utils.markdown import hbold
from deep_translator import GoogleTranslator
from app.keyboards import keyboard__, keyboard_return, keyboard_return2, pick_lang
from aiogram.fsm.context import FSMContext
from app.fsm import TranslateFSM


dp = Dispatcher()

data = {}



@dp.message(CommandStart())
async def mesag(message: Message, state: FSMContext):
    keyboard = keyboard__()
    await message.answer(f"Вітаю, {hbold(message.from_user.full_name)}!\nДля початку зайдіть в 'допомогу' та прочтіть як працює бот!\nРобили бота:Artem Perets, Vlad Paschenko", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("help"))
async def help_(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вітаю!\n1. Вам треба написати текст\n"
                                       "2. Вибрати мову або ввести вручну, список мов можете глянути в 'Список мов'\n", reply_markup=keyboard_return())

@dp.callback_query(F.data == 'list')
async def list_(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu' \nКоли вибераєте мову треба писати типу {hbold('uk')} ", reply_markup=keyboard_return2())

@dp.callback_query(F.data == 'return')
async def return_(callback: CallbackQuery, state: FSMContext):
    return await mesag(callback.message, state)

@dp.callback_query(F.data.startswith("translate"))
async def t(callback: CallbackQuery, state: FSMContext) -> None:

    await state.clear()
    await state.set_state(TranslateFSM.text)
    await callback.message.answer(hbold("Напишіть текст"))

@dp.message(TranslateFSM.text)
async def lang1(message: Message, state: FSMContext) -> None:

    await state.update_data(text=message.text)
    #await state.set_state(TranslateFSM.lang_1)
    #await message.answer("Напишіть на яку мову будете переводити!")
    await message.answer("Виберіть на яку мову будете переводити!", reply_markup=pick_lang())

@dp.callback_query(F.data.in_({'uk', 'en', 'de', 'ar'}))
async def translatedef(callback: CallbackQuery, state: FSMContext):
    translateTo = callback.data

    data = await state.get_data()
    translator = GoogleTranslator(source='auto', target=translateTo)
    translate = translator.translate(text=data['text'])

    text = f"ваш текст на {translateTo} буде: {hbold(translate)}"
    print(text)
    await callback.message.answer(text)

@dp.callback_query(F.data == 'other')
async def otherdef(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TranslateFSM.lang_1)
    await callback.message.answer("Напишіть на яку мову будете переводити!")


@dp.message(TranslateFSM.lang_1)
async def c_(message: Message, state: FSMContext) -> None:

    data = await state.update_data(lang_1=message.text)
    translator = GoogleTranslator(source='auto', target=data['lang_1'])
    translate = translator.translate(text=data['text'])
    text = f"ваш текст на {data['lang_1']} буде: {hbold(translate)}"
    print(text)
    await message.answer(text)




TOKEN = "7045509486:AAFnI5jZvg7Qal7b-lVnr0IULwThp3CNw98"
async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






