# Ko'prikqurilish AJ - Tanlov Bot 🗳️

Bu Telegram bot "Ko'prikqurilish" AJ uchun xodimlar tanlovini o'tkazish uchun yaratilgan.


## ✨ Xususiyatlari

### 🗳 Ovoz berish
- **3 ta nominatsiyada ovoz berish:**
  1. Yilning eng adolatli va shaffof boshqaruv raisi o'rinbosari (5 nomzod)
  2. Yilning eng adolatli va shaffof tizim korxona rahbari (10 nomzod)
  3. Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo'lim boshlig'i (12 nomzod)

- Har bir foydalanuvchi har nominatsiyada faqat **1 marta** ovoz bera oladi
- Faqat ruxsat berilgan guruhlardagi a'zolar ovoz bera oladi

### 👥 Guruh boshqaruvi (Admin)
- Guruhlarni tugma orqali tanlash (chat_shared)
- Guruhga havola bilan ko'rsatish
- Guruh a'zoligini Telegram API orqali avtomatik tekshirish

### 📊 PDF Hisobot
- Landscape (gorizontal) formatda chiroyli hisobot
- Bar chart diagrammalar
- To'liq ism-familiyalar (qisqartirilmagan)
- Teng ovozli g'oliblar birgalikda ko'rsatiladi
- G'oliblar ro'yxati

## 🚀 O'rnatish

### 1. Loyihani klonlash

```bash
git clone https://github.com/muslimbek77/tanlov-bot.git
cd tanlov-bot
```

### 2. Virtual muhit yaratish

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# yoki
.venv\Scripts\activate  # Windows
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

- `BOT_TOKEN` - [@BotFather](https://t.me/BotFather) dan olingan token
- `ADMIN_IDS` - Admin Telegram ID lari (vergul bilan ajratilgan)

### 5. Botni ishga tushirish

```bash
python main.py
```

## 📖 Foydalanish

### 👨‍💼 Admin uchun

**Buyruqlar:**

| Buyruq | Tavsif |
|--------|--------|
| `/admin` | Admin panelni ochish |

**Admin panel funksiyalari:**

| Tugma | Tavsif |
|-------|--------|
| ➕ Guruh qo'shish | Yangi guruhni ruxsat etilganlar ro'yxatiga qo'shish |
| 📋 Guruhlar | Ruxsat berilgan guruhlar ro'yxati (havola bilan) |
| 📊 Natijalar | Barcha nominatsiyalar natijalari |
| 📄 PDF yuklash | Chiroyli statistik PDF hisobot |
| 🔄 Ovozlarni tozalash | Barcha ovozlarni o'chirish |
| 📈 Statistika | Umumiy statistika |

### 👤 Foydalanuvchilar uchun

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni boshlash |
| `/vote` | Ovoz berish |
| `/help` | Yordam |

**Ovoz berish tartibi:**
1. Ruxsat berilgan guruhga a'zo bo'ling
2. Botga `/start` buyrug'ini yuboring
3. `/vote` buyrug'ini bosing
4. Nominatsiyani tanlang
5. Nomzodga ovoz bering ✅

## 📁 Loyiha tuzilishi

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
├── .gitignore           # Git ignore
└── README.md            # Hujjatlar
```

## 🛠 Texnologiyalar

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.12+ | Dasturlash tili |
| aiogram | 3.3.0 | Telegram Bot API |
| aiosqlite | 0.19.0 | SQLite ma'lumotlar bazasi |
| matplotlib | 3.8.2 | Diagrammalar |
| reportlab | 4.0.8 | PDF yaratish |

## 📱 BotFather sozlamalari

**Bot haqida:**
```
Ko'prikqurilish AJ tanlov boti. 3 ta nominatsiyada ovoz bering va natijalarni kuzating.
```

**Description:**
```
Ko'prikqurilish AJ xodimlar tanlovini o'tkazish uchun bot. Ovoz bering, natijalarni ko'ring!
```

**Commands:**
```
start - Botni boshlash
vote - Ovoz berish
help - Yordam
admin - Admin panel (faqat adminlar uchun)
```

## 📄 Litsenziya

MIT License

## 👨‍💻 Muallif

Yaratildi: 2025-yil, Dekabr
