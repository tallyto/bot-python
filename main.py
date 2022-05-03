from unicodedata import name
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from telegram.ext import MessageHandler, Filters
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# db config
db_config = {
    'user': 'postgres',
    'password': 'passeiopet',
    'host': 'localhost',
    'port': '5432',
    'database': 'passeiopet'
}

# conect to db with config sqlalchemy
engine = sqlalchemy.create_engine(
    'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_config), echo=True)


# Session
Session = sessionmaker(bind=engine)


# Base
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    nickname = Column(String)

    def __init__(self, id,name, nickname):
        self.id = id
        self.name = name
        self.nickname = nickname

    
Base.metadata.create_all(engine)

session = Session()

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def cadastrar(update: Update, context: CallbackContext) -> None:
    user = User(name=update.message.chat.first_name,
                            nickname=update.message.chat.username,
                            id=update.message.chat.id)

    session.add(user)
    session.commit()
    update.message.reply_text('Digite seu nome')


def start(update: Update, context: CallbackContext) -> None:
    print(update.message.chat)
    update.message.reply_text('Seja bem vindo ao Pet Passeio Bot!\
    \nAqui você poderá agendar consultas e passeios para seu pet 🐶🐱🐷🐸')
    update.message.reply_text('Para começar, digite /help')


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Digite /cadastro para se cadastrar na plataforma\
   \nDigite /agendar para agendar uma consulta\
        \nDigite /passeio para agendar um passeio\
        \nDigite /consultas para ver suas consultas agendadas\
        \nDigite /passeios para ver seus passeios agendados\
        \nDigite /cancelar para cancelar uma consulta ou passeio\
        \nDigite /sair para sair do Pet Passeio Bot')


def echo(update: Update, context: CallbackContext) -> None:
    if(update.message.text == 'hi'):
        update.message.reply_text('Hi!')
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id, text=update.message.text)


chave_api = 'sua_api_key'
updater = Updater(chave_api)


# Recebe todas as mensagens do tipo texto
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
updater.dispatcher.add_handler(echo_handler)

# Comandos
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('cadastro', cadastrar))

updater.start_polling()
updater.idle()


