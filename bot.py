import os
import logging
import openai
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from flask import Flask, request

# Включите логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Flask приложение
app = Flask(__name__)

# Функция для команды /start
def start(update: Update, context) -> None:
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.first_name}! Я бот GPT-4. Спроси меня о чем угодно.')

# Функция для обработки сообщений
def handle_message(update: Update, context) -> None:
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

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    if request.method == "POST":
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
        return "OK"
    return "Webhook is working!"

def main() -> None:
    # Токены
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Установка токена для OpenAI
    openai.api_key = OPENAI_API_KEY

    # Создание объекта Bot и Dispatcher
    global bot
    bot = Bot(token=TELEGRAM_TOKEN)
    global dispatcher
    dispatcher = Dispatcher(bot, None, use_context=True)

    # Добавление обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Установка Webhook
    webhook_url = f'grosh-production.up.railway.app.railway.app/webhook'
    bot.set_webhook(webhook_url)

    # Запуск Flask приложения
    app.run(port=5000)

if __name__ == '__main__':
    main()
