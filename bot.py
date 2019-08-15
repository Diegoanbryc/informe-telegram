# bot.py
import time
import MySQLdb
import subprocess
import requests  
import os
from datetime import datetime
from flask import Flask, request
# Add your telegram token as environment variable
BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'


app = Flask(__name__)

# Open database connection
db = MySQLdb.connect("sql10.freemysqlhosting.net","sql10282729","haM6SHtrmF","sql10282729" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")


# Fetch a single row using fetchone() method.
data2 = cursor.fetchone()
print("Conecto a la base de datos externa:")
print(data2)
cursor.execute("SET lc_time_names = 'es_ES'")
sql = ("select count(date(OrderDate)),DAYNAME(date(OrderDate)),date(OrderDate),DATEDIFF(date(now()),date(OrderDate)),(5 * (DATEDIFF(date(curdate()), date(OrderDate)) DIV 7) + MID('0123444401233334012222340111123400012345001234550', 7 * WEEKDAY(date(OrderDate)) + WEEKDAY(date(curdate())) + 1, 1)) AS DiasAtraso from Estadodellab GROUP BY date(OrderDate)")


@app.route('/', methods=['POST'])
def main():
    data = request.json

    print(data)  # Comment to hide what Telegram is sending you
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    if message == "Informe" or message == "informe":
        print("Entro al if")
        json_data = {"chat_id": chat_id, "text": "En el laboratorio RYC se encuentran trabajos de: ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        cursor.execute(sql)
        dataselect = cursor.fetchall()
       # time.sleep(3)
        json_data = {"chat_id": chat_id, "text": "|Cantidad | Día     | Fecha Calculado| Días de atraso|: ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
       # time.sleep(3)
        for row in dataselect:
            json_data = {"chat_id": chat_id, "text": "|   "+str(row[0])+"      | "+str(row[1])+"   |  /"+str(row[2].strftime("%Y_%m_%d"))+"   |  "+str(row[4])+"      |",}
            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data)
            print("Cantidad de trabajos = ", row[0], )
            print("Día = ", row[1])
            print("Fecha calculado = ", row[2])
            print("Dias calendario  = ", row[3])
            print("Dias de proceso  = ", row[4], "\n")
            #time.sleep(3)
            
        json_data = {"chat_id": chat_id, "text": "Los días de atraso no tienen en cuenta ni Sábados ni Domingos, Ahora selecciona la fecha de realizado el cálculo, para obtener información de los trabajos de esa fecha.",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)        
            
            
        
        
    elif message == "Hola" or message =="hola":
        json_data = {"chat_id": chat_id, "text": "Hola, Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        
    elif message.startswith( '/20' ):
        fechaconsulta = datetime.strptime(message,'/%y_%m_%d')
        print("Va a consultar los trabajos con fecha de:", fechaconsulta)
    else:
        json_data = {"chat_id": chat_id, "text": "Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        

   
           
  
    
    return ''


if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
