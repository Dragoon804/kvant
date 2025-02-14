from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from config import ADMIN_USERS
from aiogram import types 

async def create_keyboard(user_id):
    # Создаем основную клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Магазин', callback_data='shop'),
         InlineKeyboardButton(text='Профиль', callback_data='profile')],
        [InlineKeyboardButton(text='Игра', callback_data='play'),
         InlineKeyboardButton(text='Задания', callback_data='question')],
        [InlineKeyboardButton(text='Помощь', callback_data='help')]
    ])

    # Проверяем, если user_id соответствует определенному значению
    
    if user_id in ADMIN_USERS:  # Замените на нужный ID
        # Добавляем специальную кнопку в одну из строк
        keyboard.inline_keyboard.append([InlineKeyboardButton(text='Панель Администратора', callback_data='admin_panel')])

    return keyboard



admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выдать предметы в магазин', callback_data='get_shop'),
         InlineKeyboardButton(text='Найти профиль человека', callback_data='get_profile')],
        [InlineKeyboardButton(text='Просмотр позиций', callback_data='get_position'),
         InlineKeyboardButton(text='Выдать здания', callback_data='get_question')],
        [InlineKeyboardButton(text='Назад', callback_data='back')]])
  

    
back_to1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= 'Назад',callback_data='back1')]])

back_t3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= 'Назад',callback_data='back3')]])

back_to4 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= 'Назад',callback_data='back5')]])





    # Создаем клавиатуру


async def create_shop_keyboard(items):
    # Создаем клавиатуру с инициализацией inline_keyboard как пустого списка
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for item in items:
        button = InlineKeyboardButton(
            text=f'Предмет: {item[0]}, Цена: {item[1]}',
            callback_data=f'shopboard_{item[2]}'
        )
        # Добавляем каждую кнопку в отдельный список
        keyboard.inline_keyboard.append([button])
    back_btn = (InlineKeyboardButton(text= 'Назад',callback_data='back4'))
    keyboard.inline_keyboard.append([back_btn])
    return keyboard




add_tovar_or_delete =InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить',callback_data='add_tovar'),InlineKeyboardButton(text='Удалить',callback_data='delete_tovar')],
                                                           [InlineKeyboardButton(text= 'Назад',callback_data='back2')]])


yes_or_no = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text ='готов!',callback_data='go_exp'),InlineKeyboardButton(text ='нет',callback_data='no_exp')]])



    
#кнопки игры
s_l = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text ='осмотреться',callback_data='position1'),InlineKeyboardButton(text ='попытаться вспомить хоть что-то',callback_data='belive')]])

element_go = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text ='не шевелится и посмотреть что будет',callback_data='go_element'),InlineKeyboardButton(text ='поверить инстинкту',callback_data='go_go')]])
#кнопки игры
