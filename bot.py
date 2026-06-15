# -*- coding: utf-8 -*-
"""
AGENTLAR VIZIT BOTI (professional, mustaqil)
Har kuni soat 8:20 (Toshkent) da bugungi vizit jadvalini batafsil yuboradi.
Buyruqlar: /start /bugun /ertaga /hafta
Eslatma: bu fayl mustaqil - jadval ma'lumoti ichida, qo'shimcha fayl kerak emas.
"""

import os
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

JADVAL = {
    "Dushanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Bog'dod, Rishton",
            "clients": [
                [
                    "Murodjon Aka Bogdod",
                    "C"
                ],
                [
                    "Akram Aka Bogdod",
                    "A"
                ],
                [
                    "Abdunosir Aka Bogdod",
                    "A"
                ],
                [
                    "Erkin Aka Qora Kul",
                    "A"
                ],
                [
                    "Elyor Aka Bogdod",
                    "A"
                ],
                [
                    "Mirza Olim Aka Bogdod",
                    "A"
                ],
                [
                    "Maruf Aka Bogdod",
                    "B"
                ],
                [
                    "Abror Aka Toda Rishton",
                    "A"
                ],
                [
                    "Aziz Aka Beshkapa Yuli Rishton",
                    "A"
                ],
                [
                    "Isroil Aka Rishton",
                    "A"
                ],
                [
                    "Jo'rabek aka Nurafshon",
                    "A"
                ],
                [
                    "Abdumajid aka Yangiqo'rg'on",
                    "A"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "G'urumsaroy, Dangara",
            "clients": [
                [
                    "F57 Nazir aka G'urumsaroy Biora \"B\"",
                    "AAB"
                ],
                [
                    "F54 Yoqubjon aka Naymancha ''B'' PENA",
                    "AAA"
                ],
                [
                    "F59 Oybekaka G'urumsaroy Zamin \"B\"",
                    "AAA"
                ],
                [
                    "F58 Nazir aka G'urumsaroy Vodiy \"C\"",
                    "CBA"
                ],
                [
                    "F47 Nozimaka Oqjar ''B'' PENA",
                    "BBA"
                ],
                [
                    "F56 Faxriddin aka G`urumsaroy \"A\"",
                    "CCA"
                ],
                [
                    "F200 G'iyosjon aka Qirqlar Yangi klent '' PENA ''",
                    "CCA"
                ],
                [
                    "F64 Ahror aka G'urumsaroy \"C\"",
                    "BBA"
                ],
                [
                    "F62 Hasanboy aka G'urumsaroy Roshal/ eco Delta \"B\"",
                    "AAA"
                ],
                [
                    "F94 Rustam aka G'urumsaroy \"A\"",
                    "AAA"
                ],
                [
                    "F44 Ilxom aka Oqjar ''B\" PENA",
                    "AAA"
                ],
                [
                    "F61 Sharofiddin Aka Yangiobod POP \"B\"Bravo Biora Ferre",
                    "AAA"
                ],
                [
                    "F55 Ahadjon aka G'urumsaroy Bravo \"B\"",
                    ""
                ],
                [
                    "F63 Yo'ldoshali aka Pungon eco Gerta \"A\" PENA",
                    "AAA"
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "Qo'qon",
            "clients": [
                [
                    "I98 Royal Market ''B\"",
                    "AAA"
                ],
                [
                    "F57 Nazir aka G'urumsaroy Biora \"B\"",
                    "AAB"
                ],
                [
                    "I90 Hayot ro'para po'k ''C''",
                    "AAB"
                ],
                [
                    "I87 Dilmurodjon aka Ko'l Elash \"X\"",
                    "BBB"
                ],
                [
                    "Donyor aka shaxar parket sentr",
                    "BBB"
                ],
                [
                    "Izzatjon Aka Avg'onbog' \"C\"",
                    "CCA"
                ],
                [
                    "I95 Maqsud aka Megamix market ''A\"",
                    "CCA"
                ],
                [
                    "I92 Jahongir aka Memor ''C''",
                    "CCA"
                ],
                [
                    "Abdullox aka Derizli ''D''",
                    "CCB"
                ],
                [
                    "I97 Raximaka G'oziyog'liq \"80/20 PENA",
                    "BBA"
                ],
                [
                    "I102 Versal Market ''C''",
                    "AAA"
                ],
                [
                    "I80 Anvar aka Naymansoy yo'lii \"B\" Biora",
                    "BCA"
                ],
                [
                    "I156 Muhammadali aka Jomushu \" YANGI \"",
                    ""
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Andijon",
            "clients": []
        }
    },
    "Seshanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Pop, G'urumsaroy, Chust, To'raqo'rg'on",
            "clients": [
                [
                    "Abdurasul Aka Pop",
                    "A"
                ],
                [
                    "Islom Aka Pop",
                    "B"
                ],
                [
                    "Toxir Aka Pop",
                    "B"
                ],
                [
                    "Sharofiddin Aka Pop",
                    "A"
                ],
                [
                    "Nazir Aka Gurim Saroy Vodiy",
                    "A"
                ],
                [
                    "Xasanboy Gurim Saroy",
                    "A"
                ],
                [
                    "Marxabo opa Jomashoy",
                    "B"
                ],
                [
                    "Axror aka gurumsaroy",
                    "B"
                ],
                [
                    "Axad Aka Gurim Saroy",
                    "C"
                ],
                [
                    "Yuldoshali Aka Pungon",
                    "A"
                ],
                [
                    "Nazir Aka Gurim Saroy Biora",
                    "B"
                ],
                [
                    "Muhammadjon aka Jomashuv",
                    "A"
                ],
                [
                    "qaxramon aka tora qurgon",
                    "A"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "Chust, Pop, Namangan",
            "clients": [
                [
                    "F29 Hasanboy aka Chust ''B''",
                    "AAA"
                ],
                [
                    "F35 Yoqubjon aka Chust Bravo \"B\"",
                    "AAB"
                ],
                [
                    "F86 Xurshid aka Pop Humo Biora \"C\" PENA \"X\"",
                    "CCA"
                ],
                [
                    "F76 Abdurasul aka Pop Hilol \"B\"",
                    "AAB"
                ],
                [
                    "F71 Bekzod Aka Namangan Biora Delta \"B\"",
                    "AAA"
                ],
                [
                    "F96 Kamoliddin Aka Chust ''A''",
                    "AAB"
                ],
                [
                    "I156 Muhammadali aka Jomushu \" YANGI \"",
                    ""
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "Bog'dod",
            "clients": [
                [
                    "F90 Mirzaolimjon Aka Bog'dod Gerta ''C''",
                    "BBA"
                ],
                [
                    "F12 Haydarali aka Bog'dod \"B\" (vasko)",
                    "AAA"
                ],
                [
                    "F89 Erkin aka Bog'dod 0533 \"C\"",
                    "BBA"
                ],
                [
                    "F10 Erkin aka Qora ko'l Fendi&Ferre \"B\"",
                    "BBA"
                ],
                [
                    "F7 Bobur aka Bog'dod \"Meros\" (vasko) \"B\"",
                    "BBA"
                ],
                [
                    "F97 Hayot aka Bog'dod \"N\" Pena",
                    "BBB"
                ],
                [
                    "F5 Azamjon aka Bog'dod \"B\" pena",
                    "AAA"
                ],
                [
                    "F17 Otabek aka Bog'dod \"C\"",
                    "AAA"
                ],
                [
                    "F8 Davronjon aka Do'rmoncha Bog'dod \"B\"",
                    "AAA"
                ],
                [
                    "D140 Dilshod Aka Bog'dod \"YUKSAK\" DO'KON",
                    ""
                ],
                [
                    "F2 Abdunosir aka Bog'dod \"B\" Biora",
                    "AAA"
                ],
                [
                    "F3 Ahadjon aka Bog'dod Ultarma \"C\"",
                    "BAA"
                ],
                [
                    "F110 Lochinbek Aka Bog'dod ''C''",
                    ""
                ],
                [
                    "F13 Iqbol aka Bog'dod \"B\" PENA",
                    "AAB"
                ],
                [
                    "Murodullo Aka Bog'dod \"C\" ''PENA''",
                    "AAA"
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Andijon",
            "clients": []
        }
    },
    "Chorshanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Dangara, Qo'qon, Pungon (So'x - har 15 kunda 1 marta)",
            "clients": [
                [
                    "Dilshod Aka Chagali",
                    "A"
                ],
                [
                    "Elmurod Aka Oq Jar Doniyor Aka Oq Jar",
                    "A"
                ],
                [
                    "Sherzod Aka Oq Jar",
                    "A"
                ],
                [
                    "Shoxalandar Aka Telmin",
                    "B"
                ],
                [
                    "Doniyor Aka Aq Jar",
                    "A"
                ],
                [
                    "Shukur Aka Mulkabot",
                    "A"
                ],
                [
                    "Farux Aa Balshivek",
                    "A"
                ],
                [
                    "Bilolxon Dangara",
                    "A"
                ],
                [
                    "Nixol Aka Sox",
                    "A"
                ],
                [
                    "Abduraxmon Aka Sox",
                    "A"
                ],
                [
                    "Sanjar Aka Sox",
                    "B"
                ],
                [
                    "Nasim Aka Sox 24 96",
                    "A"
                ],
                [
                    "Nasim Aka Sox 49 42",
                    "A"
                ],
                [
                    "Oybek Aka Sox",
                    "B"
                ],
                [
                    "Alisher aka so'x",
                    "B"
                ],
                [
                    "Nuriddin Aka Sox",
                    "B"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "Buvayda, Bachqir",
            "clients": [
                [
                    "B108 Islom Aka Buvayda Sobirjon q/i PENA \"B\"",
                    "AAC"
                ],
                [
                    "Iqbol Aka Buvayda ''STROY SENTR'' PENA \"A\"",
                    "AAA"
                ],
                [
                    "B25 Otabek Oq qo'rgon Buvayda \"B\"",
                    "AAA"
                ],
                [
                    "B16 Nodir aka Bachqir \"C\"",
                    "BBA"
                ],
                [
                    "B31 Sanjar aka Buvayda Sobirjon qishlog'i \"C\"",
                    "BBB"
                ],
                [
                    "B29 Zufar aka Buvaydi Miltiqchi Biora \"C\"",
                    "BAA"
                ],
                [
                    "B30 Abbos aka 104 Buvayda \"B\" Hilol PENA",
                    "BBB"
                ],
                [
                    "B13 Farhod aka Bachqir Zamin ''C\" NAQT",
                    "CCA"
                ],
                [
                    "B18 Saidxon aka Bachqir Hilol \"C\"",
                    "AAA"
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "Rishton",
            "clients": [
                [
                    "D66 Doniyor aka Rishton \"C\"",
                    "BBB"
                ],
                [
                    "D71 Islomaka Rishton \"X\"Nikko NAQT",
                    "CCA"
                ],
                [
                    "D99 Ubaydullo Hoji aka Rishton \"B\" PENA",
                    "AAA"
                ],
                [
                    "Baxromjon Aka Rishton Pena Naqt",
                    "CCA"
                ],
                [
                    "D62 Begzod aka Rishton \"C\"",
                    "AAA"
                ],
                [
                    "D80 Odil aka Rishton \"C\"",
                    "BBA"
                ],
                [
                    "Iftixor Aka Rishton ''Naqt''",
                    "CCC"
                ],
                [
                    "D92 Aziz Aka Rishton Beshkapa yo'li \"N\"",
                    "CCC"
                ],
                [
                    "D72 Isroil aka Rishton \"C\" corella PENA",
                    "BBB"
                ],
                [
                    "D64 Bahodir aka Rishton Zohidon``C``",
                    "BBA"
                ],
                [
                    "D84 Shohruh aka Rishton \"C\" Ferre Bravo NAQT",
                    "CCA"
                ],
                [
                    "D57 Akmal aka Rishton To'da \"C\"",
                    "AAC"
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Pop + Chust + Dangara + G'urumsaroy",
            "clients": []
        }
    },
    "Payshanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Buvayda, Uchko'prik, Bachqir",
            "clients": [
                [
                    "Eldor Aka Buvayda",
                    "B"
                ],
                [
                    "Otabek Oq Qurgon",
                    "C"
                ],
                [
                    "Iqbol Aka Buvayda",
                    "A"
                ],
                [
                    "Mir Abdulla Urganji",
                    "C"
                ],
                [
                    "Elyor Aka Qumariq Obod",
                    "A"
                ],
                [
                    "Islom Aka Uch Kuprik",
                    "A"
                ],
                [
                    "Zuxruddin Aka Xon Qiz",
                    "A"
                ],
                [
                    "Said Aka Bachqir",
                    "C"
                ],
                [
                    "Zamzamali Aka Sariq Qurgon",
                    "C"
                ],
                [
                    "Lutfullo Aka Bachqir",
                    "A"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "Uchko'prik, Yangiqo'rg'on",
            "clients": [
                [
                    "B35 Ahrorjon aka Mexrigiyo \"C\"",
                    "BAA"
                ],
                [
                    "B61 Abdumajid aka Yangiqo'rg'on Zamin \"B\" Delta PENA",
                    "AAB"
                ],
                [
                    "B69 Javlonbek Aka Nurafshon Bog'dod \"B\"",
                    "AAA"
                ],
                [
                    "B41 Iqbol aka Uchko'prik Biora \"B\"",
                    "BBB"
                ],
                [
                    "B68 Iqbol aka Yangiqo'rg'on \"C\"",
                    "AAB"
                ],
                [
                    "B53 Xurshid aka Uchkuprik Kattaqashqar \"C\"",
                    "BBA"
                ],
                [
                    "B47 Muslim Aka Katta Qoshtepa \"C\" PENA",
                    "BBA"
                ],
                [
                    "B73 Shavkat aka Yangiqo'rg'on Hilol \"C\"",
                    "BBA"
                ],
                [
                    "B62 Akramjon aka Yangiqo'rg'on Matqulobod \"C\" Korella",
                    "AAA"
                ],
                [
                    "B54 ZamZamAli Aka Sariqqo'rg'on \"B\" PENA",
                    "AAB"
                ],
                [
                    "B49 Qobil aka Sariqo'rg'on ''C''",
                    "BBA"
                ],
                [
                    "B71 Muxriddin aka Matqulobod \"C\"",
                    "BBA"
                ],
                [
                    "B109 Abduvoxid Aka Yangi Qo'rg'on Matqulobod ''Yangi Naqd''",
                    ""
                ],
                [
                    "I156 Muhammadali aka Jomushu \" YANGI \"",
                    ""
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "So'x",
            "clients": [
                [
                    "I145 Abduraxmon Aka So'x 80/20",
                    "AAA"
                ],
                [
                    "B102 Nasim Aka So'x Teppa \"C\" PENA",
                    "AAB"
                ],
                [
                    "I155 Nuriddin aka So'x \"100\" pena",
                    "CCC"
                ],
                [
                    "Sanjar Aka So'x ''Naqt''",
                    "CCC"
                ],
                [
                    "B88 Oybek aka So'x ''C''",
                    "CCC"
                ],
                [
                    "B87 Olimjon Aka So'x \"C\" PENA",
                    "BBA"
                ],
                [
                    "B101 Nixol Aka So'x '' C ''",
                    "BBA"
                ],
                [
                    "I152 SHerzod Aka SO'X ''YANNGI'' NAQT",
                    "CCA"
                ],
                [
                    "I149 Rustam aka Nasim aka So'x Yangi \"100\" pena",
                    "CCA"
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Namangan + To'raqo'rg'on",
            "clients": []
        }
    },
    "Shanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Yaypan, Beshariq, Goriski, Rapqon",
            "clients": [
                [
                    "Anvar Aka Oq Changal",
                    "A"
                ],
                [
                    "Ikrom Aka Goriski",
                    "B"
                ],
                [
                    "Abror Aka Namuna",
                    "A"
                ],
                [
                    "Nozim Aka Besh Ariq",
                    "B"
                ],
                [
                    "Abror Aka Uzboy",
                    "B"
                ],
                [
                    "Abror Aka Tosh Ariq",
                    "A"
                ],
                [
                    "Dovran Aka Besh Ariq",
                    "A"
                ],
                [
                    "Iqbol Aka Tovul",
                    "A"
                ],
                [
                    "Axror Aka Sartol Besh Ariq",
                    "B"
                ],
                [
                    "Fayzullo Aka Rapqon",
                    "A"
                ],
                [
                    "Sardor Aka Yaypan Story Baza",
                    "A"
                ],
                [
                    "Nemat Aka Besh Ariq",
                    "B"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "Goriskiy, Beshariq",
            "clients": [
                [
                    "D24 Ikrom aka Goriskiy \"B\"",
                    "AAB"
                ],
                [
                    "D26 Rahmatillo aka Goriskiy Oqchangal \"C\"",
                    "AAB"
                ],
                [
                    "D5 Davron aka Beshariq ''C'' Zamin Gerta",
                    "BBA"
                ],
                [
                    "D12 Shukur aka Beshariq \"C\" 100",
                    ""
                ],
                [
                    "D18 Sarvar aka Beshariq \"C\" PENA NAQT",
                    "CCA"
                ],
                [
                    "D8 Nematjon aka Beshariq \"C\" NAQT",
                    "CCA"
                ],
                [
                    "D20 Abror aka Goriskiy Yo'li \"NAQT'' PENA",
                    "BBA"
                ],
                [
                    "D2 Abror aka Beshariq Toshariq \"C\" Delta Biora PENA",
                    "BBA"
                ],
                [
                    "D4 Beshariq Uzboy Abror \"B\" Hilol 6.5$PENA",
                    "AAB"
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "Oltiariq, Chimyon",
            "clients": [
                [
                    "I50 G'iyosjon aka Oltiariq \"B\" Best Ferre / Vasko PENA",
                    "AAA"
                ],
                [
                    "I59 Muqumjon aka Oltiariq \"C\" ALFA PENA",
                    "BBA"
                ],
                [
                    "I12 Baxromjon aka Chimyon \"C\"",
                    "BAA"
                ],
                [
                    "I56 Jahongir aka Oltiariq \"B\" Roshal 6.7$_Delta",
                    "AAA"
                ],
                [
                    "I65 Ulug'bek aka Oltiariq \"C\" NAQT",
                    "CCA"
                ],
                [
                    "I16 Sardor aka Chimyon \"B\" Bravo",
                    "BBA"
                ],
                [
                    "I17 Shaxboz aka Xonqiz Muhammadjon aka \"B\"",
                    "AAA"
                ],
                [
                    "I146 Abdulhamid Aka Oltiariq Eski Arab ''80/20''",
                    ""
                ],
                [
                    "Doston Aka Oltiariq ''Pena''",
                    "AAA"
                ],
                [
                    "I55 Ikromaka Oltiariq \"C\" Humio Biora \"HAFTALIK\"",
                    "CCA"
                ],
                [
                    "I9 Abdurahmon aka Chimyon \"B\"Hilo_Fendi",
                    "AAA"
                ],
                [
                    "I62 Oybek aka Oltiariq \"B\" Corella Delta PENA",
                    "AAA"
                ],
                [
                    "I54 Ibrohim aka Oltiariq \"C\" 0090 Nikko",
                    "BBA"
                ],
                [
                    "I60 Muzaffar aka Oltiariq \"B50/50\" Biora Fendi",
                    "BAA"
                ],
                [
                    "I46 Akmal aka Oltiariq \"C\" Rishton yo'lida Xumo",
                    "BBA"
                ],
                [
                    "I58 Mirzoxid aka Oltiariq ''Naxt'' Eski arab X",
                    "CBA"
                ],
                [
                    "I113 Abdulatif aka chimyon \"N\" PENA NAQT",
                    "CCA"
                ],
                [
                    "I49 Boburjon aka Oltiariq 'B\" Formula Nikko",
                    "AAA"
                ],
                [
                    "I200 Azamat aka Qo'r'gon teppa PENA NAQT",
                    ""
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Buvayda + Bachqir + Uchkuprik + Yangiqurg'on",
            "clients": []
        }
    },
    "Yakshanba": {
        "Abduqodir aka": {
            "lavozim": "Concrete agent",
            "region": "Oltiariq, Marg'ilon, Yozyavon",
            "clients": [
                [
                    "Bobur Aka Olti Ariq",
                    "A"
                ],
                [
                    "Joxongir Aka Olti Ariq",
                    "C"
                ],
                [
                    "Muqim Aka Olti Ariq",
                    "B"
                ],
                [
                    "abdulxamid aka oltiarq",
                    "B"
                ],
                [
                    "Mamur Aka Yozyavon",
                    "C"
                ],
                [
                    "Elmurod Aka Yozyavon",
                    "A"
                ],
                [
                    "Ixtiyor Aka Qum Tepa",
                    "B"
                ],
                [
                    "Aziz Aka Qum Tepa",
                    "A"
                ]
            ]
        },
        "Atxamjon aka": {
            "lavozim": "Peno inkassator",
            "region": "Rapqon, Yaypan",
            "clients": [
                [
                    "D49 Fayzullo aka Rapqon ''B''",
                    "AAA"
                ],
                [
                    "D108 G'ayrat aka Yaypan ''B'' VASKO PENA",
                    "AAB"
                ],
                [
                    "D110 Muxammadsolih aka Yaypan ''B''",
                    "AAA"
                ],
                [
                    "D55 Ismoil aka Nursux \"X\" \"CBA\"",
                    ""
                ],
                [
                    "D115 Sardor aka Yaypan 777 ''C'' Zamin eco Humo 6.5$",
                    "CCA"
                ],
                [
                    "D141 Azizbek Aka Rapqon ''NAQD''",
                    ""
                ],
                [
                    "D54 Temur Aka Tagob \"C\"",
                    "BBA"
                ],
                [
                    "D52 Sardor aka Rapqon ''C'' Corella Xumo NAQT",
                    "CCC"
                ]
            ]
        },
        "Abdumalik aka": {
            "lavozim": "Peno agent",
            "region": "Marg'ilon",
            "clients": [
                [
                    "I35 Qobil aka Zarkent ''C\" 1 ta yukka",
                    "AAA"
                ],
                [
                    "I109 Maqsadbek aka Vodil \"A\" pena",
                    "AAA"
                ],
                [
                    "I39 Bekzod Aka Marg'ilon Go'rovoldi Nikko \"B\" PENA",
                    "BBC"
                ],
                [
                    "I121 Muhammadjon aka Marg'ilon \"C\" Izmir",
                    "BBA"
                ],
                [
                    "I37 Sarvar Aka Marg'ilon Yo'li \"C\"",
                    "BBA"
                ],
                [
                    "I2 Begzod aka Avval \"C\"",
                    "BBA"
                ],
                [
                    "I33 Ixtiyor aka Qumtepa \"C\" Humo Biora",
                    "AAA"
                ],
                [
                    "I27 Aziz aka Marg'ilon Qum tepa \"B\" Nikko",
                    "BBA"
                ],
                [
                    "S8 Asilbek aka Qo'shtepa qorajiyda \"C\"",
                    "CBA"
                ],
                [
                    "I31 Fazliddin aka Marg'ilon \"C\"",
                    "BBC"
                ],
                [
                    "I30 Diyor Aka Marg'ilon Zarkent \"C''",
                    "AAA"
                ],
                [
                    "I26 Abdulloh aka Marg'ilon \"B\" Bravo 6.5$",
                    "BAB"
                ],
                [
                    "I156 Muhammadali aka Jomushu \" YANGI \"",
                    ""
                ]
            ]
        },
        "Ibrohimjon aka": {
            "lavozim": "Peno supervizor",
            "region": "Rapqon yayapan Beshariq + Goriski",
            "clients": []
        }
    }
}


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
