import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, ContextTypes

# Setup
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Get token from environment
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN not set!")
    exit(1)

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Forex Education Bot!\n\n"
        "📊 Commands:\n"
        "/start - Start\n"
        "/help - Help\n"
        "/position_size - Calculate position size\n"
        "/pip_value - Calculate pip value\n"
        "/risk_reward - Calculate risk-reward ratio\n\n"
        "⚠️ Educational purposes only!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Help\n\n"
        "/position_size [balance] [risk%] [pips]\n"
        "Example: /position_size 10000 2 50\n\n"
        "/pip_value [pair] [lot_size]\n"
        "Example: /pip_value EURUSD 1\n\n"
        "/risk_reward [entry] [stop] [take]\n"
        "Example: /risk_reward 1.1000 1.0950 1.1100"
    )

async def position_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "Usage: /position_size [balance] [risk%] [pips]\n"
                "Example: /position_size 10000 2 50"
            )
            return
        
        balance = float(args[0])
        risk_pct = float(args[1])
        pips = float(args[2])
        
        risk_amount = balance * (risk_pct / 100)
        lot_size = risk_amount / (pips * 10)
        
        await update.message.reply_text(
            f"📊 Position Size\n\n"
            f"Balance: ${balance:,.2f}\n"
            f"Risk: {risk_pct}%\n"
            f"Stop Loss: {pips} pips\n"
            f"Risk Amount: ${risk_amount:,.2f}\n"
            f"Position Size: {round(lot_size, 2)} lots"
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

async def pip_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "Usage: /pip_value [pair] [lot_size]\n"
                "Example: /pip_value EURUSD 1"
            )
            return
        
        pair = args[0].upper()
        lot_size = float(args[1])
        pip_value = 10 * lot_size
        
        await update.message.reply_text(
            f"📊 Pip Value\n\n"
            f"Pair: {pair}\n"
            f"Lot Size: {lot_size}\n"
            f"Pip Value: ${pip_value:,.2f}"
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

async def risk_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "Usage: /risk_reward [entry] [stop] [take]\n"
                "Example: /risk_reward 1.1000 1.0950 1.1100"
            )
            return
        
        entry = float(args[0])
        stop = float(args[1])
        take = float(args[2])
        
        risk = abs(entry - stop)
        reward = abs(take - entry)
        ratio = round(reward / risk, 2) if risk > 0 else 0
        
        await update.message.reply_text(
            f"📊 Risk-Reward\n\n"
            f"Entry: {entry}\n"
            f"Stop: {stop}\n"
            f"Take: {take}\n"
            f"Risk: {round(risk, 4)} pips\n"
            f"Reward: {round(reward, 4)} pips\n"
            f"R:R Ratio: 1:{ratio}"
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

# --- Register Handlers ---
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('position_size', position_size))
dispatcher.add_handler(CommandHandler('pip_value', pip_value))
dispatcher.add_handler(CommandHandler('risk_reward', risk_reward))

# --- Webhook ---
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok', 200

@app.route('/')
def index():
    return 'Forex Bot is running! ✅'

# --- Set Webhook ---
def set_webhook():
    webhook_url = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}/{TOKEN}"
    bot.set_webhook(webhook_url)
    print(f"✅ Webhook set to: {webhook_url}")

# --- Main ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    # Set webhook
    try:
        set_webhook()
    except:
        print("⚠️ Webhook set failed, but bot will still work")
    
    print(f"🚀 Bot is running on port {port}")
    app.run(host='0.0.0.0', port=port)
