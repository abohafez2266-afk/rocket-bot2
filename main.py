import telebot
import random
import time

TOKEN = "ضع_التوكن_هنا"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أهلا بيك في روكيت بوت 2\n\nالأوامر:\n/signal - إشارة جديدة\n/status - حالة البوت")

@bot.message_handler(commands=['signal'])
def signal(message):
    x = round(random.uniform(1.8, 5.5), 2)
    bot.reply_to(message, f"🎯 إشارة روكيت\n\n💥 النسبة المتوقعة: {x}x\n⏳ ادخل بعد 5 ثواني\n\n⚠️ العب بحذر!")

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "✅ البوت شغال تمام")

bot.infinity_polling()
