# Клавиатура кнопок
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    gender = State()
    age = State()
    grown = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')
    button_info = InlineKeyboardButton(text='Формулы расчета',callback_data='formulas')
    kb.row(button, button_info)
    await message.answer('Привет! Рассчитаем норму калорий в сутки?', reply_markup = kb)




@dp.callback_query_handler(text='formulas')
async def calculation_formula(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: \n '
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
@dp.callback_query_handler(text='calories')
# Добавлен вопрос о поле человека, так как расчет калорий различен для мужчин и женщин.
async def set_age(message):
    kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
    button_male = KeyboardButton(text='Мужчина')
    button_female = KeyboardButton(text='Женщина')
    kb1.row(button_male, button_female)
    await message.message.answer('Выберете пол', reply_markup=kb1)

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

    if data['gender'] == 'Мужчина':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) + 5, 0
        calories = f'ККалорий в сутки для мужчин: {calories}'
    elif data['gender'] == 'Женщина':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) - 161, 0
        calories = f'ККалорий в сутки для женщин: {calories}'
    else:
        calories = 'Введите правильно свой пол, М(M) - мужчина(male), Ж(F) - женщина(female):'
    await message.answer(calories)
    await state.finish()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите команду - "/start", чтобы подсчитать суточное потребление. ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
