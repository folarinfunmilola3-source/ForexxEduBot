import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text(
        "🚀 Welcome to the Forex Education Bot!\n\n"
        "I'm here to help you learn Forex trading.\n\n"
        "📊 Available Commands:\n"
        "/start - Start the bot\n"
        "/help - Show all commands\n"
        "/position_size - Calculate position size\n"
        "/pip_value - Calculate pip value\n"
        "/risk_reward - Calculate risk-reward ratio\n\n"
        "⚠️ For educational purposes only!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    await update.message.reply_text(
        "📚 Forex Education Bot - Help\n\n"
        "Commands:\n"
        "/position_size [balance] [risk%] [stop_loss_pips]\n"
        "Example: /position_size 10000 2 50\n\n"
        "/pip_value [pair] [lot_size]\n"
        "Example: /pip_value EURUSD 1\n\n"
        "/risk_reward [entry] [stop] [take]\n"
        "Example: /risk_reward 1.1000 1.0950 1.1100\n\n"
        "All calculations are for educational purposes only!"
    )

async def position_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate position size."""
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "📊 Position Size Calculator\n\n"
                "Usage: /position_size [balance] [risk%] [stop_loss_pips]\n"
                "Example: /position_size 10000 2 50"
            )
            return
        
        balance = float(args[0])
        risk_pct = float(args[1])
        stop_loss_pips = float(args[2])
        
        risk_amount = balance * (risk_pct / 100)
        lot_size = risk_amount / (stop_loss_pips * 10)
        
        await update.message.reply_text(
            f"📊 Position Size Calculation\n\n"
            f"Account Balance: ${balance:,.2f}\n"
            f"Risk Percentage: {risk_pct}%\n"
            f"Stop Loss: {stop_loss_pips} pips\n"
            f"Risk Amount: ${risk_amount:,.2f}\n"
            f"Position Size: {round(lot_size, 2)} lots"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Please enter valid numbers!")

async def pip_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate pip value."""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "📊 Pip Value Calculator\n\n"
                "Usage: /pip_value [pair] [lot_size]\n"
                "Example: /pip_value EURUSD 1"
            )
            return
        
        pair = args[0].upper()
        lot_size = float(args[1])
        pip_value = 10 * lot_size
        
        await update.message.reply_text(
            f"📊 Pip Value Calculation\n\n"
            f"Currency Pair: {pair}\n"
            f"Lot Size: {lot_size}\n"
            f"Pip Value: ${pip_value:,.2f}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Please enter valid numbers!")

async def risk_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate risk-reward ratio."""
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "📊 Risk-Reward Calculator\n\n"
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
            f"📊 Risk-Reward Analysis\n\n"
            f"Entry: {entry}\n"
            f"Stop Loss: {stop}\n"
            f"Take Profit: {take}\n"
            f"Risk: {risk} pips\n"
            f"Reward: {reward} pips\n"
            f"R:R Ratio: 1:{ratio}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Please enter valid numbers!")

# --- Error Handler ---

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.warning(f'Update {update} caused error {context.error}')

# --- Main Function ---

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if not token:
        print("❌ ERROR: TELEGRAM_TOKEN not set!")
        exit(1)
    
    print("✅ Bot token found!")
    print("🚀 Starting Forex Education Bot...")
    
    # Create application
    application = ApplicationBuilder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('position_size', position_size))
    application.add_handler(CommandHandler('pip_value', pip_value))
    application.add_handler(CommandHandler('risk_reward', risk_reward))
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling()
