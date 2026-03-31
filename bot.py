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

# ===============================
# LOAD ENV
# ===============================
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
    keyboard = [
        [
            InlineKeyboardButton("🔥 VVIP", callback_data="vvip"),
            InlineKeyboardButton("📢 Undang Teman", callback_data="referral"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===============================
# KEYBOARD VIP MENU
# ===============================
def vip_keyboard():
    keyboard = [
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
    ]
    return InlineKeyboardMarkup(keyboard)

# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.last_name if user.last_name else user.first_name

    sent_msg = await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=-1003748208059,
        message_id=3
    )

    await context.bot.edit_message_caption(
        chat_id=update.effective_chat.id,
        message_id=sent_msg.message_id,
        caption=(
            f"<b>Halo selamat datang di Asupan VVIP Update Harian {name}</b> 👋\n\n"
            "Klik tombol di bawah untuk membuka menu 🔥"
        ),
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )

# ===============================
# HANDLE BUTTON
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    # ====== MENU VVIP ======
    if query.data == "vvip":
        await query.edit_message_caption(
            caption=(
                "<b>📚 Daftar VVIP Bot</b>\n\n"
                "Silakan pilih salah satu paket 👇"
            ),
            reply_markup=vip_keyboard(),
            parse_mode="HTML"
        )

    # ====== REFERRAL ======
    elif query.data == "referral":
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user.id}"

        await query.message.reply_text(
            f"📢 <b>UNDANG TEMAN</b>\n\n"
            "Undang <b>10 teman</b> untuk membuka fitur VVIP GRATIS 🔥\n\n"
            f"🔗 Link referral kamu:\n{ref_link}\n\n"
            "Bagikan ke teman-teman kamu sekarang!",
            parse_mode="HTML"
        )

    # ====== LIST VIP ======
    elif query.data == "vip_hijabers":
        text = "📁 VIP HIJABERS\nhttps://example.com/hijabers"

    elif query.data == "vip_tiktok":
        text = "📁 VIP TIKTOK\nhttps://example.com/tiktok"

    elif query.data == "vip_ometv":
        text = "📁 VIP OME TV\nhttps://example.com/ometv"

    elif query.data == "vip_kolpri":
        text = "📁 VIP KOLPRI\nhttps://example.com/kolpri"

    elif query.data == "vip_premium":
        text = "📁 VIP PREMIUM\nhttps://example.com/premium"

    elif query.data == "vip_random":
        text = "📁 VIP RANDOM\nhttps://example.com/random"

    elif query.data == "vip_bocil_a":
        text = "📁 VIP BOCIL A\nhttps://example.com/bocilA"

    elif query.data == "vip_bocil_b":
        text = "📁 VIP BOCIL B\nhttps://example.com/bocilB"

    elif query.data == "vip_all":
        text = "🔥 Semua VIP:\nhttps://example.com/allvip"

    # ====== KEMBALI ======
    elif query.data == "menu":
        await query.edit_message_caption(
            caption="Klik tombol di bawah untuk membuka menu 🔥",
            reply_markup=start_keyboard()
        )
        return

    else:
        return

    await query.message.reply_text(text)

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

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    main()
