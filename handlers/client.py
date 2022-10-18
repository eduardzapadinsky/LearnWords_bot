from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot, dp
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
from handlers.other import synonyms, words_by_level, word_example, word_image, word_audio
from data_bases.sqlite_db import sql_save, sql_delete, sql_read, sql_check
from keyboards.client_kb import keyboard_client, keyboard_client_my_words

translated_message = None


async def command_start(message: types.Message):
    """Команда для старту"""
    await bot.send_message(message.from_user.id, "Hi! Here you can specify the word to study",
                           reply_markup=keyboard_client_my_words)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("word "))
async def button_example_callback(callback: types.CallbackQuery):
    """Інлайн кнопка прикладів застосування слова"""
    examples = word_example(callback.data.replace("word ", ""))
    if examples:
        await callback.message.answer(f"- {examples[0]}\n\n"
                                      f"- {examples[1]}\n\n"
                                      f"- {examples[2]}",
                                      parse_mode="html", reply_markup=keyboard_client)
        await callback.answer()
    else:
        await callback.message.answer(f"<i>There are no examples...</i> Try to make it up by yourself.",
                                      parse_mode="html", reply_markup=keyboard_client)
        await callback.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("image "))
async def button_image_callback(callback: types.CallbackQuery):
    """Інлайн кнопка зображення до слова"""
    image = word_image(callback.data.replace("image ", ""))
    await callback.message.answer_photo(image, reply_markup=keyboard_client)
    await callback.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("audio "))
async def button_example_callback(callback: types.CallbackQuery):
    """Інлайн кнопка озвучення слова"""
    audio = word_audio(callback.data.replace("audio ", ""))
    # audio = open(r"C:\Users\Эдик\Downloads\Telegram Desktop\C0201700.mp3", "rb")
    if audio:
        await callback.message.answer_audio(audio, reply_markup=keyboard_client)
        await callback.answer()
    else:
        await callback.message.answer(f"<i>There is no audio...</i>", parse_mode="html", reply_markup=keyboard_client)
        await callback.answer()


async def command_translate(message: types.Message):
    """Команди для перекладу"""
    global translated_message
    translated_message = GoogleTranslator(source='auto', target='en').translate(message.text)
    level = words_by_level(translated_message.lower())
    cleared_synonyms = synonyms(translated_message)
    if cleared_synonyms and len(cleared_synonyms) >= 3:
        formatted_message_part1 = f"<b><u>{translated_message}</u></b>\n" \
                                  f"{level}\n" \
                                  f"nearby words - {cleared_synonyms[0]}, " \
                                  f"{cleared_synonyms[1]}, " \
                                  f"{cleared_synonyms[2]}"
    else:
        formatted_message_part1 = f"<b><u>{translated_message}</u></b>\n" \
                                  f"{level}"
    dictionary = PyDictionary()
    meaning = dictionary.meaning(translated_message)
    # Створюємо інлайн кнопки
    word_kb = InlineKeyboardMarkup(row_width=1)
    word_button_example = InlineKeyboardButton(text="Examples", callback_data=f"word {translated_message}")
    word_button_audio = InlineKeyboardButton(text="Speech", callback_data=f"audio {translated_message}")
    word_button_image = InlineKeyboardButton(text="Image", callback_data=f"image {translated_message}")
    word_kb.row(word_button_example, word_button_audio, word_button_image)
    # Надсилаємо відповідь
    if meaning is None:
        await bot.send_message(message.from_user.id, f"{formatted_message_part1}\n", parse_mode="html",
                               reply_markup=word_kb)
    else:
        parts_of_speech = list(dictionary.meaning(translated_message).keys())[0]
        meaning = dictionary.meaning(translated_message).get(parts_of_speech)
        await bot.send_message(message.from_user.id, f"{formatted_message_part1}\n"
                                                     f"{parts_of_speech.lower()} - <i>{meaning[0]}</i>",
                               parse_mode="html", reply_markup=word_kb)


async def command_repeat(message: types.Message):
    """Команда для повтору слів"""
    data = {}
    data['id'] = message.from_user.id
    data['word'] = translated_message
    if not sql_check(data):
        await bot.send_message(message.from_user.id, f"word '<b>{translated_message}</b>' is saved", parse_mode="html",
                               reply_markup=keyboard_client_my_words)
        await sql_save(data)
    else:
        await bot.send_message(message.from_user.id, "You have already saved this word before", parse_mode="html",
                               reply_markup=keyboard_client_my_words)


async def command_read(message: types.Message):
    """Команда для виводу слів для повтору"""
    message = message.from_user.id
    await sql_read(message)


async def command_delete(message: types.Message):
    """Команди для видалення вивчених слів"""
    data = {}
    data['id'] = message.from_user.id
    data['word'] = translated_message
    if sql_check(data):
        await bot.send_message(message.from_user.id, "Super!", parse_mode="html",
                               reply_markup=keyboard_client_my_words)
        await sql_delete(data)

    else:
        await bot.send_message(message.from_user.id, f"There wasn't word <b>'{translated_message}'</b> in your words",
                               parse_mode="html", reply_markup=keyboard_client_my_words)


def register_handlers_client(dp: Dispatcher):
    """Реєстрація хендлерів"""
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(command_read, commands=["my_words"])
    dp.register_message_handler(command_repeat, commands=["repeat_it"])
    dp.register_message_handler(command_delete, commands=["I_know_it"])
    dp.register_message_handler(command_translate)
