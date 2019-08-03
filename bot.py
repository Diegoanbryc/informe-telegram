# bot.py
import mysql.connector
from mysql.connector import Error
import subprocess
import requests  
import os
from flask import Flask, request
# Add your telegram token as environment variable
BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'


try:
    connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                             database='sql10282729',
                             user='sql10282729',
                             password='haM6SHtrmF')
    if connection.is_connected():
       db_Info = connection.get_server_info()
       print("Connected to MySQL database... MySQL Server version on ",db_Info)
       cursor = connection.cursor()
       cursor.execute("select database();")
       record = cursor.fetchone()
       print ("Your connected to - ", record)
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.json

    print(data)  # Comment to hide what Telegram is sending you
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    if message == "Informe" or message == "informe":
        print("Entro al if")
        json_data = {"chat_id": chat_id, "text": "En el laboratorio RYC se encuentran trabajos de: ",}
        #subprocess.call(["php", "consultaexterna.php"])
    elif message == "Hola" or message =="hola":
        json_data = {"chat_id": chat_id, "text": "Hola, Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
    else:
        json_data = {"chat_id": chat_id, "text": "Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
        

   

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)
    
    return ''


if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
