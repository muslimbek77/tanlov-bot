# Ko'prikqurilish Tanlov Bot

Bu Telegram bot "Ko'prikqurilish" AJ uchun xodimlar tanlovini o'tkazish uchun yaratilgan.

## Xususiyatlari

- 🗳 **3 ta nominatsiyada ovoz berish:**
  1. Yilning eng adolatli va shaffof boshqaruv raisi o'rinbosari
  2. Yilning eng adolatli va shaffof tizim korxona rahbari
  3. Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo'lim boshlig'i

- 👥 **Guruh boshqaruvi:** Admin faqat ruxsat berilgan guruhlardagi a'zolarga ovoz berish huquqini berishi mumkin

- 📊 **Natijalar:** Chiroyli diagrammalar bilan PDF formatda hisobot

- 🔒 **Xavfsizlik:** Har bir foydalanuvchi har nominatsiyada faqat 1 marta ovoz bera oladi

## O'rnatish

### 1. Loyihani klonlash

```bash
git clone <repo-url>
cd tanlov-bot
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Sozlamalar

`.env.example` faylidan `.env` fayl yarating:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
```

- `BOT_TOKEN` - @BotFather dan olingan token
- `ADMIN_IDS` - Admin Telegram ID lari (vergul bilan ajratilgan)

### 5. Botni ishga tushirish

```bash
python main.py
```

## Foydalanish

### Admin uchun

| Buyruq | Tavsif |
|--------|--------|
| `/admin` | Admin panelni ochish |
| `/addgroup` | Guruhni ruxsat berilganlar ro'yxatiga qo'shish (guruhda ishlatiladi) |
| `/removegroup` | Guruhni ro'yxatdan o'chirish (guruhda ishlatiladi) |

**Admin panel funksiyalari:**
- 📋 Guruhlar ro'yxati - ruxsat berilgan guruhlarni ko'rish
- 📊 Natijalar - barcha nominatsiyalar natijalari
- 📄 PDF yuklash - chiroyli statistik hisobot
- 🔄 Ovozlarni tozalash - barcha ovozlarni o'chirish
- 📈 Statistika - umumiy statistika

### Foydalanuvchilar uchun

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni boshlash |
| `/vote` | Ovoz berish |
| `/help` | Yordam |

**Ovoz berish tartibi:**
1. Ruxsat berilgan guruhga a'zo bo'ling
2. Guruhda `/start` buyrug'ini yuboring
3. Bot shaxsiy chatiga o'ting
4. `/vote` buyrug'ini bosing
5. Nominatsiyani tanlang
6. Nomzodga ovoz bering

## Loyiha tuzilishi

```
tanlov-bot/
├── main.py              # Asosiy bot fayli
├── config.py            # Sozlamalar va nominatsiyalar
├── database.py          # Ma'lumotlar bazasi funksiyalari
├── pdf_generator.py     # PDF hisobot generatori
├── handlers/
│   ├── __init__.py
│   ├── admin.py         # Admin handlerlar
│   └── voting.py        # Ovoz berish handlerlar
├── requirements.txt     # Python kutubxonalari
├── .env.example         # Namuna sozlamalar
└── README.md           # Hujjatlar
```

## Texnologiyalar

- **aiogram 3.x** - Telegram Bot API
- **aiosqlite** - SQLite ma'lumotlar bazasi
- **matplotlib** - Diagrammalar
- **reportlab** - PDF yaratish

## Litsenziya

MIT License
