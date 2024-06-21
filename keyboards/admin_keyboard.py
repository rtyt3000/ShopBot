from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Рассылка", callback_data="mailing"),
    )
    builder.add(
        InlineKeyboardButton(text="Назад", callback_data="to_start"),
    )

    return builder.as_markup()
