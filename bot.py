# bot.py
import requests  
import os
from flask import Flask, request
# Add your telegram token as environment variable
BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'


app = Flask(__name__)


@app.route('/', methods=['POST'])

def start_callback(update, context):
    update.message.reply_text("Welcome to my awesome bot!")



dispatcher.add_handler(CommandHandler("start", start_callback))

def main():  
    data = request.json

    print(data)  # Comment to hide what Telegram is sending you
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    json_data = {
        "chat_id": chat_id,
        "text": message,
    }

    message_url = BOT_URL + 'sendmessage'
    requests.post(message_url, json=json_data)
   # print(message_url)
    return ''


if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
