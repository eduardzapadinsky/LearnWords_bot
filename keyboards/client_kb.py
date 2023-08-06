from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Client Keyboard Buttons
button1 = KeyboardButton("/I_know_it")
button2 = KeyboardButton("/repeat_it")
button3 = KeyboardButton("/my_words")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client_my_words = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(button1, button2)
keyboard_client_my_words.add(button3)
