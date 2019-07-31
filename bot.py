# bot.py
import requests  
import os
from flask import Flask, request
import telebot

TOKEN = '809561101:AAFiwB9lCLotI20CeP82B5JjGGhw6pxue18'

bot = telebot.TeleBot(TOKEN)
# Add your telegram token as environment variable
#BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'


#app = Flask(__name__)


#@app.route('/', methods=['POST'])

#def main():  
#    data = request.json

#    print(data)  # Comment to hide what Telegram is sending you
#    chat_id = data['message']['chat']['id']
#    message = data['message']['text']

#    json_data = {
#        "chat_id": chat_id,
#        "text": message,
#    }

#    message_url = BOT_URL + 'sendmessage'
#    requests.post(message_url, json=json_data)
  
#    return ''

def echo_messages(*messages):
   # """
  #  Echoes all incoming messages of content_type 'text'.
   # """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'informe':
            text = m.text
            bot.send_message(chatid, text)
 
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
    
bot.set_update_listener(echo_messages)
bot.polling()

while True: # Don't let the main Thread end.
    pass

#####################################################################################################
          
            
#f __name__ == '__main__':  
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port, debug=True)
