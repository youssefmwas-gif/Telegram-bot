from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from datetime import datetime, time

TOKEN = "8307293371:AAGkxpqlczCbjppphtVtivOEFmqAktUYFpU"
ADMIN_ID = 8307293371

last_replied = {}
reply_index = {}
welcomed_users = set()
all_users = set()

daily_message = (
    "☀️ صباح الخير من وكالة ستار تريدر 🌟\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "📊 ملخص السوق اليوم:\n"
    "🛢️ النفط: 82.45 دولار\n"
    "💰 بيتكوين: 91,163.64 دولار\n"
    "📈 آبل: 278.85 دولار\n\n"
    "🚀 نتمنى لكم يوماً مليئاً بالنجاح والفرص!"
)

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()
    now = datetime.now()

    all_users.add(user_id)

    if user_id not in welcomed_users:
        welcome_text = (
            "👋 أهلاً وسهلاً بك في وكالة ستار تريدر 🌟\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "📌 نحن هنا لنرافقك في رحلتك الاستثمارية.\n"
            "🚀 مع ستار تريدر، المستقبل بين يديك.\n\n"
            "📋 أوامر البوت:\n"
            "/oil - أسعار النفط 🛢️\n"
            "/crypto - العملات الرقمية 💰\n"
            "/stocks - الأسهم العالمية 📈\n"
            "/indices - مؤشرات الأسواق 🌍\n"
            "/news - الأخبار الاقتصادية 📰\n"
            "/about - من نحن ℹ️\n"
            "/privacy - سياسة الخصوصية 🔒\n"
            "/education - تعليم التداول 🎓\n"
            "/help - عرض الأوامر 📋"
        )
        await update.message.reply_text(welcome_text)
        welcomed_users.add(user_id)
        reply_index[user_id] = 0
        last_replied[user_id] = now
        return

    if text == "/start":
        await update.message.reply_text("👋 أهلاً بك في بوت WOLFTRADING7 🌟")
        return

    if text == "/help":
        await update.message.reply_text(
            "📋 أوامر البوت:\n/oil\n/crypto\n/stocks\n/indices\n/news\n/about\n/privacy\n/education"
        )
        return

    if text == "/oil":
        await update.message.reply_text("🛢️ أسعار النفط:\nخام برنت: 82.45 دولار\nغرب تكساس: 78.30 دولار")
        return

    if text == "/crypto":
        await update.message.reply_text("💰 بيتكوين: 91,163.64 دولار\n🪙 إيثيريوم: 2,300 دولار")
        return

    if text == "/stocks":
        await update.message.reply_text("📈 آبل: 278.85 دولار\n📉 تسلا: 245.10 دولار")
        return

    if text == "/market":
        await update.message.reply_text(
            "📊 ملخص السوق الآن:\n🛢️ النفط: 82.45 دولار\n💰 بيتكوين: 91,163.64 دولار\n📈 آبل: 278.85 دولار"
        )
        return

    if text == "/users" and user_id == ADMIN_ID:
        users_list = "\n".join([str(uid) for uid in all_users])
        await update.message.reply_text(f"👥 المستخدمين:\n{users_list}")
        return

    if text.startswith("/broadcast") and user_id == ADMIN_ID:
        msg = text.replace("/broadcast", "").strip()
        for uid in all_users:
            await context.bot.send_message(chat_id=uid, text=f"📢 رسالة من الإدارة:\n{msg}")
        await update.message.reply_text("✅ تم الإرسال.")
        return

async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    for uid in all_users:
        await context.bot.send_message(chat_id=uid, text=daily_message)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    app.job_queue.run_daily(send_daily_message, time=time(9, 0))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())