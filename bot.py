import os
import json
import logging
import traceback
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_FILE = "users.json"
DAILY_FILE = "daily_users.json"

ADMIN_ID = 7640270845  # GANTI ID LU

# ===============================
# LOAD & SAVE USER
# ===============================
def load_users():
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                data = json.load(f)
                return set(data if isinstance(data, list) else [])
    except:
        print("users.json rusak, reset...")
    return set()

def save_users(users):
    try:
        with open(USER_FILE, "w") as f:
            json.dump(list(users), f)
    except Exception as e:
        print("Gagal save users:", e)

# ===============================
# DAILY USER
# ===============================
def load_daily():
    if os.path.exists(DAILY_FILE):
        return json.load(open(DAILY_FILE))
    return {}

def save_daily(data):
    json.dump(data, open(DAILY_FILE, "w"))

users = load_users()
daily_users = load_daily()

# ===============================
# KEYBOARD START (ADMIN ONLY USER BUTTON)
# ===============================
def start_keyboard(user_id):
    buttons = [
        [
            InlineKeyboardButton("🔥 VVIP", callback_data="vvip"),
            InlineKeyboardButton("📢 Undang Teman", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("⭐ Testimoni", callback_data="testimoni"),
        ]
    ]

    if user_id == ADMIN_ID:
        buttons.append(
            [InlineKeyboardButton("👥 User", callback_data="user_count")]
        )

    return InlineKeyboardMarkup(buttons)

# ===============================
# KEYBOARD VIP
# ===============================
def vip_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📁 VIP HIJABERS", callback_data="vip_hijabers")],
        [InlineKeyboardButton("📁 VIP TIKTOK", callback_data="vip_tiktok")],
        [InlineKeyboardButton("📁 VIP RUSSIA", callback_data="vip_ometv")],
        [InlineKeyboardButton("📁 VIP INDONESIA", callback_data="vip_kolpri")],
        [InlineKeyboardButton("📁 VIP RANDOM", callback_data="vip_random")],
        [InlineKeyboardButton("📁 VIP PRENIUM", callback_data="vip_premium")],
        [InlineKeyboardButton("📁 VIP BOCIL [A]", callback_data="vip_bocil_a")],
        [InlineKeyboardButton("📁 VIP BOCIL [B]", callback_data="vip_bocil_b")],
        [InlineKeyboardButton("📁 VIP ANIME HENTAI", callback_data="vip_anime")],
        [InlineKeyboardButton("📁 VIP GAME HENTAI", callback_data="vip_game")],
        [InlineKeyboardButton("🛒 Ambil Semua VIP", callback_data="vip_all")],
        [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="menu")]
    ])

# ===============================
# TEXT PAYMENT
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
        "Lakukan pembayaran sebelum waktu habis (3 menit).\n\n"
        "Tanpa bukti transfer, tidak akan masuk dalam list VVIP."
    )

# ===============================
# PROMO
# ===============================
async def send_hourly_promo(context: ContextTypes.DEFAULT_TYPE):
    for user_id in users:
        try:
            msg = await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=-1003748208059,
                message_id=3
            )

            await context.bot.edit_message_caption(
                chat_id=user_id,
                message_id=msg.message_id,
                caption=(
                    "🔥 <b>BIG PROMO JOIN VVIP MEDIA 10K 💎</b>\n\n"
                    "Modal 10K doang udah bisa jadi member VVIP!\n"
                    "Bebas intip video viral fresh tiap jam 🔥\n\n"
                    "Jangan sampai ketinggalan!"
                ),
                reply_markup=start_keyboard(user_id),
                parse_mode="HTML"
            )

        except Exception as e:
            print(f"Gagal kirim ke {user_id}:", e)

# ===============================
# REMINDER
# ===============================
async def payment_reminder(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data

    text = (
        "⏰ <b>WAKTU HAMPIR HABIS!</b>\n\n"
        "Segera selesaikan pembayaran sebelum hangus ❌"
    )

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Gagal kirim reminder ke {user_id}:", e)

# ===============================
# FOTO
# ===============================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bukti diterima, sedang diverifikasi.",
        parse_mode="HTML"
    )

# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    today = datetime.now().strftime("%Y-%m-%d")

    if user.id not in users:
        users.add(user.id)
        save_users(users)

    if today not in daily_users:
        daily_users[today] = []

    if user.id not in daily_users[today]:
        daily_users[today].append(user.id)
        save_daily(daily_users)

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
        caption=f"Halo {mention} selamat datang di <b>VVIP PEMERSATU BANGSA</b>",
        reply_markup=start_keyboard(user.id),
        parse_mode="HTML"
    )

# ===============================
# BUTTON HANDLER
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    # USER COUNT (ADMIN ONLY)
    if query.data == "user_count":
        if user.id != ADMIN_ID:
            await query.answer("❌ Tidak diizinkan", show_alert=True)
            return

        today = datetime.now().strftime("%Y-%m-%d")
        total = len(daily_users.get(today, []))
        total_all = len(users)

        await query.message.reply_text(
            f"👥 Hari ini: {total}\n👥 Total semua: {total_all}"
        )

    elif query.data == "vvip":
        await query.edit_message_caption(
            caption="<b>📚 Daftar VVIP</b>\n\nPilih paket 👇",
            reply_markup=vip_keyboard(),
            parse_mode="HTML"
        )

    elif query.data == "testimoni":
        for msg_id in [7, 8, 9]:
            await context.bot.copy_message(
                chat_id=query.message.chat_id,
                from_chat_id=-1003748208059,
                message_id=msg_id
            )

        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003748208059,
            message_id=10,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="menu")]
            ])
        )

    elif query.data == "referral":
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user.id}"

        await query.edit_message_caption(
            caption=f"🔗 Link kamu:\n{ref_link}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="menu")]
            ]),
            parse_mode="HTML"
        )

    elif query.data in ["vip_hijabers", "vip_tiktok"]:
        await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=-1003748208059, message_id=5)
        await query.message.reply_text(get_payment_text(user, "10.000"), parse_mode="HTML")

    elif query.data in ["vip_ometv", "vip_kolpri", "vip_premium", "vip_anime"]:
        await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=-1003748208059, message_id=4)
        await query.message.reply_text(get_payment_text(user, "15.000"), parse_mode="HTML")

    elif query.data in ["vip_random", "vip_bocil_a", "vip_bocil_b", "vip_game"]:
        await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=-1003748208059, message_id=2)
        await query.message.reply_text(get_payment_text(user, "20.000"), parse_mode="HTML")

    elif query.data == "vip_all":
        await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=-1003748208059, message_id=6)
        await query.message.reply_text(get_payment_text(user, "50.000"), parse_mode="HTML")

    elif query.data == "menu":
        await query.edit_message_caption(
            caption="Klik tombol di bawah untuk membuka menu 🔥",
            reply_markup=start_keyboard(user.id)
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
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.job_queue.run_repeating(send_hourly_promo, interval=3600, first=3600)

    print("Bot aktif 🚀")

    try:
        app.run_polling(drop_pending_updates=True)
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()
