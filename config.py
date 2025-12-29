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
            {"id": 2, "name": "Rajabov Abdulxakim Gulomovich", "position": "Boshqaruv raisi o‘rinbosari"},
            {"id": 3, "name": "Kamilov Farxod Abduxamidovich", "position": "Boshqaruv raisi o‘rinbosari"},
            {"id": 4, "name": "Kadirov Nodirxon Abdumo‘minovich", "position": "Boshqaruv raisi o‘rinbosari"},
          # {"id": 5, "name": "Axatov Zafarbek Iskandar o‘g‘li", "position": "Boshqaruv raisining raqamlashtirish va axborot texnologiyalari bo‘yicha o‘rinbosari"},

        ]
    },
}
