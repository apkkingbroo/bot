import asyncio
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

BOT_TOKEN = "8016222793:AAHgeksIYgNPzzhcPjUfkgfVqn-85W0i6gI"
CHANNEL_ID = -1001992550549
REFERRAL_LINK = "https://bdgwin.cc/#/register?invitationCode=372171400520"

subscribed_users = set()
colors = ["🔴 RED", "🟢 GREEN", "🟣 VIOLET"]
numbers = list(range(0, 10))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ Join Channel", url="https://t.me/apkmodderking")],
                [InlineKeyboardButton("I have Joined", callback_data="check")]]
    
    await update.message.reply_text(
        f"✨ *Welcome to Color Predictor VIP!* ✨\n\n"
        f"Join our official channel to receive predictions every minute!\n\n"
        f"🔗 *Connected to BDGWIN:*\n{REFERRAL_LINK}\n\n"
        f"Click below to join & confirm.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
    if member.status in ['member', 'administrator', 'creator']:
        subscribed_users.add(user.id)
        await query.edit_message_text(
            text="✅ You have successfully joined @apkmodderking!\n\n"
                 "You will now receive predictions every 1 minute.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await query.edit_message_text(
            text="❌ You need to join @apkmodderking to use the bot.",
            parse_mode=ParseMode.MARKDOWN
        )

async def send_predictions(application):
    while True:
        if subscribed_users:
            prediction = f"""
╔══〔 COLOR PREDICTION 〕══╗
🎯 Number: {random.choice(numbers)}
🎨 Color: {random.choice(colors)}
➕ Big/Small: {"Big" if random.randint(0, 9) >= 5 else "Small"}
🔗 Connected: BDGWIN
👉 {REFERRAL_LINK}
📢 @apkmodderking
╚═════════════════════════╝
"""
            for user_id in subscribed_users:
                try:
                    await application.bot.send_message(chat_id=user_id, text=prediction)
                except Exception:
                    pass
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    asyncio.create_task(send_predictions(app))
    await app.initialize()
    await app.start()
    print("Bot is running...")
    await app.updater.start_polling()
    await app.updater.idle()

# ---- SAFELY RUN ON RENDER ----
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

loop.run_until_complete(main())
