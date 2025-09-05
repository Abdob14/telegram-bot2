# يعمل على كل النسخ: v13 القديمة أو v20+ الجديدة
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# نحاول أولاً استيراد الواجهه الجديدة (v20+). لو فشل نستخدم القديمة (v13).
NEW_API = True
try:
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
except Exception:
    NEW_API = False
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# التوكن الخاص بك
TOKEN = "7752022190:AAGazioJqsJSEPe5-OLdWJ44lHMgEe8gdKk"

# نص الرسالة الرئيسية
def get_main_text():
    return (
        "Solana · 🪙\n"
        "8UCEhMWYiLackDfnPMEyzzdAt7imLjxZeoXX5ro4voWy (Tap to copy)\n"
        "Balance: 0 SOL ($0.00)\n"
        "—\n\n"
        "Click on the Refresh button to update your current balance.\n\n"
        "Join our Telegram group @trojan and follow us on Twitter!\n\n"
        "💡 If you aren't already, we advise that you use any of the following bots to trade with.\n"
        "Agamemnon | Achilles | Nestor | Odysseus | Menelaus | Diomedes | Helenus | Hector\n\n"
        "⚠️ We have no control over ads shown by Telegram in this bot. Do not be scammed by fake airdrops or login pages.\n"
    )

# لوحة الأزرار
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Refresh 🔄", callback_data='refresh')],
        [InlineKeyboardButton("Buy 🛒", callback_data='buy'),
         InlineKeyboardButton("Sell 💰", callback_data='sell')],
        [InlineKeyboardButton("Positions 📊", callback_data='positions'),
         InlineKeyboardButton("Limit Orders 📌", callback_data='limit_orders')],
        [InlineKeyboardButton("DCA Orders 🔄", callback_data='dca_orders'),
         InlineKeyboardButton("Copy Trade 📥", callback_data='copy_trade')],
        [InlineKeyboardButton("Sniper 🎯", callback_data='sniper'),
         InlineKeyboardButton("Trenches 🏦", callback_data='trenches')],
        [InlineKeyboardButton("Referrals 💸", callback_data='referrals'),
         InlineKeyboardButton("⭐ Watchlist", callback_data='watchlist')],
        [InlineKeyboardButton("Withdraw 💵", callback_data='withdraw'),
         InlineKeyboardButton("⚙️ Settings", callback_data='settings')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ردود الأزرار
RESPONSES = {
    "buy": "✔️ اخترت: Buy 🛒",
    "sell": "✔️ اخترت: Sell 💰",
    "positions": "📊 هذه قائمة الـ Positions",
    "limit_orders": "📌 هذه قائمة الـ Limit Orders",
    "dca_orders": "🔄 هذه قائمة الـ DCA Orders",
    "copy_trade": "📥 هذه قائمة الـ Copy Trade",
    "sniper": "🎯 هذه أداة Sniper",
    "trenches": "🏦 هذه قائمة Trenches",
    "referrals": "💸 هذه صفحة Referrals",
    "watchlist": "⭐ هذه صفحة Watchlist",
    "withdraw": "💵 هذه صفحة Withdraw",
    "settings": "⚙️ هذه إعدادات البوت",
}

# ===== النسخة الجديدة (async, v20+) =====
if NEW_API:
    from telegram.ext import ContextTypes

    async def send_main_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            await update.message.reply_text(get_main_text(), reply_markup=get_main_menu())

    async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "refresh":
            await query.edit_message_text(get_main_text(), reply_markup=get_main_menu())
        else:
            await query.edit_message_text(RESPONSES.get(query.data, "خيار غير معروف"))

    def main():
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", send_main_message))
        from telegram.ext import filters
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_main_message))
        app.add_handler(CallbackQueryHandler(button))
        print("🚀 البوت يشتغل...")
        app.run_polling()

# ===== النسخة القديمة (sync, v13.x) =====
else:
    def send_main_message(update, context):
        update.message.reply_text(get_main_text(), reply_markup=get_main_menu())

    def button(update, context):
        query = update.callback_query
        query.answer()
        if query.data == "refresh":
            query.edit_message_text(get_main_text(), reply_markup=get_main_menu())
        else:
            query.edit_message_text(RESPONSES.get(query.data, "خيار غير معروف"))

    def main():
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", send_main_message))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_main_message))
        dp.add_handler(CallbackQueryHandler(button))
        print("🚀 البوت يشتغل...")
        updater.start_polling()
        updater.idle()

if __name__ == "__main__":
    main()
