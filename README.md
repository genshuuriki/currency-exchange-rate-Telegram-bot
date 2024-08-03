# Currency Exchange Rate Bot
A Telegram bot that provides official currency exchange rates set by the Central Bank of the Russian Federation. Users can retrieve exchange rates for the current date or a specific date and search for specific currencies.

# Features
· 📅 Get exchange rates for the current date<br>
· 📅 Get exchange rates for a specific date<br>
· 🔍 Search for specific currencies by code or name<br>
· 🗓️ Historical exchange rates from 01.07.1992 to the present

# Installation
1. Clone the repository:<br>
  git clone https://github.com/genshuuriki/currency-exchange-rate-Telegram-bot.git<br>
  cd currency-exchange-rate-bot<br>

2. Create a virtual environment and install dependencies:<br>
  python3 -m venv venv<br>
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`<br>
  pip install -r requirements.txt

3. Set up your Telegram Bot API key:<br>
  ·Obtain an API key from the Telegram BotFather.<br>
  ·Create a .env file in the root directory and add your API key:<br>
    API_KEY=your_api_key_here

# Usage
1. Start the bot<br>
   python bot.py

2. Interact with the bot on Telegram:<br>
  · Send '/start' to begin.<br>
  · Use the provided buttons to get exchange rates or search for specific currencies.

# Commands
  · '/start' - Start the bot and see available options

# How It Works
The bot scrapes currency exchange rate data from the Central Bank of Russia's website using BeautifulSoup and provides formatted results to users. It supports queries for current and historical rates and allows users to search for specific currencies by their code or name.

# Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

# License
This project is licensed under the MIT License.
