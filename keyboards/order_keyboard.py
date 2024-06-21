from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.products import get_products, get_all_brands, get_all_colors


def order_keyboard(page=1, sort_by=None, brand=None, Color='Чёрный'):
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(InlineKeyboardButton(text="Сортировка", callback_data="sorting"))
    for product in get_products(page, Color, sort_by, brand):
        builder.add(InlineKeyboardButton(text=f"{product[1]} - {int(product[2])}р",
                                         callback_data=f"order_{product[0]}"))
    try:
        var = get_products(page + 1, Color)[0]
        if sort_by == "brand":
            builder.add(InlineKeyboardButton(text="Далее", callback_data=f"page_{page + 1}){Color}_brand_{brand}"))
        else:
            builder.add(InlineKeyboardButton(text="Далее", callback_data=f"page_{page + 1}_{Color}_{sort_by}"))
    except IndexError:
        pass
    if page > 1:
        builder.add(InlineKeyboardButton(text="Назад", callback_data=f"page_{page - 1}_{Color}_{sort_by}"))
    builder.add(InlineKeyboardButton(text="В меню", callback_data="to_start"))
    return builder.as_markup()


def product_accept_keyboard(product_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Заказать", callback_data=f"buy_{product_id}"))
    builder.add(InlineKeyboardButton(text="Отмена", callback_data="order"))
    return builder.as_markup()


def back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="В меню заказа", callback_data="order"))
    return builder.as_markup()


def sorting_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="По возрастанию цены", callback_data="sort_asc"))
    builder.add(InlineKeyboardButton(text="По убыванию цены", callback_data="sort_desc"))
    builder.add(InlineKeyboardButton(text="По бренду", callback_data="sort_brand"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="order"))
    return builder.as_markup()


def brand_choose_keyboard():
    builder = InlineKeyboardBuilder()
    for brand in get_all_brands():
        builder.add(InlineKeyboardButton(text=brand[0], callback_data=f"page_1_brand_{brand[0]}"))

    builder.add(InlineKeyboardButton(text="Назад", callback_data="order"))
    return builder.as_markup()

def color_choose_keyboard():
    builder = InlineKeyboardBuilder()
    for color in get_all_colors():
        print(color)
        builder.add(InlineKeyboardButton(text=color[0], callback_data=f"page_1_color_{color[0]}"))
    return builder.as_markup()