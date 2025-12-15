import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

gban_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GBAN management bot is running!")

async def gban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Only owner can use GBAN")
        return

    if not context.args:
        await update.message.reply_text("Usage: /gban user_id")
        return

    user_id = int(context.args[0])
    gban_users.add(user_id)
    await update.message.reply_text(f"🚫 User {user_id} globally banned")

async def ungban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    user_id = int(context.args[0])
    gban_users.discard(user_id)
    await update.message.reply_text(f"✅ User {user_id} unbanned")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gban", gban))
    app.add_handler(CommandHandler("ungban", ungban))

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
