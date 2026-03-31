import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===============================
# KEYBOARD START
# ===============================
def start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔥 VVIP", callback_data="vvip"),
            InlineKeyboardButton("📢 Undang Teman", callback_data="referral"),
        ]
    ])

# ===============================
# KEYBOARD VIP
# ===============================
def vip_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📁 VIP HIJABERS", callback_data="vip_hijabers")],
        [InlineKeyboardButton("📁 VIP TIKTOK", callback_data="vip_tiktok")],
        [InlineKeyboardButton("📁 VIP OME TV", callback_data="vip_ometv")],
        [InlineKeyboardButton("📁 VIP KOLPRI", callback_data="vip_kolpri")],
        [InlineKeyboardButton("📁 VIP PREMIUM", callback_data="vip_premium")],
        [InlineKeyboardButton("📁 VIP RANDOM", callback_data="vip_random")],
        [InlineKeyboardButton("📁 VIP BOCIL [A]", callback_data="vip_bocil_a")],
        [InlineKeyboardButton("📁 VIP BOCIL [B]", callback_data="vip_bocil_b")],
        [InlineKeyboardButton("🛒 Ambil Semua VIP", callback_data="vip_all")],
        [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="menu")]
    ])

# ===============================
# TEXT PAYMENT DINAMIS
# ===============================
def get_payment_text(user, amount):
    name = user.last_name if user.last_name else user.first_name
    mention = f'<a href="tg://user?id={user.id}">{name}</a>'

    return (
        f"👋 Hallo {mention}\n\n"
        f"Silakan lakukan pembayaran sebesar:\n"
        f"<b>Rp. {amount}</b>\n"
        f"menggunakan QRIS berikut.\n\n"
        "Kirimkan bukti transfer ke sini.\n\n"
        "⚠️ <b>Catatan:</b>\n\n"
        "Pembayaran di bawah nominal dianggap sebagai sedekah.\n\n"
        "Tanpa bukti transfer, tidak akan masuk dalam list VVIP."
    )

# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.last_name if user.last_name else user.first_name
    mention = f'<a href="tg://user?id={user.id}">{name}</a>'

    msg = await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=-1003748208059,
        message_id=3
    )

    await context.bot.edit_message_caption(
        chat_id=update.effective_chat.id,
        message_id=msg.message_id,
        caption=(
            f"Halo {mention} selamat datang di <b>VVIP HARIAN PEMERSATU BANGSA</b>"
        ),
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )

# ===============================
# HANDLE BUTTON
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    # ===== MENU VVIP =====
    if query.data == "vvip":
        await query.edit_message_caption(
            caption="<b>📚 Daftar VVIP</b>\n\nPilih paket 👇",
            reply_markup=vip_keyboard(),
            parse_mode="HTML"
        )

    # ===== REFERRAL =====
    elif query.data == "referral":
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user.id}"

        await query.edit_message_caption(
            caption=(
                "📢 <b>UNDANG TEMAN</b>\n\n"
                "Undang <b>10 teman</b> untuk membuka fitur VVIP GRATIS 🔥\n\n"
                f"🔗 Link kamu:\n{ref_link}"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    # ===== 1-2 (10K) =====
    elif query.data in ["vip_hijabers", "vip_tiktok"]:
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003748208059,
            message_id=5
        )
        await query.message.reply_text(get_payment_text(user, "10.000"), parse_mode="HTML")

    # ===== 3-5 (15K) =====
    elif query.data in ["vip_ometv", "vip_kolpri", "vip_premium"]:
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003748208059,
            message_id=4
        )
        await query.message.reply_text(get_payment_text(user, "15.000"), parse_mode="HTML")

    # ===== 6-8 (20K) =====
    elif query.data in ["vip_random", "vip_bocil_a", "vip_bocil_b"]:
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003748208059,
            message_id=2
        )
        await query.message.reply_text(get_payment_text(user, "20.000"), parse_mode="HTML")

    # ===== 9 (50K) =====
    elif query.data == "vip_all":
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003748208059,
            message_id=6
        )
        await query.message.reply_text(get_payment_text(user, "50.000"), parse_mode="HTML")

    # ===== BACK =====
    elif query.data == "menu":
        await query.edit_message_caption(
            caption="Klik tombol di bawah untuk membuka menu 🔥",
            reply_markup=start_keyboard()
        )

# ===============================
# MAIN
# ===============================
def main():
    if not BOT_TOKEN:
        print("TOKEN belum diisi!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot aktif bro 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
