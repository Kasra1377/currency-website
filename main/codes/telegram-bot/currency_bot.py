import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from token_address import TOKEN
import pandas as pd
import numpy as np

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

def update_description():
    currency_description = """
    دلار آمریکا : {}
    یورو : {}
    لیر ترکیه : {}
    پوند انگلیس : {}
    درهم امارات : {}
    """
    main_page_currency_table = pd.read_csv("..\codes\data\datasets\main_page_table\main_page_currency_table.csv")
    # main_page_currency_table.index = main_page_currency_table["Currency"]
    values = main_page_currency_table["Live Value"].to_list()
    values = [int(np.floor(value / 10)) for value in values]
    return currency_description.format(*values)

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update_description()
    await context.bot.send_message(chat_id=update._effective_chat.id,
            text=text)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    
    currency_handler = CommandHandler("currency", currency)
    application.add_handler(currency_handler)

    application.run_polling()