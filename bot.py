import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# توكن البوت من BotFather
TOKEN = os.getenv("TOKEN")

# قائمة لحفظ التنبيهات النشطة لكل مستخدم
active_alerts = {}

# ====== دوال جلب الأسعار ======
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url).json()
    return response["bitcoin"]["usd"]

def get_gold_price():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=XAU"
    response = requests.get(url).json()
    return response["rates"]["XAU"]

def get_forex_price():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
    response = requests.get(url).json()
    return response["rates"]["EUR"]

# ====== أوامر البوت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/bitcoin", "/gold"],
        ["/forex", "/alerts"],
        ["/alert bitcoin 40000", "/removealert 1"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 أهلاً بك في WOLLFTRADING!\nاختر أمر من الأزرار أو اكتب يدويًا:",
        reply_markup=reply_markup
    )

async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_bitcoin_price()
    await update.message.reply_text(f"₿ سعر البيتكوين الحالي: {price} USD")

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_gold_price()
    await update.message.reply_text(f"💰 سعر الذهب الحالي: {price} USD")

async def forex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_forex_price()
    await update.message.reply_text(f"💱 سعر الدولار مقابل اليورو: {price}")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        asset = context.args[0].lower()
        target_price = float(context.args[1])
        chat_id = update.effective_chat.id

        if chat_id not in active_alerts:
            active_alerts[chat_id] = []
        active_alerts[chat_id].append({"asset": asset, "target": target_price})

        await update.message.reply_text(f"🔔 تم ضبط تنبيه {asset} عند {target_price}$")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ استخدم الأمر بهذا الشكل: /alert bitcoin 40000")

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in active_alerts or len(active_alerts[chat_id]) == 0:
        await update.message.reply_text("📭 لا توجد تنبيهات نشطة حالياً.")
    else:
        msg = "📋 التنبيهات النشطة:\n"
        for i, alert in enumerate(active_alerts[chat_id], start=1):
            msg += f"{i}. {alert['asset']} عند {alert['target']}$\n"
        await update.message.reply_text(msg)

async def removealert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        index = int(context.args[0]) - 1
        if chat_id in active_alerts and 0 <= index < len(active_alerts[chat_id]):
            removed = active_alerts[chat_id].pop(index)
            await update.message.reply_text(
                f"🗑️ تم حذف التنبيه: {removed['asset']} عند {removed['target']}$"
            )
        else:
            await update.message.reply_text("⚠️ رقم التنبيه غير صحيح.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ استخدم الأمر بهذا الشكل: /removealert 1")

# ====== تشغيل البوت ======
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bitcoin", bitcoin))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("forex", forex))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("alerts", alerts))
    app.add_handler(CommandHandler("removealert", removealert))
    app.run_polling()

if __name__ == "__main__":
    main()