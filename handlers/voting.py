from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatMemberStatus

from config import NOMINATIONS
from database import (
    has_voted, add_vote, 
    get_user_votes, add_group_member, is_allowed_group, get_all_groups
)

router = Router()

async def check_user_in_allowed_groups(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi ruxsat berilgan guruhlardan birida a'zo ekanligini tekshirish"""
    groups = await get_all_groups()
    
    for group in groups:
        try:
            member = await bot.get_chat_member(group['chat_id'], user_id)
            if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, 
                                ChatMemberStatus.CREATOR, ChatMemberStatus.RESTRICTED, ChatMemberStatus.CREATOR]:
                # Foydalanuvchini bazaga qo'shish
                await add_group_member(user_id, group['chat_id'], None, None)
                return True
        except Exception as e:
            # Guruhda yo'q yoki xatolik
            continue
    
    return False

@router.message(Command("start"))
async def start_command(message: Message, bot: Bot):
    """Bot boshlanishi"""
    user = message.from_user
    
    # Agar guruhda bo'lsa, foydalanuvchini ro'yxatga olish
    if message.chat.type in ["group", "supergroup"]:
        if await is_allowed_group(message.chat.id):
            await add_group_member(
                user.id, 
                message.chat.id, 
                user.username, 
                user.full_name
            )
            await message.answer(
                f"✅ {user.full_name}, siz guruhga qo'shildingiz!\n\n"
                "Ovoz berish uchun menga shaxsiy xabarda /vote buyrug'ini yuboring."
            )
        return
    
    # Shaxsiy chatda
    text = (
        "🗳 <b>Ko'prikqurilish Tanlov Botiga xush kelibsiz!</b>\n\n"
        "Bu bot orqali siz 3 ta nominatsiyada o'z ovozingizni berishingiz mumkin:\n\n"
        "🏆 <b>1.</b> Yilning eng adolatli va shaffof boshqaruv raisi o'rinbosari\n"
        "🏆 <b>2.</b> Yilning eng adolatli va shaffof tizim korxona rahbari\n"
        "🏆 <b>3.</b> Yilning eng adolatli va shaffof markaziy apparat boshqarma va bo'lim boshlig'i\n\n"
        "📌 Har bir nominatsiyada faqat <b>1 marta</b> ovoz berishingiz mumkin.\n\n"
        "Ovoz berish uchun /vote buyrug'ini bosing."
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🗳 Ovoz berish", callback_data="vote:start")
    kb.button(text="📊 Mening ovozlarim", callback_data="my_votes")
    kb.adjust(1)
    
    await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")

@router.message(Command("vote"))
async def vote_command(message: Message, bot: Bot):
    """Ovoz berish buyrug'i"""
    if message.chat.type != "private":
        await message.answer("❗️ Ovoz berish faqat shaxsiy chatda mumkin!")
        return
    
    # Guruh a'zosi ekanligini tekshirish (Telegram API orqali)
    if not await check_user_in_allowed_groups(bot, message.from_user.id):
        await message.answer(
            "❌ <b>Kechirasiz!</b>\n\n"
            "Ovoz berish uchun avval ruxsat berilgan guruhga a'zo bo'lishingiz kerak.",
            parse_mode="HTML"
        )
        return
    
    await show_nominations(message)

async def show_nominations(message: Message):
    """Nominatsiyalar ro'yxatini ko'rsatish"""
    user_id = message.from_user.id
    user_votes = await get_user_votes(user_id)
    voted_nominations = {v['nomination_key'] for v in user_votes}
    
    short_titles = {
        "nomination_1": "Boshqaruv raisi o'rinbosari",
        "nomination_2": "Tizim korxona rahbari",
        "nomination_3": "Boshqarma/bo'lim boshlig'i"
    }
    
    text = "🗳 <b>TANLOV NOMINATSIYALARI</b>\n\n"
    text += "Ovoz berish uchun nominatsiyani tanlang:\n\n"
    
    kb = InlineKeyboardBuilder()
    
    for i, (nom_key, nomination) in enumerate(NOMINATIONS.items(), 1):
        status = "✅" if nom_key in voted_nominations else "⏳"
        text += f"{status} <b>{i}.</b> {nomination['title']}\n"
        
        short = short_titles.get(nom_key, nomination['title'][:20])
        btn_text = f"{'✅ ' if nom_key in voted_nominations else ''}{i}. {short}"
        kb.button(text=btn_text, callback_data=f"nomination:{nom_key}")
    
    kb.adjust(1)
    
    all_voted = len(voted_nominations) == len(NOMINATIONS)
    if all_voted:
        text += "\n\n🎉 <b>Siz barcha nominatsiyalarda ovoz berdingiz!</b>"
    else:
        text += f"\n\n📊 Ovoz berilgan: {len(voted_nominations)}/{len(NOMINATIONS)}"
    
    await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")

@router.callback_query(F.data == "vote:start")
async def start_voting(callback: CallbackQuery, bot: Bot):
    """Ovoz berishni boshlash"""
    if callback.message.chat.type != "private":
        await callback.answer("❗️ Ovoz berish faqat shaxsiy chatda mumkin!", show_alert=True)
        return
    
    if not await check_user_in_allowed_groups(bot, callback.from_user.id):
        await callback.answer(
            "❌ Avval ruxsat berilgan guruhga a'zo bo'ling!",
            show_alert=True
        )
        return
    
    await show_nominations_callback(callback)

async def show_nominations_callback(callback: CallbackQuery):
    """Nominatsiyalar ro'yxatini ko'rsatish (callback uchun)"""
    user_id = callback.from_user.id
    user_votes = await get_user_votes(user_id)
    voted_nominations = {v['nomination_key'] for v in user_votes}
    
    short_titles = {
        "nomination_1": "Boshqaruv raisi o'rinbosari",
        "nomination_2": "Tizim korxona rahbari",
        "nomination_3": "Boshqarma/bo'lim boshlig'i"
    }
    
    text = "🗳 <b>TANLOV NOMINATSIYALARI</b>\n\n"
    text += "Ovoz berish uchun nominatsiyani tanlang:\n\n"
    
    kb = InlineKeyboardBuilder()
    
    for i, (nom_key, nomination) in enumerate(NOMINATIONS.items(), 1):
        status = "✅" if nom_key in voted_nominations else "⏳"
        text += f"{status} <b>{i}.</b> {nomination['title']}\n"
        
        short = short_titles.get(nom_key, nomination['title'][:20])
        btn_text = f"{'✅ ' if nom_key in voted_nominations else ''}{i}. {short}"
        kb.button(text=btn_text, callback_data=f"nomination:{nom_key}")
    
    kb.adjust(1)
    
    all_voted = len(voted_nominations) == len(NOMINATIONS)
    if all_voted:
        text += "\n\n🎉 <b>Siz barcha nominatsiyalarda ovoz berdingiz!</b>"
    else:
        text += f"\n\n📊 Ovoz berilgan: {len(voted_nominations)}/{len(NOMINATIONS)}"
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("nomination:"))
async def show_candidates(callback: CallbackQuery):
    """Nomzodlar ro'yxatini ko'rsatish"""
    nom_key = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    if nom_key not in NOMINATIONS:
        await callback.answer("❌ Nominatsiya topilmadi!", show_alert=True)
        return
    
    nomination = NOMINATIONS[nom_key]
    
    # Allaqachon ovoz berganligini tekshirish
    if await has_voted(user_id, nom_key):
        await callback.answer("✅ Siz bu nominatsiyada allaqachon ovoz bergansiz!", show_alert=True)
        return
    
    text = f"🏆 <b>{nomination['title']}</b>\n\n"
    text += f"📝 {nomination['description']}\n\n"
    text += "👤 <b>Nomzodlar:</b>\n\n"
    
    kb = InlineKeyboardBuilder()
    
    for candidate in nomination['candidates']:
        text += f"<b>{candidate['id']}.</b> {candidate['name']}\n"
        text += f"   <i>{candidate['position']}</i>\n\n"
        
        kb.button(
            text=f"{candidate['id']}. {candidate['name'][:25]}...",
            callback_data=f"vote:{nom_key}:{candidate['id']}"
        )
    
    kb.button(text="◀️ Orqaga", callback_data="vote:start")
    kb.adjust(1)
    
    text += "\n⚠️ <b>Diqqat:</b> Ovoz berganingizdan keyin uni o'zgartira olmaysiz!"
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("vote:") & ~F.data.in_(["vote:start"]))
async def process_vote(callback: CallbackQuery):
    """Ovozni qayd etish"""
    parts = callback.data.split(":")
    if len(parts) != 3:
        return
    
    _, nom_key, candidate_id = parts
    candidate_id = int(candidate_id)
    user = callback.from_user
    
    if nom_key not in NOMINATIONS:
        await callback.answer("❌ Nominatsiya topilmadi!", show_alert=True)
        return
    
    nomination = NOMINATIONS[nom_key]
    
    # Nomzod borligini tekshirish
    candidate = None
    for c in nomination['candidates']:
        if c['id'] == candidate_id:
            candidate = c
            break
    
    if not candidate:
        await callback.answer("❌ Nomzod topilmadi!", show_alert=True)
        return
    
    # Ovozni saqlash
    success = await add_vote(
        user.id,
        user.username,
        user.full_name,
        nom_key,
        candidate_id
    )
    
    if success:
        await callback.answer("✅ Ovozingiz qabul qilindi!", show_alert=True)
        
        text = (
            f"✅ <b>Ovoz muvaffaqiyatli berildi!</b>\n\n"
            f"🏆 Nominatsiya: {nomination['title']}\n"
            f"👤 Nomzod: {candidate['name']}\n\n"
            f"Rahmat, sizning ovozingiz ahamiyatga ega! 🙏"
        )
        
        kb = InlineKeyboardBuilder()
        kb.button(text="🗳 Boshqa nominatsiyalar", callback_data="vote:start")
        kb.button(text="📊 Mening ovozlarim", callback_data="my_votes")
        kb.adjust(1)
        
        await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    else:
        await callback.answer("❌ Siz bu nominatsiyada allaqachon ovoz bergansiz!", show_alert=True)

@router.callback_query(F.data == "my_votes")
async def show_my_votes(callback: CallbackQuery):
    """Foydalanuvchi ovozlarini ko'rsatish"""
    user_id = callback.from_user.id
    user_votes = await get_user_votes(user_id)
    
    if not user_votes:
        text = "📊 <b>Mening ovozlarim</b>\n\n❌ Siz hali hech qanday ovoz bermagansiz!"
    else:
        text = "📊 <b>Mening ovozlarim</b>\n\n"
        
        for vote in user_votes:
            nom_key = vote['nomination_key']
            candidate_id = vote['candidate_id']
            
            if nom_key in NOMINATIONS:
                nomination = NOMINATIONS[nom_key]
                candidate = None
                for c in nomination['candidates']:
                    if c['id'] == candidate_id:
                        candidate = c
                        break
                
                text += f"🏆 <b>{nomination['title']}</b>\n"
                if candidate:
                    text += f"   👤 {candidate['name']}\n\n"
    
    text += f"\n📈 Jami: {len(user_votes)}/{len(NOMINATIONS)} nominatsiya"
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🗳 Ovoz berish", callback_data="vote:start")
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.message(Command("help"))
async def help_command(message: Message):
    """Yordam"""
    text = (
        "📖 <b>Yordam</b>\n\n"
        "<b>Buyruqlar:</b>\n"
        "/start - Botni boshlash\n"
        "/vote - Ovoz berish\n"
        "/help - Yordam\n\n"
        "<b>Qanday ovoz berish mumkin:</b>\n"
        "1. Avval ruxsat berilgan guruhga a'zo bo'ling\n"
        "2. Guruhda /start buyrug'ini yuboring\n"
        "3. Shaxsiy chatda /vote buyrug'ini bosing\n"
        "4. Nominatsiyani tanlang\n"
        "5. Nomzodga ovoz bering\n\n"
        "⚠️ Har bir nominatsiyada faqat 1 marta ovoz berishingiz mumkin!"
    )
    await message.answer(text, parse_mode="HTML")
