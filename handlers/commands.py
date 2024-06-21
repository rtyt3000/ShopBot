from aiogram import types, Router, F
from aiogram.filters.command import CommandStart, Command

from db.user import add_user, check_admin
from keyboards.admin_keyboard import admin_keyboard
from keyboards.start_keyboard import start_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("Приветствуем! Выберите желаемое действие", reply_markup=start_keyboard())


@router.message(Command("admin"))
async def cmd_admin(message: types.Message, user_id=None):
    if user_id is None:
        user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("Вы администратор", reply_markup=admin_keyboard())
    else:
        await message.answer("У вас нет доступа в этот раздел")


@router.callback_query(F.data == "to_start")
async def call_start(call: types.CallbackQuery):
    await call.message.edit_text("Выберите желаемое действие", reply_markup=start_keyboard())
