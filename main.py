from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from fastapi import FastAPI, Request
import uvicorn
import os
import asyncio

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Настройки бота
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен из переменной окружения
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Основная клавиатура
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Бетон", callback_data="beton"),
        InlineKeyboardButton(text="Блоки ФБС", callback_data="fbcs")
    )
    builder.row(
        InlineKeyboardButton(text="Полусферы", callback_data="spheres"),
        InlineKeyboardButton(text="Контакты", callback_data="contacts")
    )
    builder.row(
        InlineKeyboardButton(text="Оставить заявку", callback_data="order"),
        InlineKeyboardButton(text="Рассчитать стоимость", url="https://beton61.github.io/monolit/1")
    )
    return builder.as_markup()

# Приветствие
@dp.message(F.text == "/start")
async def start(message):
    text = (
        "✅ Завод бетона в Батайске\n"
        "✔️ Высокое качество ✔️ Низкие цены ✔️ Быстрая доставка\n"
        "Мы предлагаем:\n"
        "🔹 Бетон всех классов\n"
        "🔹 Блоки ФБС\n"
        "🔹 Полусферы для водоёмов\n"
        "🔹 Онлайн-расчёт стоимости\n\n"
        "Выберите нужный пункт ниже 👇"
    )
    await message.reply(text=text, reply_markup=get_main_keyboard())

# Прайс бетона
@dp.callback_query(F.data == "beton")
async def beton(callback):
    text = (
        "📦 Бетон:\n\n"

        "🔹 B7.5 (M100)\n"
        "▫️ Назначение: Подбетонка, подготовительные работы\n"
        "▫️ Цена: от 3 200 ₽/куб.м\n\n"

        "🔹 B10 (M150)\n"
        "▫️ Назначение: Подушки под фундаменты\n"
        "▫️ Цена: от 3 400 ₽/куб.м\n\n"

        "🔹 B15 (M200)\n"
        "▫️ Назначение: Ленточные фундаменты, дорожные покрытия\n"
        "▫️ Цена: от 3 900 ₽/куб.м\n\n"

        "🔹 B20 (M250)\n"
        "▫️ Назначение: Монолитные плиты перекрытия, мелкозаглубленные фундаменты\n"
        "▫️ Цена: от 4 200 ₽/куб.м\n\n"

        "🔹 B25 (M350)\n"
        "▫️ Назначение: Крупногабаритные конструкции, колонны\n"
        "▫️ Цена: от 4 700 ₽/куб.м\n\n"

        "🔹 B30 (M400)\n"
        "▫️ Назначение: Строительство высотных зданий, мостов\n"
        "▫️ Цена: от 5 100 ₽/куб.м\n\n"

        "Чтобы рассчитать точную стоимость — воспользуйтесь кнопкой \"Рассчитать стоимость\"."
    )
    await callback.message.edit_text(text=text, reply_markup=get_main_keyboard())
    await callback.answer()

# Прайс блоков ФБС
@dp.callback_query(F.data == "fbcs")
async def fbcs(callback):
    text = (
        "📦 Блоки ФБС:\n\n"

        "🔹 590х290х188 мм\n"
        "▫️ Назначение: Устройство фундаментов, стен подвалов\n"
        "▫️ Цена: от 1 200 ₽/шт\n\n"

        "🔹 590х290х140 мм\n"
        "▫️ Назначение: Фундаменты малоэтажных домов\n"
        "▫️ Цена: от 1 100 ₽/шт\n\n"

        "🔹 590х290х288 мм\n"
        "▫️ Назначение: Конструкции с повышенной прочностью\n"
        "▫️ Цена: от 1 400 ₽/шт\n\n"

        "🔹 390х290х188 мм\n"
        "▫️ Назначение: Устройство внутренних перегородок\n"
        "▫️ Цена: от 950 ₽/шт\n\n"

        "Для расчёта стоимости — воспользуйтесь кнопкой \"Рассчитать стоимость\"."
    )
    await callback.message.edit_text(text=text, reply_markup=get_main_keyboard())
    await callback.answer()

# Полусферы
@dp.callback_query(F.data == "spheres")
async def spheres(callback):
    text = (
        "🌊 Парковочные полусферы:\n\n"

        "🔹 60 см\n"
        "▫️ Назначение: Декоративные элементы на парковках\n"
        "▫️ Цена: от 2 500 ₽/шт\n\n"

        "🔹 80 см\n"
        "▫️ Назначение: Зонирование парковок, оформление дорог\n"
        "▫️ Цена: от 3 200 ₽/шт\n\n"

        "🔹 1 м\n"
        "▫️ Назначение: Оформление центральных элементов, фонтанов\n"
        "▫️ Цена: от 4 500 ₽/шт\n\n"

        "Можно использовать как отдельные элементы, так и комплекты.\n"
        "Для расчёта стоимости — воспользуйтесь кнопкой \"Рассчитать стоимость\"."
    )
    await callback.message.edit_text(text=text, reply_markup=get_main_keyboard())
    await callback.answer()

# Контакты
@dp.callback_query(F.data == "contacts")
async def contacts(callback):
    text = (
        "📞 Контакты завода:\n"
        "📍 Адрес: г. Батайск, ул. Строителей, д. 12\n"
        "☎️ Телефон: +7 (909) 123-45-67\n"
        "📧 Email: info@bataysk-beton.ru\n"
        "🌐 Сайт: www.bataysk-beton.ru\n\n"
        "Работаем с 8:00 до 18:00, без выходных."
    )
    await callback.message.edit_text(text=text, reply_markup=get_main_keyboard())
    await callback.answer()

# Оставить заявку
@dp.callback_query(F.data == "order")
async def order(callback):
    text = (
        "📝 Чтобы оставить заявку, просто напишите нам:\n"
        "🔹 Какой товар?\n"
        "🔹 Объём или количество\n"
        "🔹 Адрес доставки\n\n"
        "Или нажмите кнопку ниже 👇"
    )
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text="💬 Написать администратору", url=f"https://t.me/Olegzov13"))
    await callback.message.edit_text(text=text, reply_markup=markup.as_markup())
    await callback.answer()

# Создаем FastAPI приложение
app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    update = await request.json()
    await dp.process_update(update)
    return {"status": "ok"}

# Устанавливаем вебхук
WEBHOOK_PATH = "/webhook"

# Установка вебхука
async def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_URL')}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

# Удаление вебхука
async def delete_webhook():
    await bot.delete_webhook()
    print("❌ Webhook удалён")

if __name__ == "__main__":
    # Установим вебхук перед запуском
    asyncio.run(set_webhook())
    uvicorn.run(app, host="0.0.0.0", port=8000)
