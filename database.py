import aiosqlite
from config import DATABASE_PATH

async def init_db():
    """Ma'lumotlar bazasini yaratish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Ruxsat berilgan guruhlar jadvali
        await db.execute('''
            CREATE TABLE IF NOT EXISTS allowed_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE NOT NULL,
                chat_title TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ovozlar jadvali
        await db.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                nomination_key TEXT NOT NULL,
                candidate_id INTEGER NOT NULL,
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, nomination_key)
            )
        ''')
        
        # Guruh a'zolari jadvali (ovoz berish huquqi uchun)
        await db.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, chat_id)
            )
        ''')
        
        await db.commit()

async def add_group(chat_id: int, chat_title: str) -> bool:
    """Yangi guruhni qo'shish"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO allowed_groups (chat_id, chat_title) VALUES (?, ?)",
                (chat_id, chat_title)
            )
            await db.commit()
            return True
    except Exception as e:
        print(f"Guruh qo'shishda xato: {e}")
        return False

async def remove_group(chat_id: int) -> bool:
    """Guruhni o'chirish"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("DELETE FROM allowed_groups WHERE chat_id = ?", (chat_id,))
            await db.commit()
            return True
    except Exception as e:
        print(f"Guruh o'chirishda xato: {e}")
        return False

async def get_all_groups() -> list:
    """Barcha guruhlarni olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM allowed_groups") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def is_allowed_group(chat_id: int) -> bool:
    """Guruh ruxsat berilganligini tekshirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT id FROM allowed_groups WHERE chat_id = ?", 
            (chat_id,)
        ) as cursor:
            return await cursor.fetchone() is not None

async def add_group_member(user_id: int, chat_id: int, username: str = None, full_name: str = None):
    """Guruh a'zosini qo'shish"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                """INSERT OR REPLACE INTO group_members 
                   (user_id, chat_id, username, full_name) 
                   VALUES (?, ?, ?, ?)""",
                (user_id, chat_id, username, full_name)
            )
            await db.commit()
    except Exception as e:
        print(f"A'zo qo'shishda xato: {e}")

async def is_group_member(user_id: int) -> bool:
    """Foydalanuvchi ruxsat berilgan guruhda borligini tekshirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            """SELECT gm.id FROM group_members gm
               INNER JOIN allowed_groups ag ON gm.chat_id = ag.chat_id
               WHERE gm.user_id = ?""",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone() is not None

async def add_vote(user_id: int, username: str, full_name: str, 
                   nomination_key: str, candidate_id: int) -> bool:
    """Ovoz qo'shish"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                """INSERT INTO votes 
                   (user_id, username, full_name, nomination_key, candidate_id) 
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, username, full_name, nomination_key, candidate_id)
            )
            await db.commit()
            return True
    except aiosqlite.IntegrityError:
        return False
    except Exception as e:
        print(f"Ovoz berishda xato: {e}")
        return False

async def has_voted(user_id: int, nomination_key: str) -> bool:
    """Foydalanuvchi ovoz berganligini tekshirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT id FROM votes WHERE user_id = ? AND nomination_key = ?",
            (user_id, nomination_key)
        ) as cursor:
            return await cursor.fetchone() is not None

async def get_user_votes(user_id: int) -> list:
    """Foydalanuvchining barcha ovozlarini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM votes WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_votes_by_nomination(nomination_key: str) -> list:
    """Nominatsiya bo'yicha ovozlarni olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT candidate_id, COUNT(*) as vote_count 
               FROM votes WHERE nomination_key = ? 
               GROUP BY candidate_id 
               ORDER BY vote_count DESC""",
            (nomination_key,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_all_votes() -> list:
    """Barcha ovozlarni olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM votes ORDER BY voted_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_total_voters() -> int:
    """Umumiy ovoz berganlar sonini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(DISTINCT user_id) as total FROM votes"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_votes_count_by_nomination(nomination_key: str) -> int:
    """Nominatsiya bo'yicha ovozlar sonini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM votes WHERE nomination_key = ?",
            (nomination_key,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def reset_votes():
    """Barcha ovozlarni o'chirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM votes")
        await db.commit()
