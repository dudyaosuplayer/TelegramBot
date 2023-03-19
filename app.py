import telebot
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k in keys.keys():
        text = '\n'.join((text, k))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Неправильное кол-во параметров в запросе!')

        base, quote, amount = values
        value = APIParser().convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду: \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {float(amount) * value}'
        bot.send_message(message.chat.id, text)


bot.polling()
