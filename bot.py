import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from test_superex import SuperExAPI
import re

# 加载.env文件
load_dotenv()

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 设置第三方库的日志级别为WARNING
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('apscheduler').setLevel(logging.WARNING)

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

async def handle_price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理价格查询命令"""
    if not update.message or not update.message.text:
        return
        
    command = update.message.text[1:].split()[0].upper()  # 去掉/并获取第一个词
    if command in ["START", "HELP"]:  # 忽略 start 和 help 命令
        return
        
    # 添加 _USDT 后缀
    if '_' not in command:
        command = f"{command}_USDT"
        
    # 获取价格信息
    price_info = api.get_market_summary(command)
    
    # 发送响应
    await update.message.reply_text(
        format_price_message(price_info),
        parse_mode='HTML'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令"""
    await update.message.reply_text(
        'Hi! I am SuperEx Price Bot! 🤖\n\n'
        'Use commands like /btc or /eth to get price information.\n\n'
        'Examples:\n'
        '/btc - for BTC/USDT price\n'
        '/eth - for ETH/USDT price\n'
        '/bnb - for BNB/USDT price'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /help 命令"""
    await update.message.reply_text(
        'Use commands to get price information:\n\n'
        'Examples:\n'
        '/btc - Shows BTC/USDT price\n'
        '/eth - Shows ETH/USDT price\n'
        '/dot - Shows DOT/USDT price'
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
    
    # 注册价格查询命令处理器
    # 使用正则表达式过滤器匹配以/开头后跟字母的命令
    price_filter = filters.Regex(r'^/[a-zA-Z]+$')
    application.add_handler(MessageHandler(price_filter, handle_price_command))

    # 启动机器人
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
