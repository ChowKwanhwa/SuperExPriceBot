# SuperEx Price Bot

A Telegram bot that provides real-time cryptocurrency price information from SuperEx exchange.

## Features

- Get real-time price information for any trading pair
- View 24-hour high/low prices
- Check trading volume
- Monitor price changes

## Setup

1. Clone the repository:
```bash
git clone https://github.com/ChowKwanhwa/SuperExPriceBot.git
cd SuperExPriceBot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Telegram bot token:
```
BOT_TOKEN=your_bot_token_here
```

4. Run the bot:
```bash
python bot.py
```

## Usage

- Send any trading pair symbol (e.g., `BTC` or `ETH`) to get its current price
- The bot will automatically add `_USDT` if no trading pair is specified
- Use `/start` or `/help` to get usage instructions

## Dependencies

- python-telegram-bot>=20.0
- requests==2.31.0
- urllib3>=2.0.7
- certifi>=2025.1.31
- python-dotenv>=1.0.0
