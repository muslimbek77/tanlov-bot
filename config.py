import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DATABASE_PATH = "database.db"
VOTING_CLOSED = os.getenv("VOTING_CLOSED", "false").lower() == "true"

NOMINATIONS = {
    "nomination_1": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof boshqaruv raisi o‘rinbosari",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof boshqaruv raisi o‘rinbosari” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "Isaev Qudrat Toshpo‘latovich", "position": "Boshqaruv raisining birinchi o‘rinbosari"},
            {"id": 2, "name": "Axatov Zafarbek Iskandar o‘g‘li", "position": "Boshqaruv raisining raqamlashtirish va axborot texnologiyalari bo‘yicha o‘rinbosari"},
            {"id": 3, "name": "Rajabov Abdulxakim Gulomovich", "position": "Boshqaruv raisi o‘rinbosari"},
            {"id": 4, "name": "Kamilov Farxod Abduxamidovich", "position": "Boshqaruv raisi o‘rinbosari"},
            {"id": 5, "name": "Kadirov Nodirxon Abdumo‘minovich", "position": "Boshqaruv raisi o‘rinbosari"}
        ]
    },
    "nomination_3": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo‘lim boshlig‘i",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo‘lim boshlig‘i” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "Hamidinov Alisher G‘afurovich", "position": "Buxgalteriya hisobi va MXXS yuritish bo‘limi boshlig‘i – bosh hisobchi"},
            {"id": 2, "name": "Majidov Boburjon Mustafo o‘g‘li", "position": "Iqtisodiyot, istiqbolni belgilash va korporativ munosabatlar boshqarmasi boshlig‘i"},
            {"id": 3, "name": "Rahimbabaeva Lola Amurdjanovna", "position": "Personallarni boshqarish va kadrlarni tayyorlash boshqarmasi boshlig‘i"},
            {"id": 4, "name": "Matnazarov O‘g‘aboy Karimovich", "position": "Xaridlarni tashkillashtirish, tartibga solish, monitoring qilish va shartnomalar boshqarmasi boshlig‘i"},
            {"id": 5, "name": "Malikov Temur-Malik Fotihovich", "position": "Yuridik boshqarma boshlig‘i"},
            {"id": 6, "name": "Tursunboyev Farrux Jo‘raboy o‘g‘li", "position": "Korrupsiyaga qarshi kurashish va komplaens nazorat boshqarmasi boshlig‘i"},
            {"id": 7, "name": "Pozdnyakov Aleksandr Alekseyevich", "position": "Arxitektura va boshqaruvni rejalashtirish boshqarmasi boshlig‘i"},
            {"id": 8, "name": "Alimov Otabek Maxmudovich", "position": "Qurilishni mexanizatsiyalashtirish, energetika va mehnat muhofazasi boshqarmasi boshlig‘i"},
            {"id": 9, "name": "Malikov Qobiljon Vasikovich", "position": "Devonxona, ijro nazorati va xo‘jalik ishlari yuritish boshqarmasi boshlig‘i o‘rinbosari"},
            {"id": 10, "name": "Mamadaliyev Abdulmajit Ma’rufjon o‘g‘li", "position": "Raqamlashtirish va AKTni joriy qilish boshqarmasi boshlig‘i o‘rinbosari"},
            {"id": 11, "name": "Pulatov Rustam Nabidjonovich", "position": "Maxsus bo‘lim boshlig‘i"},
            {"id": 12, "name": "Xonkeldiev Davron Inomjonovich", "position": "Ishlab chiqarish va pudrat ishlari boshqarmasi boshlig‘i"}
        ]
    },
    "nomination_2": {
        "title": "Ko‘prikqurilish” AJda — Yilning eng adolatli va shaffof tizim korxonasi rahbari",
        "description": "“Ko‘prikqurilish” AJda “Yilning eng adolatli va shaffof tizim korxonasi rahbari” nominasiyasiga ovoz bering.",
        "candidates": [
            {"id": 1, "name": "Axmedjanov Ulug‘bek Nigmatdjanovich", "position": "13-sonli “Ko‘prikqurilish” otryadi boshlig‘i"},
            {"id": 2, "name": "Ibadullaev Artur Karimovich", "position": "14-sonli “Ko‘prikqurilish” otryadi boshlig‘i"},
            {"id": 3, "name": "Axmedov Ravshan Quchkarovich", "position": "67-sonli “Ko‘prikqurilish” otryadi boshlig‘i"},
            {"id": 4, "name": "Usanov Ilyos Sheralievich", "position": "“1-Ko‘prikqurilish otryadi” MChJ direktori"},
            {"id": 5, "name": "Xonkeldiev Rustamjon Maxammadovich", "position": "“Ko‘prikqurilishbutlash” MChJ direktori"},
            {"id": 6, "name": "Annakulov Anarbay Xudoyberdievich", "position": "“Ko‘prikqurilishfoydalanish” MChJ direktori"},
            {"id": 7, "name": "Djumaniyazov Shuxrat Aminovich", "position": "“Xorazm temir yo‘l qurilish” MChJ direktori"},
            {"id": 8, "name": "Kamalov Azamat Xusniddinovich", "position": "“Ko‘priksifatnazorat” MChJ direktori"},
            {"id": 9, "name": "Ismoilov Dilshodbek Shuxratovich", "position": "“Ko‘prikqurilishtamirlash direksiyasi” MChJ direktori"}
        ]
    }
}

