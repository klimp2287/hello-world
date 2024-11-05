import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7554180417:AAEqPUxdNKwHabpsD-QK9nmh44lApEo0z1I")
dp = Dispatcher()
class TeacherContact(StatesGroup):
    message = State()
    fio = State()


kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "/Студент")],
    [KeyboardButton(text = '/Преподаватель')]
], resize_keyboard=True)

kb2 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "/Связь")],
    [KeyboardButton(text = "/Назад")]

], resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветствую. нажмите на вашу должность:",
                         reply_markup=kb)

@dp.message(Command("Преподаватель"))
async def cmd_start(message: types.Message):
    await message.answer("Вы отлично справились ☺️"
                         "\nВам осталось просто ожидать сообщения от студентов."
                         "\nНад их сообщением будет полное наименование группы и их фамилия, имя, а под сообщением будет кнопка ответить."
                         "\nПросто нажмите на нее, пишите ответ студенту и отправляйте!"
                         "\nЖелаем всего наилучшего ❤️")

@dp.message(Command("Студент"))
async def cmd_start(message: types.Message):
    await message.answer("эщкере",reply_markup=kb2)
@dp.message(Command("Назад"))
async def cmd_nazad(message: types.Message):
    await message.answer("Возвращаем",reply_markup=kb)

async def load_users():
    filename = 'users.json'
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"Файл {filename} не найден, создаем новый.")
        return {"teachers": {}}
    except json.JSONDecodeError:
        return {"teachers": {}}
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        return {"teachers": {}}

@dp.message(Command('Связь'))
async def contact_teacher(message: types.Message, state: FSMContext):
    await state.set_state(TeacherContact.fio)
    await message.answer("Введите ФИО преподавателя, с которым хотите связаться.")

@dp.message(TeacherContact.fio)
async def get_teacher_fio(message: types.Message, state: FSMContext):
    await state.update_data(teacher_fio=message.text)
    await state.set_state(TeacherContact.message)
    await message.answer("Теперь введите Ваше сообщение:")


@dp.message(TeacherContact.message)
async def send_message_to_teacher(message: types.Message, state: FSMContext):
    data = await state.get_data()
    teacher_fio = data['teacher_fio']
    student_message = message.text
    users = await load_users()

    teacher_id = None
    for user_id, fio in users['teachers'].items():
        if fio == teacher_fio:
            teacher_id = user_id
            break

    if teacher_id:
        try:
            await bot.send_message(chat_id=teacher_id, text=f"Сообщение от студента: {student_message}")
            await message.answer(f"Ваше сообщение отправлено преподавателю {teacher_fio}.")
        except Exception as e:
            await message.answer(f"Ошибка при отправке сообщения: {e}")
    else:
        await message.answer("Преподаватель с таким ФИО не найден. Пожалуйста, проверьте написание.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())