import os
import logging
import openai
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включите логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.first_name}! Я бот GPT-4. Спроси меня о чем угодно.')

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Отправка сообщения GPT-4 через OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )

    bot_response = response.choices[0].text.strip()

    # Ответ бота
    context.bot.send_message(chat_id=chat_id, text=bot_response)

def main() -> None:
    # Токены
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Установка токена для OpenAI
    openai.api_key = OPENAI_API_KEY

    # Создание объекта Updater и передача ему токена бота
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    # Добавление обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
