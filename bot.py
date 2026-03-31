import os
import json
import logging
import traceback
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
USER_FILE = "users.json"

# ===============================
# LOAD USER (ANTI ERROR)
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

users = load_users()

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
        [InlineKeyboardButton("📁 VIP RUSSIA", callback_data="vip_ometv")],
        [InlineKeyboardButton("📁 VIP INDONESIA", callback_data="vip_kolpri")],
        [InlineKeyboardButton("📁 VIP RANDOM", callback_data="vip_premium")],
        [InlineKeyboardButton("📁 VIP PRENIUM", callback_data="vip_random")],
        [InlineKeyboardButton("📁 VIP BOCIL [A]", callback_data="vip_bocil_a")],
        [InlineKeyboardButton("📁 VIP BOCIL [B]", callback_data="vip_bocil_b")],
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
        "Pembayaran di bawah nominal dianggap sebagai sedekah.\n\n"
        "Tanpa bukti transfer, tidak akan masuk dalam list VVIP."
    )

# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in users:
        users.add(user.id)
        save_users(users)

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
        caption=f"Halo {mention} selamat datang di <b>VVIP HARIAN PEMERSATU BANGSA</b>",
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )

# ===============================
# AUTO BROADCAST (60 DETIK TEST)
# ===============================
async def broadcast_vvip(context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 <b>BIG PROMO JOIN VVIP MEDIA 10K 💎</b>\n\n"
        "Modal 10K doang udah bisa jadi member VVIP!\n"
        "Bebas intip-intip ribuan video viral yang selalu fresh setiap jam.\n\n"
        "Harga paling bersahabat dengan kualitas video FULL HD.\n\n"
        "Jangan cuma jadi penonton, JOIN sekarang sebelum promo berakhir!"
    )

    for user_id in list(users):
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Hapus user {user_id} karena error:", e)
            users.discard(user_id)
            save_users(users)

# ===============================
# HANDLE BUTTON
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "vvip":
        await query.edit_message_caption(
            caption="<b>📚 Daftar VVIP</b>\n\nPilih paket 👇",
            reply_markup=vip_keyboard(),
            parse_mode="HTML"
        )

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

    # JOB QUEUE AMAN
    try:
        job_queue = app.job_queue
        if job_queue:
            job_queue.run_repeating(broadcast_vvip, interval=60, first=10)
            print("Broadcast aktif tiap 60 detik")
        else:
            print("JobQueue tidak aktif! Install extra package.")
    except Exception as e:
        print("JobQueue error:", e)

    print("Bot aktif anti crash 🚀")

    try:
        app.run_polling(drop_pending_updates=True)
    except Exception:
        print("ERROR BESAR:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
