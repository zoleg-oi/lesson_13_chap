# Методы отправки сообщений
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    gender = State()
    age = State()
    grown = State()
    weight = State()


@dp.message_handler(text='Calories')
# Добавлен вопрос о поле человека, так как расчет калорий различен для мужчин и женщин.
async def set_age(message):
    await message.answer('Введите свой пол, М(M) - мужчина(male), Ж(F) - женщина(female):')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.grown.set()


@dp.message_handler(state=UserState.grown)
async def set_weight(message, state):
    await state.update_data(grown=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # отрабатываем ответ о поле человека, для корректного расчета к.калорий
    if data['gender'] == 'М' or data['gender'] == 'M':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) + 5, 0
        calories = f'ККалорий в сутки для мужчин: {calories}'
    elif data['gender'] == 'Ж' or data['gender'] == 'F':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) - 161, 0
        calories = f'ККалорий в сутки для женщин: {calories}'
    else:
        calories = 'Введите правильно свой пол, М(M) - мужчина(male), Ж(F) - женщина(female):'
    await message.answer(calories)
    await state.finish()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите слово - "Calories", чтобы подсчитать суточное потребление. ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
