from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_profile_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data="profile"),
    )

    return builder.as_markup()


def back_to_admin_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Назад", callback_data="admin"),
    )

    return builder.as_markup()
