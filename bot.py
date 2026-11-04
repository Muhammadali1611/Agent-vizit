# -*- coding: utf-8 -*-
"""
AGENTLAR HUDUD BOTI
Har kuni soat 8:20 (Toshkent) da haftalik hudud jadvalini RASM qilib yuboradi
(bugungi kun yashil bilan belgilanadi) va tagiga bugungi hududlarni matn bilan yozadi.
Buyruqlar: /start /bugun /ertaga /hafta
Hududlarni o'zgartirish: jadval_rasm.py ichidagi REGION qismi.
"""

import os
import sys
import asyncio
import logging
from datetime import time, datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler

from jadval_rasm import KUNLAR, AGENTLAR, REGION, rasm_yasash

# ============ SOZLAMALAR ============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8950532180:AAEHDGIcobPIr2gMm0zw4c9j27wa5K8BArE")

# 8:20 da xabar keladigan ID lar ro'yxati.
OLUVCHILAR = [
    7242956193,      # siz
    525237955,       # Menejer
]

SOAT, DAQIQA = 8, 20
TZ = ZoneInfo("Asia/Tashkent")
# ====================================

logging.basicConfig(level=logging.INFO)


def kun_nomi(offset=0):
    return KUNLAR[(datetime.now(TZ) + timedelta(days=offset)).weekday()]


def sana(offset=0):
    return (datetime.now(TZ) + timedelta(days=offset)).strftime("%d.%m.%Y")


def matn(kun, sana_txt):
    bosh = f"<b>{kun.upper()} | {sana_txt}</b>\n"
    if kun == "Juma":
        return bosh + "\nBugun dam olish kuni."
    qator = [bosh + "Bugungi agentlar hududi:", ""]
    for i, ag in enumerate(AGENTLAR, 1):
        qator.append(f"{i}. <b>{ag}</b> — {REGION[ag].get(kun, '-')}")
    return "\n".join(qator)


async def rasm_yubor(bot, chat_id, offset=0):
    kun, s = kun_nomi(offset), sana(offset)
    await bot.send_photo(chat_id=chat_id, photo=rasm_yasash(kun, s),
                         caption=matn(kun, s), parse_mode=ParseMode.HTML)


async def start(update, context):
    await update.message.reply_text(
        "Assalomu alaykum. Bu - agentlar hudud jadvali boti.\n\n"
        f"Chat ID: <code>{update.effective_chat.id}</code>\n\n"
        "Buyruqlar:\n/bugun - bugungi jadval\n/ertaga - ertangi jadval\n/hafta - haftalik jadval\n\n"
        "Har kuni soat 8:20 da jadval avtomatik yuboriladi.",
        parse_mode=ParseMode.HTML,
    )


async def bugun(update, context):
    await rasm_yubor(context.bot, update.effective_chat.id, 0)


async def ertaga(update, context):
    await rasm_yubor(context.bot, update.effective_chat.id, 1)


async def hafta(update, context):
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=rasm_yasash(None, None),
                                 caption="Agentlar haftalik hudud jadvali")


async def hammaga_yubor(bot, oluvchilar):
    for oluvchi in oluvchilar:
        try:
            await rasm_yubor(bot, oluvchi, 0)
        except Exception as e:
            logging.warning("Xabar yuborilmadi (%s): %s", oluvchi, e)


async def kunlik_yuborish(context):
    await hammaga_yubor(context.bot, OLUVCHILAR)


async def bir_marta_yuborish(oluvchilar):
    """Railway cron (har kuni 8:20) uchun: rasmni yuboradi va dastur tugaydi."""
    async with Bot(BOT_TOKEN) as bot:
        await hammaga_yubor(bot, oluvchilar)
    logging.info("Kunlik jadval yuborildi, dastur tugadi.")


def main():
    # 1) Cron rejimi: faqat 8:20 xabarini yuborib chiqib ketadi
    if "--send-today" in sys.argv or os.environ.get("BOT_MODE") == "send":
        asyncio.run(bir_marta_yuborish(OLUVCHILAR))
        return
    # Test: faqat birinchi oluvchiga (sizga) yuboradi
    if "--test" in sys.argv:
        asyncio.run(bir_marta_yuborish(OLUVCHILAR[:1]))
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bugun", bugun))
    app.add_handler(CommandHandler("ertaga", ertaga))
    app.add_handler(CommandHandler("hafta", hafta))

    domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if domain:
        # 2) Webhook rejimi (Railway, "uxlash" yoqilgan). 8:20 xabarini cron servis yuboradi.
        url_path = "tg-" + BOT_TOKEN.split(":")[0]
        secret = BOT_TOKEN.split(":")[-1][:32].replace("-", "_")
        logging.info("Bot webhook rejimida: https://%s/%s", domain, url_path)
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", "8080")),
            url_path=url_path,
            webhook_url=f"https://{domain}/{url_path}",
            secret_token=secret,
            allowed_updates=Update.ALL_TYPES,
        )
    else:
        # 3) Lokal/oddiy rejim: polling + 8:20 dagi avtomatik yuborish
        app.job_queue.run_daily(kunlik_yuborish, time=time(hour=SOAT, minute=DAQIQA, tzinfo=TZ), name="kunlik_jadval")
        logging.info("Bot ishga tushdi. Kunlik yuborish: %02d:%02d (Toshkent)", SOAT, DAQIQA)
        app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
