import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Database
DATABASE_PATH = "database.db"

# Nominatsiyalar
NOMINATIONS = {
    "nomination_1": {
        "title": "Yilning eng adolatli va shaffof boshqaruv raisi o'rinbosari",
        "description": '"Ko\'prikqurilish" Ajda "Yilning eng adolatli va shaffof boshqaruv raisi o\'rinbosari" nominatsiyasiga ovoz bering.\nKeling, halollikni qadrlaymiz, halollikni qo\'llab-quvvatlab ularga xolisona ovoz beramiz! Sizning ovozingiz ahamiyatga ega.',
        "candidates": [
            {"id": 1, "name": "Isaev Qudrat Toshpo'latovich", "position": "Boshqaruv raisining birinchi o'rinbosari"},
            {"id": 2, "name": "Rajabov Abdulxakim Gulomovich", "position": "Boshqaruv raisi o'rinbosari"},
            {"id": 3, "name": "Qodirov Nodirxon Abduminovich", "position": "Boshqaruv raisi o'rinbosari"},
            {"id": 4, "name": "Komilov Farxod Abduxamidovich", "position": "Boshqaruv raisi o'rinbosari"},
            {"id": 5, "name": "Axatov Zafarbek Iskandar o'g'li", "position": "Boshqaruv raisi o'rinbosari"},
        ]
    },
    "nomination_2": {
        "title": "Yilning eng adolatli va shaffof tizim korxona rahbari",
        "description": '"Ko\'prikqurilish" Ajda "Yilning eng adolatli va shaffof tizim korxona rahbari" nominatsiyasiga ovoz bering.\nKeling, halollikni qadrlaymiz, halollikni qo\'llab-quvvatlab ularga xolisona ovoz beramiz! Sizning ovozingiz ahamiyatga ega.',
        "candidates": [
            {"id": 1, "name": "Usanov Ilyos Sheralievich", "position": '"1-Ko\'prikqurilish otryadi" MChJ direktori'},
            {"id": 2, "name": "Axmedjanov Ulug'bek Nig'matjanovich", "position": '"13-Ko\'prikqurilish otryadi" boshlig\'i'},
            {"id": 3, "name": "Ibadullaev Artur Karimovich", "position": '"14-Ko\'prikqurilish otryadi" boshlig\'i'},
            {"id": 4, "name": "Axmedov Ravshan Kuchkarovich", "position": '"67-Ko\'prikqurilish otryadi" boshlig\'i'},
            {"id": 5, "name": "Xonkeldiyev Rustamjon Muxammadovich", "position": '"Ko\'prikqurilishbutlash" MChJ direktori'},
            {"id": 6, "name": "Annakulov Anarbay Xudayberdievich", "position": '"Ko\'prikqurilishfoydalanish" MChJ direktori'},
            {"id": 7, "name": "Kamalov Azamat Xusniddinovich", "position": '"Ko\'priksifatnazorat" MChJ direktori'},
            {"id": 8, "name": "Axatov Zafarbek Iskandar o'g'li", "position": '"Ko\'prikqurilishloyiha" MChJ direktori'},
            {"id": 9, "name": "Ismoilov Dilshodbek Shuxratovich", "position": '"Ko\'prikqurilishtamirlashdireksiyasi" MChJ direktori'},
            {"id": 10, "name": "Djumaniyzov Shuxrat Aminovich", "position": '"Xorazm temir yo\'l qurilish" MChJ direktori'},
        ]
    },
    "nomination_3": {
        "title": "Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo'lim boshlig'i",
        "description": '"Ko\'prikqurilish" Ajda "Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo\'lim boshlig\'i" nominatsiyasiga ovoz bering.\nKeling, halollikni qadrlaymiz, halollikni qo\'llab-quvvatlab ularga xolisona ovoz beramiz! Sizning ovozingiz ahamiyatga ega.',
        "candidates": [
            {"id": 1, "name": "Matnazarov Og'aboy Kamirovich", "position": "XT, TS, MQ va Sh boshqarmasi boshlig'i"},
            {"id": 2, "name": "Alimov Otabek Maxmudovich", "position": "QM, E va MM boshqarmasi boshlig'i"},
            {"id": 3, "name": "Pozdnyakov Aleksandr Alekseyevich", "position": "Arxitektura va qurilishni rejalashtirish boshqarmasi boshlig'i"},
            {"id": 4, "name": "Majidov Boburjon Mustafo o'g'li", "position": "Iqtisodiyot va istiqbolni belgilash boshqarmasi boshlig'i"},
            {"id": 5, "name": "Mamadaliyev Abdulmajit Ma'rufjon o'g'li", "position": "R va AKTni joriy qilish boshqarmasi boshliq o'rinbosari"},
            {"id": 6, "name": "Xonkeldiyev Davron Inomjonovich", "position": "Ishlab chiqarish va pudrat ishlari boshqarmasi boshlig'i"},
            {"id": 7, "name": "Malikov Kabildjan Vasikovich", "position": "Devonxona va ijro nazorati boshqarmasi boshlig'i o'rinbosari"},
            {"id": 8, "name": "Tursunbayev Farrux Jurabay o'g'li", "position": "Korrupsiyaga qarshi kurashish boshqarmasi boshlig'i"},
            {"id": 9, "name": "Raximbabayeva Lola Amurdjanovna", "position": "PB va KT boshqarmasi boshlig'i"},
            {"id": 10, "name": "Malikov Temur-Malik Fotixovich", "position": "Yuridik boshqarma boshlig'i"},
            {"id": 11, "name": "Xamidinov Alisher Gafurovich", "position": "Buxgalteriya hisobi va MXXS yuritish bo'limi boshlig'i"},
            {"id": 12, "name": "Pulatov Rustam Nabidjonovich", "position": "Maxsus bo'lim boshlig'i"},
        ]
    }
}
