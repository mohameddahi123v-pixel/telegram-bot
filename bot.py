import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient

TOKEN = os.getenv("8075424913:AAEwgo6msBvIXxBcuxXRGvkNGFTF3bihrPQ")
MONGO = os.getenv("mongodb+srv://Mohameddahi123a:<db_password>@cluster0.jf1xisu.mongodb.net/?appName=Cluster0")
CHANNEL = "@tgstars203"
GROUP = "@Profite_internet"

client = MongoClient(MONGO)
db = client["ref_bot"]
users = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # تحقق من الاشتراك
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            await update.message.reply_text("⚠️ اشترك في القناة الأول ثم اكتب /start")
            return
    except:
        await update.message.reply_text("⚠️ تأكد إنك مشترك في القناة")
        return

    ref = context.args[0] if context.args else None

    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id, "ref": ref, "points": 0})

        if ref and ref.isdigit():
            users.update_one({"user_id": int(ref)}, {"$inc": {"points": 1}})

    link = f"https://t.me/YOUR_BOT?start={user_id}"

    await update.message.reply_text(
        f"🎉 أهلاً بيك!\n\n"
        f"🔗 رابط الدعوة الخاص بك:\n{link}\n\n"
        f"📊 كل صديق تدخله = نقطة"
    )

# عرض النقاط
async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.find_one({"user_id": user_id})

    if user:
        await update.message.reply_text(f"📊 نقاطك: {user['points']}")
    else:
        await update.message.reply_text("❌ مش مسجل")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("points", points))

app.run_polling()
