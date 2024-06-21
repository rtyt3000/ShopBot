from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.user import get_all_users
from handlers.commands import cmd_admin
from keyboards.back_keyboards import back_to_admin_keyboard

router = Router()


class MailingSG(StatesGroup):
    mailing_in_process = State()


@router.callback_query(F.data == 'mailing')
async def call_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите текст рассылки", reply_markup=back_to_admin_keyboard())
    await state.set_state(MailingSG.mailing_in_process)


@router.callback_query(F.data == 'admin')
async def back_admin(call: types.CallbackQuery):
    await cmd_admin(call.message, call.from_user.id)


@router.message(MailingSG.mailing_in_process)
async def mailing_process(message: types.Message, state: FSMContext):
    if message.photo is not None:
        send_photo = True
    else:
        send_photo = False

    users = get_all_users()
    for user in users:
        try:
            if send_photo:
                await message.bot.send_photo(user[0], message.photo[-1].file_id, caption=message.caption)
            else:
                await message.bot.send_message(user[0], message.text)
        except ValueError:
            await message.answer("Введен некорректный текст, попробуйте еще раз")
            return
    await state.clear()
    await message.answer("Рассылка завершена", reply_markup=back_to_admin_keyboard())
