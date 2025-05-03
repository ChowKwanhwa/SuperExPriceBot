import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from test_superex import SuperExAPI

# 加载.env文件
load_dotenv()

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 创建 SuperEx API 实例
api = SuperExAPI()

def format_price_message(ticker_data):
    """格式化价格信息消息"""
    if "error" in ticker_data:
        return f"Error: {ticker_data['error']}"
    
    return (
        f"💰 {ticker_data['symbol']} Price Info:\n\n"
        f"Current Price: ${ticker_data['last_price']:,.2f}\n"
        f"24h High: ${ticker_data['24h_high']:,.2f}\n"
        f"24h Low: ${ticker_data['24h_low']:,.2f}\n"
        f"24h Volume: {ticker_data['24h_volume']:,.2f} {ticker_data['symbol'].split('_')[0]}\n"
        f"24h Change: {ticker_data['24h_change']}%"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理用户消息"""
    text = update.message.text.upper()
    
    # 如果消息是单个词，假设它是一个交易对
    if len(text.split()) == 1:
        # 添加 _USDT 后缀（如果需要）
        symbol = f"{text}_USDT" if "_" not in text else text
        
        # 获取价格信息
        price_info = api.get_market_summary(symbol)
        
        # 发送响应
        await update.message.reply_text(
            format_price_message(price_info),
            parse_mode='HTML'
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令"""
    await update.message.reply_text(
        'Hi! I am SuperEx Price Bot! 🤖\n\n'
        'Send me a ticker symbol (e.g., BTC or ETH) to get the latest price information.\n\n'
        'Examples:\n'
        'BTC - for BTC/USDT price\n'
        'ETH - for ETH/USDT price\n'
        'BTC_ETH - for BTC/ETH price'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /help 命令"""
    await update.message.reply_text(
        'Send me a ticker symbol to get price information.\n\n'
        'Examples:\n'
        'BTC - Shows BTC/USDT price\n'
        'ETH - Shows ETH/USDT price\n'
        'DOT - Shows DOT/USDT price'
    )

def main() -> None:
    """启动机器人"""
    # 从环境变量获取 token
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("No token found! Please set BOT_TOKEN environment variable.")
        return

    # 创建 Application
    application = Application.builder().token(token).build()

    # 注册命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # 注册消息处理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 启动机器人
    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
