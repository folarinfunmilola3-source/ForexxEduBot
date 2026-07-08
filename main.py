import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

print("🚀 Starting Forex Bot...")

# Get token
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    print("❌ ERROR: TELEGRAM_TOKEN not set!")
    exit(1)

print("✅ Bot token found!")

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **Forex Education Bot**\n\n"
        "📊 **Commands:**\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "/position_size [balance] [risk%] [pips]\n"
        "Example: /position_size 10000 2 50\n\n"
        "/pip_value [pair] [lot_size]\n"
        "Example: /pip_value EURUSD 1\n\n"
        "/risk_reward [entry] [stop] [take]\n"
        "Example: /risk_reward 1.1000 1.0950 1.1100\n\n"
        "⚠️ Educational purposes only!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **Help**\n\n"
        "**Position Size:**\n`/position_size 10000 2 50`\n\n"
        "**Pip Value:**\n`/pip_value EURUSD 1`\n\n"
        "**Risk Reward:**\n`/risk_reward 1.1000 1.0950 1.1100`",
        parse_mode='Markdown'
    )

async def position_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Usage: `/position_size 10000 2 50`", parse_mode='Markdown')
            return
        
        balance = float(args[0])
        risk_pct = float(args[1])
        pips = float(args[2])
        
        risk_amount = balance * (risk_pct / 100)
        lot_size = risk_amount / (pips * 10)
        
        await update.message.reply_text(
            f"📊 **Position Size**\n\n"
            f"Balance: ${balance:,.2f}\n"
            f"Risk: {risk_pct}%\n"
            f"Stop Loss: {pips} pips\n"
            f"Risk Amount: ${risk_amount:,.2f}\n"
            f"**Position Size: {round(lot_size, 2)} lots**",
            parse_mode='Markdown'
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

async def pip_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Usage: `/pip_value EURUSD 1`", parse_mode='Markdown')
            return
        
        pair = args[0].upper()
        lot_size = float(args[1])
        pip_value = 10 * lot_size
        
        await update.message.reply_text(
            f"📊 **Pip Value**\n\n"
            f"Pair: {pair}\n"
            f"Lot Size: {lot_size}\n"
            f"Pip Value: ${pip_value:,.2f}",
            parse_mode='Markdown'
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

async def risk_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Usage: `/risk_reward 1.1000 1.0950 1.1100`", parse_mode='Markdown')
            return
        
        entry = float(args[0])
        stop = float(args[1])
        take = float(args[2])
        
        risk = abs(entry - stop)
        reward = abs(take - entry)
        ratio = round(reward / risk, 2) if risk > 0 else 0
        
        await update.message.reply_text(
            f"📊 **Risk Reward**\n\n"
            f"Entry: {entry}\n"
            f"Stop: {stop}\n"
            f"Take: {take}\n"
            f"Risk: {round(risk, 4)} pips\n"
            f"Reward: {round(reward, 4)} pips\n"
            f"**R:R Ratio: 1:{ratio}**",
            parse_mode='Markdown'
        )
    except:
        await update.message.reply_text("❌ Please enter valid numbers!")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('position_size', position_size))
    app.add_handler(CommandHandler('pip_value', pip_value))
    app.add_handler(CommandHandler('risk_reward', risk_reward))
    
    print("✅ Bot is running! Waiting for messages...")
    app.run_polling()
