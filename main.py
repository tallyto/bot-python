from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from telegram.ext import MessageHandler, Filters

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    if(update.message.text == 'hi'):
        update.message.reply_text('Hi!')
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text=update.message.text)

chave_api = 'sua chave de api'
updater = Updater(chave_api)


# Recebe todas as mensagens do tipo texto
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
updater.dispatcher.add_handler(echo_handler)

# Comandos
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
updater.idle()
