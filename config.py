import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DATABASE_PATH = "database.db"

NOMINATIONS = {
    "nomination_1": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof boshqaruv raisi o‘rinbosari",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof boshqaruv raisi o‘rinbosari” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "Boshqaruv raisining birinchi o‘rinbosari", "position": "Isaev Qudrat Toshpo‘latovich"},
            {"id": 2, "name": "Boshqaruv raisining raqamlashtirish va axborot texnologiyalari bo‘yicha o‘rinbosari", "position": "Axatov Zafarbek Iskandar o‘g‘li"},
            {"id": 3, "name": "Boshqaruv raisi o‘rinbosari", "position": "Rajabov Abdulxakim Gulomovich"},
            {"id": 4, "name": "Boshqaruv raisi o‘rinbosari", "position": "Kamilov Farxod Abduxamidovich"},
            {"id": 5, "name": "Boshqaruv raisi o‘rinbosari", "position": "Kadirov Nodirxon Abdumo‘minovich"}
        ]
    },
    "nomination_3": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo‘lim boshlig‘i",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo‘lim boshlig‘i” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "Buxgalteriya hisobi va MXXS yuritish bo‘limi boshlig‘i – bosh hisobchi", "position": "Hamidinov Alisher G‘afurovich"},
            {"id": 2, "name": "Iqtisodiyot, istiqbolni belgilash va korporativ munosabatlar boshqarmasi boshlig‘i", "position": "Majidov Boburjon Mustafo o‘g‘li"},
            {"id": 3, "name": "Personallarni boshqarish va kadrlarni tayyorlash boshqarmasi boshlig‘i", "position": "Rahimbabaeva Lola Amurdjanovna"},
            {"id": 4, "name": "Xaridlarni tashkillashtirish, tartibga solish, monitoring qilish va shartnomalar boshqarmasi boshlig‘i", "position": "Matnazarov O‘g‘aboy Karimovich"},
            {"id": 5, "name": "Yuridik boshqarma boshlig‘i", "position": "Malikov Temur-Malik Fotihovich"},
            {"id": 6, "name": "Korrupsiyaga qarshi kurashish va komplaens nazorat boshqarmasi boshlig‘i", "position": "Tursunboyev Farrux Jo‘raboy o‘g‘li"},
            {"id": 7, "name": "Arxitektura va boshqaruvni rejalashtirish boshqarmasi boshlig‘i", "position": "Pozdnyakov Aleksandr Alekseyevich"},
            {"id": 8, "name": "Qurilishni mexanizatsiyalashtirish, energetika va mehnat muhofazasi boshqarmasi boshlig‘i", "position": "Alimov Otabek Maxmudovich"},
            {"id": 9, "name": "Devonxona, ijro nazorati va xo‘jalik ishlari yuritish boshqarmasi boshlig‘i o‘rinbosari", "position": "Malikov Qobiljon Vasikovich"},
            {"id": 10, "name": "Raqamlashtirish va AKTni joriy qilish boshqarmasi boshlig‘i o‘rinbosari", "position": "Mamadaliyev Abdulmajit Ma’rufjon o‘g‘li"},
            {"id": 11, "name": "Maxsus bo‘lim boshlig‘i", "position": "Pulatov Rustam Nabidjonovich"},
            {"id": 12, "name": "Ishlab chiqarish va pudrat ishlari boshqarmasi boshlig‘i", "position": "Xonkeldiev Davron Inomjonovich"}
        ]
    },
    "nomination_2": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof tizim korxonasi rahbari",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof tizim korxonasi rahbari” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "13-sonli “Ko‘prikqurilish” otryadi boshlig‘i", "position": "Axmedjanov Ulug‘bek Nigmatdjanovich"},
            {"id": 2, "name": "14-sonli “Ko‘prikqurilish” otryadi boshlig‘i", "position": "Ibadullaev Artur Karimovich"},
            {"id": 3, "name": "67-sonli “Ko‘prikqurilish” otryadi boshlig‘i", "position": "Axmedov Ravshan Quchkarovich"},
            {"id": 4, "name": "“1-Ko‘prikqurilish otryadi” MChJ direktori", "position": "Usanov Ilyos Sheralievich"},
            {"id": 5, "name": "“Ko‘prikqurilishbutlash” MChJ direktori", "position": "Xonkeldiev Rustamjon Maxammadovich"},
            {"id": 6, "name": "“Ko‘prikqurilishfoydalanish” MChJ direktori", "position": "Annakulov Anarbay Xudoyberdievich"},
            {"id": 7, "name": "“Xorazm temir yo‘l qurilish” MChJ direktori", "position": "Djumaniyazov Shuxrat Aminovich"},
            {"id": 8, "name": "“Ko‘priksifatnazorat” MChJ direktori", "position": "Kamalov Azamat Xusniddinovich"},
            {"id": 9, "name": "“Ko‘prikqurilishtamirlash direksiyasi” MChJ direktori", "position": "Ismoilov Dilshodbek Shuxratovich"}
        ]
    }
}

