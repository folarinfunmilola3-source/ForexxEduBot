import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Import utility modules
from utils.calculators import *
from utils.market_data import *
from utils.educational import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    welcome_text = """
    🚀 Welcome to the Forex Education Bot!

    I'm here to help you learn Forex trading through educational tools and simulators.

    📊 Available Commands:
    /help - Show all available commands
    /education - Learn Forex basics
    /position_size - Calculate position size
    /pip_value - Calculate pip value
    /risk_reward - Calculate risk-reward ratio
    /pivot_points - Calculate daily pivot points
    /economic_calendar - View upcoming economic events
    /sentiment - Check market sentiment
    /quiz - Take a Forex knowledge quiz

    ⚠️ Disclaimer: This bot is for educational purposes only. 
    All tools are simulators and do not provide financial advice.
    """
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    help_text = """
    📚 **Forex Education Bot - Help Center**

    **Calculators:**
    /position_size - Calculate your optimal lot size
    /pip_value - Calculate the value of 1 pip
    /risk_reward - Calculate your risk-to-reward ratio
    /pivot_points - Get daily pivot levels

    **Market Analysis:**
    /economic_calendar - See upcoming news events
    /sentiment - Get market sentiment overview

    **Education:**
    /education - Learn Forex terminology
    /quiz - Test your Forex knowledge

    **Account Management:**
    /set_balance - Set your account balance
    /set_risk - Set your risk percentage
    /profile - View your current settings

    *All calculations are for educational purposes only.*
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send educational content."""
    keyboard = [
        [InlineKeyboardButton("📖 Forex Basics", callback_data='edu_basics')],
        [InlineKeyboardButton("📊 Candlestick Patterns", callback_data='edu_candlesticks')],
        [InlineKeyboardButton("📈 Technical Indicators", callback_data='edu_indicators')],
        [InlineKeyboardButton("💰 Risk Management", callback_data='edu_risk')],
        [InlineKeyboardButton("🔙 Back to Main", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎓 **Forex Education Center**\n\nChoose a topic to learn more:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def position_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate position size."""
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "📊 **Position Size Calculator**\n\n"
                "Usage: `/position_size [account_balance] [risk_percentage] [stop_loss_pips]`\n\n"
                "Example: `/position_size 10000 2 50`\n"
                "This calculates the lot size for a $10,000 account risking 2% with a 50 pip stop loss.",
                parse_mode='Markdown'
            )
            return
        
        balance = float(args[0])
        risk_pct = float(args[1])
        stop_loss_pips = float(args[2])
        
        result = calculate_position_size(balance, risk_pct, stop_loss_pips)
        
        await update.message.reply_text(
            f"📊 **Position Size Calculation**\n\n"
            f"Account Balance: ${balance:,.2f}\n"
            f"Risk Percentage: {risk_pct}%\n"
            f"Stop Loss: {stop_loss_pips} pips\n"
            f"Risk Amount: ${result['risk_amount']:,.2f}\n"
            f"Position Size: {result['lot_size']} lots\n\n"
            f"*Based on standard lot (100,000 units) using USD as quote currency*",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Please enter valid numbers.")

async def pip_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate pip value."""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "📊 **Pip Value Calculator**\n\n"
                "Usage: `/pip_value [currency_pair] [lot_size]`\n\n"
                "Example: `/pip_value EURUSD 1`\n"
                "This calculates the pip value for 1 standard lot of EUR/USD.",
                parse_mode='Markdown'
            )
            return
        
        pair = args[0].upper()
        lot_size = float(args[1])
        
        result = calculate_pip_value(pair, lot_size)
        
        await update.message.reply_text(
            f"📊 **Pip Value Calculation**\n\n"
            f"Currency Pair: {pair}\n"
            f"Lot Size: {lot_size}\n"
            f"Pip Value: ${result['pip_value']:,.2f}\n\n"
            f"*Calculated based on standard pip sizes*",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Please enter valid numbers.")

async def risk_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate risk-reward ratio."""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "📊 **Risk-Reward Ratio Calculator**\n\n"
                "Usage: `/risk_reward [entry_price] [stop_loss] [take_profit]`\n\n"
                "Example: `/risk_reward 1.1000 1.0950 1.1100`\n"
                "This calculates the R:R ratio for your trade setup.",
                parse_mode='Markdown'
            )
            return
        
        entry = float(args[0])
        stop = float(args[1])
        take = float(args[2])
        
        result = calculate_risk_reward(entry, stop, take)
        
        await update.message.reply_text(
            f"📊 **Risk-Reward Analysis**\n\n"
            f"Entry: {entry}\n"
            f"Stop Loss: {stop}\n"
            f"Take Profit: {take}\n"
            f"Risk: {result['risk']} pips\n"
            f"Reward: {result['reward']} pips\n"
            f"**R:R Ratio: 1:{result['ratio']}**\n\n"
            f"*A higher R:R ratio means better risk management*",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Please enter valid numbers.")

async def pivot_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate pivot points."""
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text(
                "📊 **Pivot Points Calculator**\n\n"
                "Usage: `/pivot_points [high] [low] [close]`\n\n"
                "Example: `/pivot_points 1.1050 1.0950 1.1000`\n"
                "This calculates the daily pivot levels for your trading.",
                parse_mode='Markdown'
            )
            return
        
        high = float(args[0])
        low = float(args[1])
        close = float(args[2])
        
        result = calculate_pivot_points(high, low, close)
        
        await update.message.reply_text(
            f"📊 **Daily Pivot Points**\n\n"
            f"Pivot: {result['pivot']}\n"
            f"R1: {result['r1']} | S1: {result['s1']}\n"
            f"R2: {result['r2']} | S2: {result['s2']}\n"
            f"R3: {result['r3']} | S3: {result['s3']}\n\n"
            f"*R = Resistance, S = Support*",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Please enter valid numbers.")

async def economic_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show upcoming economic events."""
    events = get_economic_events()
    message = "📅 **Upcoming Economic Events**\n\n"
    for event in events[:5]:
        message += f"• {event['time']} - {event['currency']}: {event['event']}\n"
        message += f"  Impact: {event['impact']} | Forecast: {event['forecast']}\n\n"
    message += "*Data is for educational purposes*"
    await update.message.reply_text(message, parse_mode='Markdown')

async def sentiment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show market sentiment."""
    sentiment_data = get_market_sentiment()
    message = "📊 **Market Sentiment Overview**\n\n"
    for pair, data in sentiment_data.items():
        message += f"**{pair}**\n"
        message += f"Sentiment: {data['sentiment']}\n"
        message += f"Strength: {data['strength']}/10\n\n"
    await update.message.reply_text(message, parse_mode='Markdown')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a Forex quiz."""
    question = get_quiz_question()
    keyboard = [
        [InlineKeyboardButton(option, callback_data=f'quiz_{option}')]
        for option in question['options']
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"📝 **Forex Quiz**\n\n{question['question']}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# --- Callback Query Handlers ---

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'back_to_start':
        await start(update, context)
    
    elif data == 'edu_basics':
        await query.edit_message_text(
            "📖 **Forex Basics**\n\n"
            "Forex (Foreign Exchange) is the global market for trading currencies.\n\n"
            "**Key Concepts:**\n"
            "• **Currency Pair:** e.g., EUR/USD\n"
            "• **Base Currency:** First currency in pair\n"
            "• **Quote Currency:** Second currency in pair\n"
            "• **Spread:** Difference between bid and ask price\n\n"
            "📌 *This is the foundation of all Forex trading.*",
            parse_mode='Markdown'
        )
    
    elif data == 'edu_candlesticks':
        await query.edit_message_text(
            "📊 **Candlestick Patterns**\n\n"
            "Candlesticks show price movement for a specific period.\n\n"
            "**Common Patterns:**\n"
            "• **Doji:** Market indecision\n"
            "• **Hammer:** Potential reversal at bottom\n"
            "• **Shooting Star:** Potential reversal at top\n"
            "• **Engulfing:** Strong reversal signal\n\n"
            "📌 *Patterns are more reliable with confirmation.*",
            parse_mode='Markdown'
        )
    
    elif data == 'edu_indicators':
        await query.edit_message_text(
            "📈 **Technical Indicators**\n\n"
            "Indicators help analyze market conditions.\n\n"
            "**Popular Indicators:**\n"
            "• **RSI:** Overbought/oversold conditions\n"
            "• **MACD:** Trend strength and direction\n"
            "• **Bollinger Bands:** Volatility measurement\n"
            "• **Moving Averages:** Trend identification\n\n"
            "📌 *Use 2-3 indicators for confirmation.*",
            parse_mode='Markdown'
        )
    
    elif data == 'edu_risk':
        await query.edit_message_text(
            "💰 **Risk Management**\n\n"
            "Protecting your capital is the #1 rule.\n\n"
            "**Golden Rules:**\n"
            "• Risk 1-2% per trade maximum\n"
            "• Always use stop-loss orders\n"
            "• Aim for 1:2 or higher R:R ratio\n"
            "• Never revenge trade\n"
            "• Keep a trading journal\n\n"
            "📌 *Risk management separates professionals from amateurs.*",
            parse_mode='Markdown'
        )
    
    elif data.startswith('quiz_'):
        answer = data.replace('quiz_', '')
        correct = check_quiz_answer(answer)
        if correct:
            await query.edit_message_text("✅ Correct! Well done! 🎉")
        else:
            await query.edit_message_text("❌ Not quite right. Keep learning! 💪")

# --- Main Function ---

if __name__ == '__main__':
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN environment variable not set!")
    
    application = ApplicationBuilder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('education', education))
    application.add_handler(CommandHandler('position_size', position_size))
    application.add_handler(CommandHandler('pip_value', pip_value))
    application.add_handler(CommandHandler('risk_reward', risk_reward))
    application.add_handler(CommandHandler('pivot_points', pivot_points))
    application.add_handler(CommandHandler('economic_calendar', economic_calendar))
    application.add_handler(CommandHandler('sentiment', sentiment))
    application.add_handler(CommandHandler('quiz', quiz))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    logger.info("Forex Education Bot started!")
    application.run_polling()
