from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.order import get_order
from db.user import get_user, add_balance
from keyboards.back_keyboards import back_to_profile_keyboard
from keyboards.profile_keyboard import profile_keyboard, orders_keyboard

router = Router()


class AddBalanceSG(StatesGroup):
    adding_in_process = State()


@router.callback_query(F.data == 'profile')
async def call_profile(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user = get_user(call.from_user.id)
    await call.message.edit_text(f"Ваш ID: {user[0]}\nВаш баланс: {user[1]}",
                                 reply_markup=profile_keyboard())
    await state.clear()


@router.callback_query(F.data == 'add_balance')
async def call_add_balance(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите сумму для пополнения баланса", reply_markup=back_to_profile_keyboard())
    await state.set_state(AddBalanceSG.adding_in_process)


@router.message(AddBalanceSG.adding_in_process)
async def add_balance_process(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Введите корректное число")
        return
    except Exception as e:
        await message.answer(f"{e.args}")
        return
    add_balance(message.from_user.id, amount)
    await state.clear()
    await message.answer("Баланс успешно пополнен", reply_markup=back_to_profile_keyboard())


@router.callback_query(F.data == 'my_orders')
async def call_my_orders(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Ваши заказы", reply_markup=orders_keyboard(call.from_user.id))


@router.callback_query(F.data.startswith('get_orders_'))
async def call_get_orders(call: types.CallbackQuery):
    await call.answer()
    page = int(call.data.split('_')[-1])
    await call.message.edit_text("Ваши заказы", reply_markup=orders_keyboard(call.from_user.id, page))


@router.callback_query(F.data.startswith('get_order_'))
async def call_get_order(call: types.CallbackQuery):
    await call.answer()
    order_id = int(call.data.split('_')[-1])
    order = get_order(order_id)
    await call.message.edit_text(f"ID заказа: {order_id}\nID товара: {order[2]}\nСтатус: {order[3]}",
                                 reply_markup=back_to_profile_keyboard())
