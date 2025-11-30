‏import requests
‏from telegram import Update
‏from telegram.ext import Application, CommandHandler, ContextTypes
‏
‏TOKEN = "8403763339:AAFuyHOTd7WWu8S1SwdqBk-X_wNAcneKN-I"
‏
‏# قائمة لحفظ التنبيهات النشطة لكل مستخدم
‏active_alerts = {}
‏
‏# ====== دوال جلب الأسعار ======
‏def get_bitcoin_price():
‏    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
‏    response = requests.get(url).json()
‏    return response["bitcoin"]["usd"]
‏
‏def get_gold_price():
‏    url = "https://metals-api.com/api/latest?access_key=ضع_المفتاح_هنا&base=USD&symbols=XAU"
‏    response = requests.get(url).json()
‏    return response["rates"]["XAU"]
‏
‏def get_forex_price():
‏    url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
‏    response = requests.get(url).json()
‏    return response["rates"]["EUR"]
‏
‏# ====== أوامر البوت ======
‏async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    await update.message.reply_text(
‏        "👋 أهلاً بك!\n"
‏        "الأوامر المتاحة:\n"
‏        "/alert <asset> <price> → ضبط تنبيه\n"
‏        "/alerts → عرض التنبيهات النشطة\n"
‏        "/removealert <رقم> → حذف تنبيه\n"
‏        "الأصول المدعومة: bitcoin, gold, forex\n"
‏        "مثال: /alert bitcoin 40000"
‏    )
‏
‏# أمر ضبط التنبيه
‏async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    try:
‏        asset = context.args[0].lower()
‏        target_price = float(context.args[1])
‏        chat_id = update.effective_chat.id
‏
‏        if chat_id not in active_alerts:
‏            active_alerts[chat_id] = []
‏        active_alerts[chat_id].append({"asset": asset, "target": target_price})
‏
‏        await update.message.reply_text(f"🔔 تم ضبط تنبيه {asset} عند {target_price}$")
‏    except (IndexError, ValueError):
‏        await update.message.reply_text("⚠️ استخدم الأمر بهذا الشكل: /alert bitcoin 40000")
‏
‏# أمر عرض التنبيهات
‏async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    chat_id = update.effective_chat.id
‏    if chat_id not in active_alerts or len(active_alerts[chat_id]) == 0:
‏        await update.message.reply_text("📭 لا توجد تنبيهات نشطة حالياً.")
‏    else:
‏        msg = "📋 التنبيهات النشطة:\n"
‏        for i, alert in enumerate(active_alerts[chat_id], start=1):
‏            msg += f"{i}. {alert['asset']} عند {alert['target']}$\n"
‏        await update.message.reply_text(msg)
‏
‏# أمر حذف التنبيه
‏async def removealert(update: Update, context: ContextTypes.DEFAULT_TYPE):
‏    chat_id = update.effective_chat.id
‏    try:
‏        index = int(context.args[0]) - 1  # المستخدم يدخل رقم التنبيه (1,2,3...)
‏        if chat_id in active_alerts and 0 <= index < len(active_alerts[chat_id]):
‏            removed = active_alerts[chat_id].pop(index)
‏            await update.message.reply_text(
‏                f"🗑️ تم حذف التنبيه: {removed['asset']} عند {removed['target']}$"
‏            )
‏        else:
‏            await update.message.reply_text("⚠️ رقم التنبيه غير صحيح.")
‏    except (IndexError, ValueError):
‏        await update.message.reply_text("⚠️ استخدم الأمر بهذا الشكل: /removealert 1")
‏
‏# ====== تشغيل البوت ======
‏def main():
‏    app = Application.builder().token(TOKEN).build()
‏
‏    app.add_handler(CommandHandler("start", start))
‏    app.add_handler(CommandHandler("alert", alert))
‏    app.add_handler(CommandHandler("alerts", alerts))
‏    app.add_handler(CommandHandler("removealert", removealert))
‏
‏    app.run_polling()
‏
‏if __name__ == "__main__":
‏    main()