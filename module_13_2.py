# Бот Телеги
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['Привет!', 'Отклонение'])
async def text_message(message: types.message):
    if message.text == 'Привет!':
        await message.answer('Привет!')
        print('Привет!')
    elif message.text == 'Отклонение':
        await message.answer('Это отклонение от пути')
        print('Это отклонение от пути')


@dp.message_handler(commands=['start'])
async def command_start(message):
    print('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def other_message(message):
    print("Введите команду /start, чтобы начать общение. ")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
