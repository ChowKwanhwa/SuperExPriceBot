import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from test_superex import SuperExAPI

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """发送开始消息"""
    await update.message.reply_text('欢迎使用 SuperEx 价格查询机器人！\n请直接发送交易对符号（如 BTC 或 ETH）来查询价格。')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """发送帮助消息"""
    await update.message.reply_text('直接发送交易对符号（如 BTC 或 ETH）来查询价格。')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户消息"""
    symbol = update.message.text.strip().upper()
    
    if not symbol:
        await update.message.reply_text('请输入交易对符号')
        return

    # 如果用户只输入了币种，自动添加 _USDT
    if '_' not in symbol:
        symbol = f'{symbol}_USDT'

    try:
        # 获取市场数据
        market_data = api.get_market_data(symbol)
        
        if market_data:
            # 格式化响应消息
            response = (
                f"🏦 {symbol} 价格信息:\n\n"
                f"💰 当前价格: {market_data['last']}\n"
                f"📈 24h 最高: {market_data['high']}\n"
                f"📉 24h 最低: {market_data['low']}\n"
                f"💎 24h 成交量: {market_data['volume']}\n"
                f"📊 24h 涨跌: {market_data['change']}%"
            )
        else:
            response = f"❌ 未找到 {symbol} 的价格信息"
            
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text(f"❌ 获取 {symbol} 价格时出错，请稍后重试")

def main():
    """启动机器人"""
    # 从环境变量获取 token
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("No token found! Please set BOT_TOKEN environment variable.")
        return

    # 创建应用
    application = Application.builder().token(token).build()

    # 添加处理程序
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 启动机器人
    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
