import dataset
import telebot

from config import settings
from os import environ

db = dataset.connect(environ['DATABASE_URL'])
table = db[settings.USER]
bot = telebot.TeleBot(environ['TOKEN'])


@bot.message_handler(commands=["start"])
def start(message):
    if table.find_one(id=message.chat.id) == None:
        response = (
            "Bem vindo ao alerta de noticias do NEI UFRN.\n"
            "Você agora será alertado sempre que uma noticia nova for postada "
            "no portal de noticias do NEI UFRN.\n"
            "Para remover o seu cadastro, basta enviar a mensagem: /sair"
        )
        user_name = message.from_user.username
        full_name = (
            f"{message.from_user.first_name}" f"{message.from_user.last_name.strip()}"
            if message.from_user.last_name != None
            else ""
        )
        print("New user",user_name, full_name)
        table.insert(dict(id=message.chat.id, user_name=user_name, full_name=full_name))
    else:
        response = "Você já está cadastrado."
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["sair"])
def start(message):
    if table.find_one(id=message.chat.id) == None:
        response = (
            "Você não está cadastrado.\n"
            "Envie a mensagem: /start para iniciar o recebimento de noticias do NEI UFRN"
        )
    else:
        response = (
            "Seu cadastro para alerta das noticias do NEI UFRN foi removido.\n"
            "Caso deseja voltar a receber alertas, envie a mensagem: /start"
        )
        table.delete(id=message.chat.id)
    print(f'User {message.chat.id} left')
    bot.send_message(message.chat.id, response)
    


def send_noticia(title, url):
    response = "Nova noticia:\n" f"{title}\n{url}"
    users = table.find()
    for user in users:
        bot.send_message(user["id"], response)
    return True


if __name__ == "__main__":
    bot.polling()
