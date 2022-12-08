from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Нажми и прими свою судьбу")

b_1 = KeyboardButton(text="\U0001F3A5 ФИЛЬМ")
kb_client.add(b_1)