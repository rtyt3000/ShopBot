from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.order import get_orders


def profile_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Мои заказы", callback_data="my_orders"),
        InlineKeyboardButton(text="Пополнить баланс", callback_data="add_balance"),
    )
    builder.row(InlineKeyboardButton(text="Назад", callback_data="to_start"))
    return builder.as_markup()


def orders_keyboard(user, page=1):
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    orders = get_orders(user, page)
    for order in orders:
        builder.add(
            InlineKeyboardButton(text=f"Заказ №{order[0]}({order[1]})", callback_data=f"get_order_{order[0]}"),
        )

    try:
        var = get_orders(user, page + 1)[0]
        builder.add(InlineKeyboardButton(text="Вперед", callback_data=f"get_orders_{page + 1}"))
    except Exception as e:
        pass

    if page > 1:
        builder.add(InlineKeyboardButton(text="Назад", callback_data=f"get_orders_{page - 1}"))
    if page == 1:
        builder.add(InlineKeyboardButton(text="В меню", callback_data="profile"))

    return builder.as_markup()


def order_keyboard(order):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Отменить заказ", callback_data=f"cancel_order_{order}"),
        InlineKeyboardButton(text="Выполнено", callback_data=f"done_order_{order}")
    )
    return builder.as_markup()
