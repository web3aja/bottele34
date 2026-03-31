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
# CHANNEL WAJIB JOIN
# ===============================
CHANNELS = [
    {"username": "@LunaaAirDrop", "link": "https://t.me/LunaaAirDrop"},
    {"username": "@gamegilacuan", "link": "https://t.me/gamegilacuan"},
    {"username": "@gamecuanngila", "link": "https://t.me/gamecuanngila"},
    {"username": "@gamegilacuan", "link": "https://t.me/gamegilacuan"},
]

# ===============================
# MENU UTAMA
# ===============================
def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("1. Diamond", callback_data="Diamond"),
            InlineKeyboardButton("2. Cash", callback_data="Cash"),
        ],
        [
            InlineKeyboardButton("3. Poin", callback_data="Poin"),
            InlineKeyboardButton("4. Lokasi", callback_data="Lokasi"),
        ],
        [
            InlineKeyboardButton("🔄 Coba Lagi", callback_data="retry"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ===============================
# KEYBOARD JOIN (4 KOTAK)
# ===============================
def get_join_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNELS[0]["link"]),
            InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNELS[1]["link"]),
        ],
        [
            InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNELS[2]["link"]),
            InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNELS[3]["link"]),
        ],
        [
            InlineKeyboardButton("🔄 CEK LAGI", callback_data="check_join")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ===============================
# CEK APAKAH SUDAH JOIN
# ===============================
async def is_user_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        # User harus join semua channel
        for ch in CHANNELS:
            member = await context.bot.get_chat_member(ch["username"], user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False


# ===============================
# START COMMAND
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name

    joined = await is_user_joined(update, context)

    if not joined:
        await update.message.reply_text(
            f"<b>HELLO {name}</b> 👋\n\n"
            "ANDA HARUS BERGABUNG DI SEMUA CHANNEL/GRUP SAYA TERLEBIH DAHULU\n"
            "UNTUK MELIHAT FILE YANG SAYA BAGIKAN\n\n"
            "SILAHKAN JOIN KE CHANNEL TERLEBIH DAHULU 👇",
            reply_markup=get_join_keyboard(),
            parse_mode="HTML"
        )
        return

    await update.message.reply_text(
        f"<b>Halo {name}!</b> 👋\n\n"
        "Selamat datang.\nSilakan pilih layanan di bawah ini:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


# ===============================
# HANDLE BUTTON
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    joined = await is_user_joined(update, context)

    if not joined:
        await query.edit_message_text(
            "🚫 Kamu belum join semua channel!\nSilakan join dulu 👇",
            reply_markup=get_join_keyboard()
        )
        return

    if query.data == "Diamond":
        text = "💎 Link Diamond:\nhttps://link-diamond.com"

    elif query.data == "Cash":
        text = "💵 Link Cash:\nhttps://link-cash.com"

    elif query.data == "Poin":
        text = "🎯 Link Poin:\nhttps://link-poin.com"

    elif query.data == "Lokasi":
        text = "📍 Link Lokasi:\nhttps://link-lokasi.com"

    elif query.data == "retry":
        await query.edit_message_text(
            "Menu sudah di-refresh bg 👇",
            reply_markup=get_main_menu_keyboard()
        )
        return

    elif query.data == "check_join":
        if joined:
            await query.edit_message_text(
                "✅ Terima kasih sudah join semua channel!\nSilakan pilih layanan:",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await query.answer("❌ Kamu belum join semua channel!", show_alert=True)
        return

    else:
        return

    await query.edit_message_text(
        text,
        reply_markup=get_main_menu_keyboard()
    )


# ===============================
# MAIN
# ===============================
def main():
    if not BOT_TOKEN:
        print("TOKEN belum diisi di file .env!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()