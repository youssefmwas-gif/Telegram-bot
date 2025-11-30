import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# توكن البوت من BotFather (مكتوب مباشرة داخل الكود)
TOKEN = "8403763339:AAFuyHOTd7WWu8S1SwdqBk-X_wNAcneKN-I"

# ====== دوال جلب الأسعار ======
def سعر_البيتكوين():
    رابط = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    رد = requests.get(رابط).json()
    return رد["bitcoin"]["usd"]

def سعر_الذهب():
    رابط = "https://api.exchangerate.host/latest?base=USD&symbols=XAU"
    رد = requests.get(رابط).json()
    return رد["rates"]["XAU"]

def سعر_اليورو():
    رابط = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
    رد = requests.get(رابط).json()
    return رد["rates"]["EUR"]

# ====== أوامر البوت ======
async def ابدأ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    لوحة = [["💰 بيتكوين", "🪙 ذهب"], ["💶 يورو"]]
    رد = ReplyKeyboardMarkup(لوحة, resize_keyboard=True)
    await update.message.reply_text("أهلاً بك في WOLF TRADER 👋\nاختر نوع السعر الذي تريده:", reply_markup=رد)

async def بيتكوين(update: Update, context: ContextTypes.DEFAULT_TYPE):
    السعر = سعر_البيتكوين()
    await update.message.reply_text(f"سعر البيتكوين الحالي: ${السعر}")

async def ذهب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    السعر = سعر_الذهب()
    await update.message.reply_text(f"سعر الذهب الحالي (أونصة): ${السعر}")

async def يورو(update: Update, context: ContextTypes.DEFAULT_TYPE):
    السعر = سعر_اليورو()
    await update.message.reply_text(f"سعر اليورو مقابل الدولار: {السعر}")

# ====== تشغيل البوت ======
التطبيق = Application.builder().token(TOKEN).build()
التطبيق.add_handler(CommandHandler("start", ابدأ))
التطبيق.add_handler(CommandHandler("bitcoin", بيتكوين))
التطبيق.add_handler(CommandHandler("gold", ذهب))
التطبيق.add_handler(CommandHandler("forex", يورو))

التطبيق.run_polling()