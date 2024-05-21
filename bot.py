import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from pytonlib import TonlibClient
import json

# Получение переменных окружения
TOKEN = os.getenv('TOKEN')
TON_WALLET_ADDRESS = os.getenv('TON_WALLET_ADDRESS')

# Настройка TON
client = TonlibClient(ls_index=0)
client.init_tonlib()

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Купить товар 1", callback_data='buy_item_1')],
        [InlineKeyboardButton("Купить товар 2", callback_data='buy_item_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Добро пожаловать! Выберите товар:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    item_data = {
        'buy_item_1': {'name': 'Товар 1', 'price': 10, 'file_id': 'FILE_ID_1'},
        'buy_item_2': {'name': 'Товар 2', 'price': 20, 'file_id': 'FILE_ID_2'}
    }

    item = item_data.get(query.data)
    if item:
        message = f"Вы выбрали {item['name']}. Цена: {item['price']} TON. Переведите сумму на {TON_WALLET_ADDRESS} и отправьте сюда свой адрес кошелька TON."
        context.user_data['selected_item'] = item
        query.edit_message_text(text=message)

def verify_payment(update: Update, context: CallbackContext) -> None:
    user_wallet_address = update.message.text
    selected_item = context.user_data.get('selected_item')
    
    if selected_item:
        transaction = client.get_transactions(TON_WALLET_ADDRESS)
        
        for tx in transaction:
            if tx['in_msg']['source'] == user_wallet_address and tx['in_msg']['value'] == selected_item['price'] * 10**9:
                update.message.reply_text('Платеж подтвержден. Вот ваш товар:')
                update.message.reply_document(document=selected_item['file_id'])
                return
        
        update.message.reply_text('Платеж не найден. Пожалуйста, проверьте правильность введенного адреса или сумму.')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, verify_payment))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
