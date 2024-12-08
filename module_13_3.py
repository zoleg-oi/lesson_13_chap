# Методы отправки сообщений
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os.path

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


def pecipe(number_recipe):
    # Данная функция возвращает текст рецепта,
    # записанного в файл,
    # в зависимости от выбора меню в чатботе
    if not isinstance(number_recipe, str):
        number_recipe = str(number_recipe)
    number_recipe = number_recipe[1]  # удаляем слэш
    name_file = f'recipe{number_recipe}.txt'  # получаем имя файла
    lines = ''
    if os.path.exists(name_file): # если данный файл существует выводим его содержание, иначе стандартный текст
        with open(name_file, encoding='utf-8') as file:
            for line in file:
                lines += line

    else:
        lines = 'Обратитесь к врачу, не нужно заниматься самолечением'
    return lines


@dp.message_handler(text=['Привет!', 'Отклонение'])
async def text_message(message: types.message):
    if message.text == 'Привет!':
        await message.answer('Привет!')
    elif message.text == 'Отклонение':
        await message.answer('Это отклонение от пути')


@dp.message_handler(commands=['1', '2'])
async def text_recipe(message):
    await message.answer(pecipe(message.text))


@dp.message_handler(commands=['start'])
async def command_start(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.')
    await message.answer('    Нажмите - /1, если вы хотите воспользоваться народныим рецептом')
    await message.answer('    Нажмите - /2, если вы хотите воспользоваться советом врача')


@dp.message_handler()
async def other_message(message):
    await message.answer("Введите команду /start, чтобы начать общение. ")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
