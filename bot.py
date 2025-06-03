import os
import sys
import asyncio
from pathlib import Path
import django
from asgiref.sync import sync_to_async

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command

# Django sozlamalari
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from telefoniya.models import Abonent, Tolov  # Tarif modeli ham kerak bo‘lsa, import qiling

# Bot tokeni (o‘zingizning tokeningizni shu yerga yozing)
API_TOKEN = "7138194585:AAFVQmFMQn2LKyvTzYtFlxBiTn4pZMV3YCE"

# Aiogram sozlamalari
bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# FSM holatlar guruhi
class TolovForm(StatesGroup):
    summa = State()


# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Xush kelibsiz! Abonentlar uchun /abonentlar ni bosing.")


# /abonentlar komandasi
@dp.message(Command("abonentlar"))
async def show_abonentlar(message: Message):
    # Barcha abonentlarni sinxron holatda olishni async-ga aylantiramiz
    abonentlar = await sync_to_async(list)(Abonent.objects.all())
    if not abonentlar:
        await message.answer("Abonentlar topilmadi.")
        return

    # InlineKeyboardMarkup yaratamiz (bo‘sh ro‘yxat bilan)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for a in abonentlar:
        # Modeldagi maydon nomlari: FIO va telefon
        btn = InlineKeyboardButton(
            text=f"{a.FIO} ({a.telefon})",
            callback_data=f"abonent_{a.id}"
        )
        keyboard.inline_keyboard.append([btn])

    await message.answer("📋 Abonentlar ro‘yxati:", reply_markup=keyboard)


# Abonent tanlandi (callback_data = "abonent_<id>")
@dp.callback_query(F.data.startswith("abonent_"))
async def abonent_info(call: CallbackQuery, state: FSMContext):
    abonent_id = call.data.split("_")[1]

    # Abonent obyektini olish (sync_to_async bilan)
    try:
        abonent = await sync_to_async(Abonent.objects.get)(id=abonent_id)
    except Abonent.DoesNotExist:
        await call.message.edit_text("❗️ Abonent topilmadi.")
        return

    # Keyingi bosqichlarda ishlatish uchun abonent_id-ni saqlaymiz
    await state.update_data(abonent_id=abonent.id)

    # Tarif nomini olishni ham async kontekstga o'tkazamiz
    tarif_name = await sync_to_async(lambda: abonent.tarif.nomi if abonent.tarif else "Yoʻq")()

    # Matn ichida modeldagi maydon nomlarini to‘g‘ri ishlatamiz (FIO va telefon)
    status_text = "Aktiv" if abonent.status else "Bloklangan"
    text = (
        f"👤 <b>{abonent.FIO}</b>\n"
        f"📱 Telefon: {abonent.telefon}\n"
        f"📦 Tarif: {tarif_name}\n"
        f"🔘 Status: {status_text}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Toʻlov qoʻshish", callback_data="tolov_qoshish")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="orqaga")]
    ])
    await call.message.edit_text(text, reply_markup=keyboard)


# To‘lov kiritish bosildi
@dp.callback_query(F.data == "tolov_qoshish")
async def tolov_kiritish(call: CallbackQuery, state: FSMContext):
    await call.message.answer("💸 Toʻlov summasini kiriting:")
    await state.set_state(TolovForm.summa)


# Kiritilgan summani qabul qilish
@dp.message(TolovForm.summa)
async def qabul_summa(message: Message, state: FSMContext):
    data = await state.get_data()
    abonent_id = data.get("abonent_id")

    # Foydalanuvchi noto‘g‘ri matn kiritsa, yana so‘raymiz
    try:
        summa = float(message.text.replace(',', '.'))
        if summa <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❗️ Iltimos, musbat sonni kiriting.")
        return

    # Abonentni yana tekshirib olishimiz kerak
    abonent = await sync_to_async(Abonent.objects.filter(id=abonent_id).first)()
    if not abonent:
        await message.answer("❗️ Abonent topilmadi.")
        await state.clear()
        return

    # To‘lovni yaratamiz (sync_to_async bilan)
    await sync_to_async(Tolov.objects.create)(abonent=abonent, summa=summa)
    await message.answer(f"✅ Toʻlov qoʻshildi:\n👤 {abonent.FIO}\n💰 {summa} soʻm")
    await state.clear()


# Orqaga tugmasi bosildi
@dp.callback_query(F.data == "orqaga")
async def qaytish(call: CallbackQuery):
    abonentlar = await sync_to_async(list)(Abonent.objects.all())
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for a in abonentlar:
        btn = InlineKeyboardButton(
            text=f"{a.FIO} ({a.telefon})",
            callback_data=f"abonent_{a.id}"
        )
        keyboard.inline_keyboard.append([btn])
    await call.message.edit_text("📋 Abonentlar ro‘yxati:", reply_markup=keyboard)


# Botni ishga tushirish
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
