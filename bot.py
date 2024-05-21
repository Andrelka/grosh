import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включите логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я твой бот.')

# Функция для обработки текстовых сообщений
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main() -> None:
    # Получите токен из переменных окружения
    token = os.getenv("TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    # Команда /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
