from aiogram.types import CallbackQuery

from config import bot
from db.products import get_product_by_id
from aiogram import Router, F
from db.order import create_order, change_order_status
from db.user import get_user, add_balance, get_all_admins
from keyboards.back_keyboards import back_to_profile_keyboard
from keyboards.order_keyboard import (order_keyboard, product_accept_keyboard,
                                      back_keyboard, sorting_keyboard, brand_choose_keyboard, color_choose_keyboard)
from keyboards import profile_keyboard

router = Router()


@router.callback_query(F.data == "order")
async def order(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(f"Добро пожаловать, {query.from_user.username}, выберите цвета из списка ниже",
                                  reply_markup=color_choose_keyboard())


@router.callback_query(F.data.startswith("order_"))
async def order_product(query: CallbackQuery):
    await query.answer()
    product_id = query.data.split("_")[1]
    product = get_product_by_id(product_id)
    await query.message.edit_text(f"Вы выбрали: {product[1]} за {int(product[2])}р. ",
                                  reply_markup=product_accept_keyboard(product_id))


@router.callback_query(F.data.startswith("buy_"))
async def accept_product(query: CallbackQuery):
    await query.answer()
    product_id = query.data.split("_")[1]
    product = get_product_by_id(product_id)
    user = get_user(query.from_user.id)
    if user[1] < int(product[2]):
        await query.message.edit_text("У вас недостаточно средств на счету", reply_markup=back_keyboard())
        return
    add_balance(query.from_user.id, -int(product[2]))
    order_id = create_order(query.from_user.id, product_id)
    await query.message.edit_text(f"Вы заказали {product[1]} за {int(product[2])}р. Спасибо за покупку!",
                                  reply_markup=back_keyboard())
    for admin in get_all_admins():
        await bot.send_message(admin[0],
                               f"Пользователь @{query.from_user.username} заказал {product[1]} за {int(product[2])}р.",
                               reply_markup=profile_keyboard.order_keyboard(order_id))


@router.callback_query(F.data.startswith("page_"))
async def page(query: CallbackQuery):
    await query.answer()
    page_number = int(query.data.split("_")[1])
    color = query.data.split("_")[2]
    sort_by = query.data.split("_")[3]
    if sort_by == "brand":
        brand = query.data.split("_")[4]
        await query.message.edit_reply_markup(reply_markup=order_keyboard(page_number,
                                                                          Color=color, sort_by=sort_by, brand=brand))
        return

    await query.message.edit_reply_markup(reply_markup=order_keyboard(page_number, sort_by=sort_by))


@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order(query: CallbackQuery):
    await query.answer()
    order_id = int(query.data.split("_")[-1])
    change_order_status(order_id, "canceled")
    await query.message.edit_text("Заказ отменен", reply_markup=back_to_profile_keyboard())


@router.callback_query(F.data.startswith("done_order_"))
async def done_order(query: CallbackQuery):
    await query.answer()
    order_id = int(query.data.split("_")[-1])
    change_order_status(order_id, "done")
    await query.message.edit_text("Заказ выполнен", reply_markup=back_to_profile_keyboard())


@router.callback_query(F.data == "sorting")
async def sorting(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Выберите сортировку", reply_markup=sorting_keyboard())


@router.callback_query(F.data == "sort_asc")
async def sort_asc(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Сортировка по возрастанию цены", reply_markup=order_keyboard(sort_by="asc"))


@router.callback_query(F.data == "sort_desc")
async def sort_desc(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Сортировка по убыванию цены", reply_markup=order_keyboard(sort_by="desc"))


@router.callback_query(F.data == "sort_brand")
async def sort_brand(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Выберите бренд", reply_markup=brand_choose_keyboard())
