# -*- coding: utf-8 -*-
"""
AGENTLAR VIZIT BOTI (professional)
Har kuni soat 8:20 (Toshkent) da bugungi vizit jadvalini batafsil yuboradi.
Buyruqlar: /start /bugun /ertaga /hafta
"""

import os
import json
import logging
from datetime import time, datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# ============ SOZLAMALAR ============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8950532180:AAEHDGIcobPIr2gMm0zw4c9j27wa5K8BArE")
MANAGER_CHAT_ID = int(os.environ.get("MANAGER_CHAT_ID", "7242956193"))
SOAT, DAQIQA = 8, 20
TZ = ZoneInfo("Asia/Tashkent")
TG_LIMIT = 4000
# ====================================

logging.basicConfig(level=logging.INFO)

KUNLAR = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
AGENT_TARTIB = ["Abduqodir aka", "Atxamjon aka", "Abdumalik aka", "Ibrohimjon aka"]

with open(os.path.join(os.path.dirname(__file__), "jadval.json"), encoding="utf-8") as f:
    JADVAL = json.load(f)


def chiziq(belgi="-", uzunlik=34):
    return belgi * uzunlik


def hisobot(kun, sana_txt=None):
    bosh = f"<b>{kun.upper()}</b>"
    if sana_txt:
        bosh += f"  |  {sana_txt}"
    bosh += "\n"

    agentlar = JADVAL.get(kun)
    if not agentlar:
        return bosh + "\n" + chiziq("=") + "\nBugun dam olish kuni. Hech bir agent vizitga chiqmaydi."

    qator = [bosh, chiziq("="), "UMUMIY KO'RINISH"]
    chiquvchilar = [a for a in AGENT_TARTIB if a in agentlar]
    qator.append(f"Bugun chiqadigan agentlar: {len(chiquvchilar)} ta")

    jami = 0
    for ag in chiquvchilar:
        info = agentlar[ag]
        n = len(info["clients"])
        jami += n
        belgi = f"[{n} mijoz]" if n else "[region qamrovi]"
        qator.append(f"  - {ag} ({info['lavozim']}) - {info['region']}  {belgi}")
    qator.append(f"Jami mijozlar: {jami}")
    qator.append("")

    for idx, ag in enumerate(chiquvchilar, 1):
        info = agentlar[ag]
        qator.append(chiziq("="))
        qator.append(f"<b>{idx}. {ag.upper()}</b>")
        qator.append(f"Lavozim: {info['lavozim']}")
        qator.append(f"Region: {info['region']}")
        if info["clients"]:
            qator.append(f"Mijozlar ({len(info['clients'])}):")
            for j, (nom, baho) in enumerate(info["clients"], 1):
                baho_txt = f"  [{baho}]" if baho else ""
                qator.append(f"  {j}. {nom}{baho_txt}")
        else:
            qator.append("Mijozlar: region bo'yicha umumiy nazorat (alohida ro'yxat yo'q)")
        qator.append("")

    return "\n".join(qator).rstrip()


def bolib_yubor(matn):
    if len(matn) <= TG_LIMIT:
        return [matn]
    qismlar, joriy = [], ""
    bloklar = matn.split("\n" + chiziq("="))
    for i, blok in enumerate(bloklar):
        if i > 0:
            blok = "\n" + chiziq("=") + blok
        if len(joriy) + len(blok) > TG_LIMIT and joriy:
            qismlar.append(joriy.strip())
            joriy = blok
        else:
            joriy += blok
    if joriy.strip():
        qismlar.append(joriy.strip())
    return qismlar


def kun_nomi(offset=0):
    return KUNLAR[(datetime.now(TZ) + timedelta(days=offset)).weekday()]


def sana(offset=0):
    return (datetime.now(TZ) + timedelta(days=offset)).strftime("%d.%m.%Y")


async def yubor(send_func, matn):
    for qism in bolib_yubor(matn):
        await send_func(qism, parse_mode=ParseMode.HTML)


async def start(update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "Assalomu alaykum. Bu - agentlar kunlik vizit jadvali boti.\n\n"
        f"Chat ID: <code>{chat_id}</code>\n\n"
        "Buyruqlar:\n"
        "/bugun - bugungi batafsil jadval\n"
        "/ertaga - ertangi jadval\n"
        "/hafta - butun hafta\n\n"
        "Har kuni soat 8:20 da jadval avtomatik yuboriladi.",
        parse_mode=ParseMode.HTML,
    )


async def bugun(update, context):
    await yubor(update.message.reply_text, hisobot(kun_nomi(0), sana(0)))


async def ertaga(update, context):
    await yubor(update.message.reply_text, hisobot(kun_nomi(1), sana(1)))


async def hafta(update, context):
    for k in KUNLAR:
        await yubor(update.message.reply_text, hisobot(k))


async def kunlik_yuborish(context):
    matn = hisobot(kun_nomi(0), sana(0))
    for qism in bolib_yubor(matn):
        await context.bot.send_message(chat_id=MANAGER_CHAT_ID, text=qism, parse_mode=ParseMode.HTML)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bugun", bugun))
    app.add_handler(CommandHandler("ertaga", ertaga))
    app.add_handler(CommandHandler("hafta", hafta))
    app.job_queue.run_daily(
        kunlik_yuborish,
        time=time(hour=SOAT, minute=DAQIQA, tzinfo=TZ),
        name="kunlik_jadval",
    )
    logging.info("Bot ishga tushdi. Kunlik yuborish: %02d:%02d (Toshkent)", SOAT, DAQIQA)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
