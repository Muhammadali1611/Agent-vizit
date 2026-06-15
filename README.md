# Agentlar Vizit Boti

Har kuni soat **8:20 (Toshkent vaqti)** da menejerga bugungi agent vizit jadvalini avtomatik yuboradi.

## Buyruqlar
- `/start` — botni ishga tushirish va o'z chat ID ni ko'rish
- `/bugun` — bugungi jadval
- `/ertaga` — ertangi jadval
- `/hafta` — butun hafta jadvali

---

## 1-QADAM: Tayyor
Token va chat ID allaqachon `bot.py` ichiga yozilgan — xabar sizga (Abbosxon) keladi, keyin menejerga forward qilasiz.

## 2-QADAM: Railway ga joylash
1. Bu papkani GitHub repozitoriyaga yuklang (`alimansurov929-lgtm`)
2. [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Deploy tugaydi — bot ishlaydi. Har kuni 8:20 da xabar avtomatik keladi.

> Token/ID ni o'zgartirmoqchi bo'lsangiz: `bot.py` ning yuqorisidagi `BOT_TOKEN` va `MANAGER_CHAT_ID` qatorlarini tahrirlang. Yoki Railway → **Variables** ga `BOT_TOKEN` va `MANAGER_CHAT_ID` qo'shsangiz, ular ustun bo'ladi.

---

> MUHIM: `bot.py`, `jadval.json`, `requirements.txt`, `Procfile` — to'rttasi ham birga yuklanishi shart. `jadval.json` mijozlar ro'yxatini saqlaydi.

## Jadvalni o'zgartirish
`bot.py` ichidagi `JADVAL` qismida region/agentlarni tahrirlang.
Vaqtni o'zgartirish uchun: `SOAT = 8`, `DAQIQA = 20` qatorlarini o'zgartiring.

## Eslatma
- **Juma** kuni hech kim chiqmaydi (dam olish) — bot avtomatik "vizit yo'q" deb yozadi.
- Railway uzluksiz ishlab turishi kerak (bot polling rejimida).
