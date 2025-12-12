from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import KeyboardButtonRequestChat
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from config import ADMIN_IDS, NOMINATIONS
from database import (
    add_group, remove_group, get_all_groups, 
    get_votes_by_nomination, get_total_voters, 
    get_votes_count_by_nomination, reset_votes, get_all_votes
)
from pdf_generator import generate_results_pdf

router = Router()

def is_admin(user_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return user_id in ADMIN_IDS

def get_admin_keyboard():
    """Admin panel tugmalari"""
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Guruh qo'shish", callback_data="admin:add_group")
    kb.button(text="➖ Guruh o'chirish", callback_data="admin:remove_group")
    kb.button(text="📋 Guruhlar ro'yxati", callback_data="admin:groups")
    kb.button(text="📊 Natijalar", callback_data="admin:results")
    kb.button(text="📄 PDF yuklash", callback_data="admin:pdf")
    kb.button(text="🔄 Ovozlarni tozalash", callback_data="admin:reset")
    kb.button(text="📈 Statistika", callback_data="admin:stats")
    kb.adjust(2)
    return kb.as_markup()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Admin panel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    await message.answer(
        "🔐 <b>Admin Panel</b>\n\n"
        "Quyidagi amallardan birini tanlang:",
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin:add_group")
async def request_add_group(callback: CallbackQuery):
    """Guruh qo'shish uchun so'rov"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    # Guruh tanlash tugmasi
    kb = ReplyKeyboardBuilder()
    kb.button(
        text="📋 Guruhni tanlang",
        request_chat=KeyboardButtonRequestChat(
            request_id=1,
            chat_is_channel=False,
            chat_is_forum=False,
            chat_has_username=False,
            chat_is_created=False,
            bot_is_member=True
        )
    )
    kb.button(text="❌ Bekor qilish")
    kb.adjust(1)
    
    await callback.message.answer(
        "📋 <b>Guruh qo'shish</b>\n\n"
        "Quyidagi tugmani bosib, qo'shmoqchi bo'lgan guruhni tanlang.\n\n"
        "⚠️ Bot o'sha guruhga a'zo bo'lishi kerak!",
        reply_markup=kb.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "admin:remove_group")
async def request_remove_group(callback: CallbackQuery):
    """Guruh o'chirish uchun ro'yxat"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    groups = await get_all_groups()
    
    if not groups:
        await callback.answer("❌ Hech qanday guruh qo'shilmagan!", show_alert=True)
        return
    
    kb = InlineKeyboardBuilder()
    for group in groups:
        kb.button(
            text=f"🗑 {group['chat_title'][:30]}",
            callback_data=f"remove_group:{group['chat_id']}"
        )
    kb.button(text="◀️ Orqaga", callback_data="admin:back")
    kb.adjust(1)
    
    await callback.message.edit_text(
        "🗑 <b>Guruh o'chirish</b>\n\n"
        "O'chirmoqchi bo'lgan guruhni tanlang:",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

# Guruh tanlanganda (chat_shared)
@router.message(F.chat_shared)
async def handle_chat_shared(message: Message):
    """Tanlangan guruhni qo'shish"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!", reply_markup=ReplyKeyboardRemove())
        return
    
    chat_id = message.chat_shared.chat_id
    request_id = message.chat_shared.request_id
    
    if request_id == 1:  # Guruh qo'shish
        # Guruh nomini olishga harakat qilamiz
        try:
            chat = await message.bot.get_chat(chat_id)
            chat_title = chat.title or f"Guruh {chat_id}"
        except:
            chat_title = f"Guruh {chat_id}"
        
        success = await add_group(chat_id, chat_title)
        
        if success:
            await message.answer(
                f"✅ <b>Guruh muvaffaqiyatli qo'shildi!</b>\n\n"
                f"📌 Guruh: {chat_title}\n"
                f"🆔 ID: <code>{chat_id}</code>",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "❌ Guruh qo'shishda xatolik yuz berdi!",
                reply_markup=ReplyKeyboardRemove()
            )
        
        # Admin panelni ko'rsatish
        await message.answer(
            "🔐 <b>Admin Panel</b>\n\n"
            "Quyidagi amallardan birini tanlang:",
            reply_markup=get_admin_keyboard(),
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("remove_group:"))
async def confirm_remove_group(callback: CallbackQuery):
    """Guruh o'chirishni tasdiqlash"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    chat_id = int(callback.data.split(":")[1])
    
    # Guruh nomini olish
    groups = await get_all_groups()
    group_title = "Noma'lum"
    for g in groups:
        if g['chat_id'] == chat_id:
            group_title = g['chat_title']
            break
    
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Ha, o'chirish", callback_data=f"confirm_remove:{chat_id}")
    kb.button(text="❌ Bekor qilish", callback_data="admin:remove_group")
    kb.adjust(2)
    
    await callback.message.edit_text(
        f"⚠️ <b>Tasdiqlash</b>\n\n"
        f"<b>{group_title}</b> guruhini o'chirishni xohlaysizmi?\n\n"
        f"🆔 ID: <code>{chat_id}</code>",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_remove:"))
async def execute_remove_group(callback: CallbackQuery):
    """Guruhni o'chirish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    chat_id = int(callback.data.split(":")[1])
    success = await remove_group(chat_id)
    
    if success:
        await callback.answer("✅ Guruh muvaffaqiyatli o'chirildi!", show_alert=True)
    else:
        await callback.answer("❌ Guruh o'chirishda xatolik!", show_alert=True)
    
    # Admin panelga qaytish
    await callback.message.edit_text(
        "🔐 <b>Admin Panel</b>\n\n"
        "Quyidagi amallardan birini tanlang:",
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )

@router.message(F.text == "❌ Bekor qilish")
async def cancel_action(message: Message):
    """Amalni bekor qilish"""
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "🔐 <b>Admin Panel</b>\n\n"
        "Quyidagi amallardan birini tanlang:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await message.answer(
        "Quyidagi amallardan birini tanlang:",
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin:groups")
async def show_groups(callback: CallbackQuery, bot: Bot):
    """Guruhlar ro'yxatini ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    groups = await get_all_groups()
    
    if not groups:
        text = "📋 <b>Ruxsat berilgan guruhlar</b>\n\n❌ Hech qanday guruh qo'shilmagan!"
    else:
        text = "📋 <b>Ruxsat berilgan guruhlar</b>\n\n"
        for i, group in enumerate(groups, 1):
            # Guruh linkini olishga harakat qilish
            try:
                chat = await bot.get_chat(group['chat_id'])
                link = None
                
                # 1. Agar guruhda username bo'lsa
                if chat.username:
                    link = f"https://t.me/{chat.username}"
                # 2. Agar mavjud invite_link bo'lsa
                elif chat.invite_link:
                    link = chat.invite_link
                # 3. Yangi link yaratishga harakat
                else:
                    try:
                        link = await bot.export_chat_invite_link(group['chat_id'])
                    except:
                        link = None
                
                text += f"{i}. <b>{chat.title or group['chat_title']}</b>\n"
                text += f"   🆔 <code>{group['chat_id']}</code>\n"
                if link:
                    text += f"   🔗 {link}\n\n"
                else:
                    text += f"   ⚠️ <i>Link uchun botni admin qiling</i>\n\n"
            except Exception as e:
                text += f"{i}. <b>{group['chat_title']}</b>\n"
                text += f"   🆔 <code>{group['chat_id']}</code>\n"
                text += f"   ❌ <i>Guruh topilmadi yoki bot chiqarilgan</i>\n\n"
    
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Guruh qo'shish", callback_data="admin:add_group")
    kb.button(text="➖ Guruh o'chirish", callback_data="admin:remove_group")
    kb.button(text="◀️ Orqaga", callback_data="admin:back")
    kb.adjust(2)
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin:results")
async def show_results(callback: CallbackQuery):
    """Natijalarni ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    text = "📊 <b>TANLOV NATIJALARI</b>\n\n"
    
    for nom_key, nomination in NOMINATIONS.items():
        text += f"🏆 <b>{nomination['title']}</b>\n"
        text += "─" * 30 + "\n"
        
        votes = await get_votes_by_nomination(nom_key)
        total = await get_votes_count_by_nomination(nom_key)
        
        if not votes:
            text += "❌ Hali ovoz berilmagan\n\n"
            continue
        
        votes_dict = {v['candidate_id']: v['vote_count'] for v in votes}
        
        for candidate in nomination['candidates']:
            vote_count = votes_dict.get(candidate['id'], 0)
            percentage = (vote_count / total * 100) if total > 0 else 0
            bar = "█" * int(percentage / 10) + "░" * (10 - int(percentage / 10))
            text += f"{candidate['id']}. {candidate['name']}\n"
            text += f"   {bar} {vote_count} ({percentage:.1f}%)\n"
        
        text += f"\n📊 Jami ovozlar: {total}\n\n"
    
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Orqaga", callback_data="admin:back")
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin:pdf")
async def send_pdf(callback: CallbackQuery):
    """PDF yuklash"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    await callback.answer("📄 PDF tayyorlanmoqda...", show_alert=False)
    
    try:
        pdf_path = await generate_results_pdf()
        
        from aiogram.types import FSInputFile
        pdf_file = FSInputFile(pdf_path, filename="tanlov_natijalari.pdf")
        
        await callback.message.answer_document(
            pdf_file,
            caption="📊 <b>Tanlov natijalari</b>\n\nYuqoridagi PDF faylda batafsil statistika mavjud.",
            parse_mode="HTML"
        )
        
        # PDF faylni o'chirish
        import os
        os.remove(pdf_path)
        
    except Exception as e:
        await callback.message.answer(f"❌ PDF yaratishda xatolik: {str(e)}")

@router.callback_query(F.data == "admin:reset")
async def confirm_reset(callback: CallbackQuery):
    """Ovozlarni tozalashni tasdiqlash"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Ha, tozalash", callback_data="admin:reset_confirm")
    kb.button(text="❌ Bekor qilish", callback_data="admin:back")
    kb.adjust(2)
    
    await callback.message.edit_text(
        "⚠️ <b>DIQQAT!</b>\n\n"
        "Barcha ovozlar o'chiriladi. Bu amalni qaytarib bo'lmaydi!\n\n"
        "Davom etasizmi?",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "admin:reset_confirm")
async def reset_all_votes(callback: CallbackQuery):
    """Barcha ovozlarni o'chirish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    await reset_votes()
    
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Orqaga", callback_data="admin:back")
    
    await callback.message.edit_text(
        "✅ <b>Barcha ovozlar muvaffaqiyatli o'chirildi!</b>",
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "admin:stats")
async def show_stats(callback: CallbackQuery):
    """Statistikani ko'rsatish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    total_voters = await get_total_voters()
    groups = await get_all_groups()
    all_votes = await get_all_votes()
    
    text = "📈 <b>STATISTIKA</b>\n\n"
    text += f"👥 Ovoz bergan foydalanuvchilar: <b>{total_voters}</b>\n"
    text += f"📋 Ruxsat berilgan guruhlar: <b>{len(groups)}</b>\n"
    text += f"🗳 Jami ovozlar: <b>{len(all_votes)}</b>\n\n"
    
    text += "📊 <b>Nominatsiyalar bo'yicha:</b>\n"
    for nom_key, nomination in NOMINATIONS.items():
        count = await get_votes_count_by_nomination(nom_key)
        text += f"• {nomination['title'][:30]}...: <b>{count}</b> ta ovoz\n"
    
    kb = InlineKeyboardBuilder()
    kb.button(text="◀️ Orqaga", callback_data="admin:back")
    
    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin:back")
async def back_to_admin(callback: CallbackQuery):
    """Admin panelga qaytish"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🔐 <b>Admin Panel</b>\n\n"
        "Quyidagi amallardan birini tanlang:",
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()
