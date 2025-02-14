from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message,CallbackQuery,callback_query
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
import app.keyboard as kb
from aiogram import types
import time
import sqlite3

go1 =None
go = None
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT,name TEXT, password INT, balance INT DEFAULT 0, user_id INT ,  element TEXT,user_name TEXT )")
cursor.execute("CREATE TABLE IF NOT EXISTS shop(id INT,name TEXT,price INT,id_tovar INTEGER PRIMARY KEY AUTOINCREMENT)")
db.commit()

router = Router()

class AddTovarStates(StatesGroup):
    name_tovarState = State()
    price_tovarState = State()
    image_tovarState = State()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.chat.id
    name_user = message.from_user.username
    name_user1 = message.from_user.full_name

    # Проверяем, существует ли пользователь
    cursor.execute("SELECT id, balance FROM users WHERE id = ?", (user_id,))
    data2 = cursor.fetchone()
    # Проверяем, существует ли пользователь
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    data1 = cursor.fetchone()

    if data1 is None:
        # Если пользователь не найден, добавляем его
        cursor.execute("INSERT INTO users (user_id,name,user_name) VALUES (?,?,?)", (user_id,name_user1,name_user,))
        db.commit()  # Не забудьте подтвердить изменения


    if data2 is None:
        # Если пользователь не найден, добавляем его с начальным балансом
        initial_balance = 1  # Начальный баланс
        cursor.execute("INSERT INTO users (id, balance) VALUES (?, ?)", (user_id, initial_balance))
        db.commit()  # Не забудьте подтвердить изменения в базе данных
        await message.answer('Приветствую, вы попали в бот кванториума! Ваш баланс инициализирован.', reply_markup=await kb.create_keyboard(user_id))
    else:
        # Если пользователь найден, выводим его баланс и приветственное сообщение
        await message.answer(f'Приветствую, вы попали в бот кванториума! Чем могу помочь?', reply_markup=await kb.create_keyboard(user_id))



#обработка главных кнопок
#
@router.callback_query(F.data == 'shop')
async def hay1(callback: CallbackQuery):
    await callback.answer('Вы перешли в магазин')
    cursor.execute("SELECT name, price,id_tovar FROM shop")
    items = cursor.fetchall()
    if not items:
         await callback.message.edit_text('товара к сожалению не добавлено',reply_markup=kb.back_to1)
    else:
        await callback.message.edit_text('Выберите товар',reply_markup=await kb.create_shop_keyboard(items))
        global go1
        go1 = 0
#
@router.callback_query(F.data == 'profile')
async def hay2(callback: CallbackQuery):
    await callback.answer('Вы перешли в профиль', show_alert=False)
    first_name = callback.from_user.first_name
    user_id = callback.message.chat.id

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT id, balance FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    # Проверяем, есть ли данные
    if not data:  # Если data пустой, значит пользователя нет в базе
        # Вставляем нового пользователя в базу данных с начальным балансом 0
        cursor.execute("INSERT INTO users(name, user_id, balance) VALUES(?, ?, ?)", (first_name, user_id, 0))
        db.commit()  # Сохраняем изменения
    else:
    # Отправляем сообщение с профилем
        await callback.message.edit_text(
            f'ваш профиль\nNick: {first_name}\nid: {user_id}\nbalance: {data[1]}',
            reply_markup=kb.back_to1
        )


#
@router.callback_query(F.data == 'play')
async def hay3(callback: CallbackQuery):
    await callback.answer('Вы начали игру')
    await callback.message.edit_text('Пока доступно прохождение сюжета вы готовы?',reply_markup=kb.yes_or_no)


@router.callback_query(F.data == 'go_exp')
async def back(call:CallbackQuery):
     await call.answer('Твоя учетная запись загружается,готовся воин',show_alert=True)
     await call.message.edit_text('Вы просыпаетесь и не можете понять где вы?',reply_markup=kb.s_l)
     global go
     go = 0
     

@router.callback_query(F.data == 'position1')
async def back(call:CallbackQuery):
     await call.answer('Вы осматриваитесь...')
     await call.message.answer_photo(photo='AgACAgIAAxkBAAIBsWePxqsoeXWl9YmHMfM7wuIPAt2XAAIv7jEbnlaBSIiFXAIttheyAQADAgADeQADNgQ',
                                     caption='Вдруг через мгновение вы видите силуэт человека,Незнакомец стоит и что-то пытается показать',reply_markup=kb.element_go)
     get_go = go + 1
     if get_go == 1:
         await call.message.delete()
     
@router.callback_query(F.data == 'go_element')
async def back(call:CallbackQuery):
     await call.answer('...',)
     await call.message.answer_photo(photo='Неожидано незнакомец падает и из его окровавленых рук падает 4 сферы',
                                     caption='Неожидано незнакомец падает и и его окровавленых рук падает 4 сферы')
     global go
     go = 0


#
@router.callback_query(F.data == 'question')
async def questions(callback: CallbackQuery):
    await callback.answer('Вы перешли в задания')
    await callback.message.answer('как дела?')
#
@router.callback_query(F.data == 'help')
async def hay5(callback: CallbackQuery):
    await callback.answer('Вы перешли в помощь')
    await callback.message.edit_text('Это бот для кванториума пока эта функиция не работает задайте вопросы\n @slippedbisson',reply_markup=kb.back_to1)
# 
#обработка главных кнопок

#админ панель
@router.callback_query(F.data == 'admin_panel')
async def admin(callback: CallbackQuery):
     await callback.answer('Вы выбрали панель администратора')
     await callback.message.edit_text('выберите следующие действие',reply_markup=kb.admin_keyboard)
#админ панель


#обработчик кнопки back
@router.callback_query(F.data == 'back')
async def back(call:CallbackQuery):
     await call.answer('вы перешли назад')
     user_id = call.message.chat.id
     await call.message.edit_text('Приветствую,вы попали в бот кванториума чем могу помочь?',reply_markup=await kb.create_keyboard(user_id))


@router.callback_query(F.data == 'back1')
async def back(call:CallbackQuery):
     await call.answer('вы перешли назад')
     user_id = call.message.chat.id
     await call.message.edit_text('Приветствую,вы попали в бот кванториума чем могу помочь?',reply_markup=await kb.create_keyboard(user_id))

@router.callback_query(F.data == 'back2')
async def back(call:CallbackQuery):
     await call.answer('вы перешли назад')
     await call.message.edit_text('выберите следующие действие',reply_markup=kb.admin_keyboard)

@router.callback_query(F.data == 'back4')
async def back(call:CallbackQuery):
     await call.answer('вы перешли назад')
     user_id = call.message.chat.id
     await call.message.edit_text('Приветствую,вы попали в бот кванториума чем могу помочь?',reply_markup= await kb.create_keyboard(user_id))

@router.callback_query(F.data == 'back3')
async def back(call:CallbackQuery):
     await call.answer('вы перешли назад')
     await call.message.edit_text('выберите следующие действие',reply_markup=kb.admin_keyboard)

@router.callback_query(F.data == 'back5')
async def back(callback: CallbackQuery):
    await callback.answer('Вы вернулись назад')
    await hay1(callback)  # Вызываем hay1, чтобы показать товары снова

@router.callback_query(F.data == 'no_exp')
async def back5(call:CallbackQuery):
     await call.answer('вы перешли назад')
     user_id = call.message.chat.id
     await call.message.edit_text('Приветствую,вы попали в бот кванториума чем могу помочь?',reply_markup= await kb.create_keyboard(user_id))



#обработчик кнопки back

#обработчик get_shop

@router.callback_query(F.data == 'get_shop')
async def get_shop(call: CallbackQuery):
    await call.answer("Вы перешли в регулировку товаров")
    await call.message.edit_text('Добавьте или уберите товар', reply_markup=kb.add_tovar_or_delete)

@router.callback_query(F.data == 'add_tovar')
async def add_tovar(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddTovarStates.name_tovarState)
    await call.message.edit_text('Прошу введите название предмета',reply_markup= None)
    

@router.message(AddTovarStates.name_tovarState)
async def add_tovar2(message: types.Message, state: FSMContext):
    await state.update_data(name_tovar=message.text)
    await state.set_state(AddTovarStates.price_tovarState)
    await message.answer("Введите цену предмета")

@router.message(AddTovarStates.price_tovarState)
async def add_tovar3(message: types.Message, state: FSMContext):
    await state.update_data(price_tovar=message.text)
    user_data = await state.get_data()
    name_tovar = user_data.get('name_tovar')
    price_tovar = user_data.get('price_tovar')
    cursor.execute("INSERT INTO shop(name,price) VALUES(?,?)",(name_tovar,price_tovar,))
    cursor.execute("SELECT name, price,id_tovar FROM shop WHERE name = ? AND price = ?", (name_tovar, price_tovar))
    data = cursor.fetchall()
    item = data[0]
    db.commit()
    await message.answer(f'Товар добавлен:\nНазвание: {item[0]}\nЦена: {item[1]}\nайди товара:{item[2]}',reply_markup=kb.back_t3)
    await state.clear()
    #await state.set_state(AddTovarStates.image_tovarState)
    #await message.answer('Добавьте картинку, отправив изображение.')

#@router.message(AddTovarStates.image_tovarState, content_types=types.ContentType.PHOTO)
##async def add_tovar_image(message: types.Message, state: FSMContext):
    #user_data = await state.get_data()
    #name_tovar = user_data.get('name_tovar')
    #price_tovar = user_data.get('price_tovar')

    # Получаем ID самого высокого качества изображения
    #photo_id = message.photo[-1].file_id  

    # Отправляем сообщение с подтверждением
    #await message.answer(f'Товар добавлен:\nНазвание: {name_tovar}\nЦена: {price_tovar}\nИзображение: {photo_id}')

    # Завершаем состояние
    #await state.finish()  # Лучше использовать finish для завершения состояния


#callback кнопки shop для покупки
@router.callback_query(F.data.startswith('shopboard_'))
async def shopboard(call: CallbackQuery):
        print("Начинаем обработку запроса.")

        # Извлекаем ID товара из callback_data
        item_id = call.data.split('_')[1]  # Предполагается, что ID товара идет после 'shopboard_'
        print(f"Запрашиваем товар с ID: {item_id}")

        # Получаем цену товара по ID
        cursor.execute("SELECT price FROM shop WHERE id_tovar = ?", (item_id,))
        item = cursor.fetchone()

        if item is None:
            await call.message.answer('Товар не найден.')
            return

        price = item[0]  # Извлекаем цену товара из кортежа
        print(f"Цена товара: {price}")
        user_id = call.from_user.id

        # Получаем баланс пользователя
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()

        if data is None:
            await call.message.answer('Пользователь не найден.')
            return

        balance = data[0]  # Извлекаем баланс пользователя из кортежа
        print(f"Баланс пользователя: {balance}")

        # Проверяем, достаточно ли средств
        if balance < price:
            await call.message.edit_text('У вас недостаточно средств.',reply_markup=kb.back_to4)
        else:
            new_balance = balance - price  # Вычитаем цену товара из баланса
            cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))  # Обновляем баланс пользователя
            db.commit()  # Подтверждаем изменения в базе данных

            await call.message.answer(f'Вы купили товар за {price} единиц. Ваш новый баланс: {new_balance}.', reply_markup=kb.back_to1)
            get_go = go1 + 1
            if get_go == 1:
                await call.message.delete()



@router.message(F.text == 'get_1000')
async def get_100(message : Message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,))
    data = cursor.fetchone()
    if data is None:
        await message.answer('Извините, пользователь не был инициализирован!')
        return
    balance = data[0] + 1000
    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ? ",(balance,user_id,))
    await message.answer(f'Ваш баланс обновлен:{balance}')
    db.commit()



@router.message(F.photo)
async def lovphoto(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f'{photo_id}')


@router.callback_query(F.data == 'get_profile')
async def get_profile(call: CallbackQuery):
    await call.answer('вы перешли в просмотр людей')
    cursor.execute("SELECT user_id,name,user_name FROM users")
    users = cursor.fetchall()
    user_list = ''
    for user in users:
        if user[0] is not None:
            user_list += f'\nID:{user[0],user[1],user[2]}'
    if user_list:
        await call.message.edit_text(f'Выберите нужного пользователя:\n{user_list}', reply_markup=kb.back_t3)
    else:
        await call.message.edit_text('Нет пользователей.', reply_markup=kb.back_t3)



