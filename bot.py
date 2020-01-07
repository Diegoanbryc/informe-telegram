# bot.py
import time
import MySQLdb
import subprocess
import requests  
import os
from datetime import datetime
from flask import Flask, request
MySQLdb.paramstyle

# Add your telegram token as environment variable
BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'


app = Flask(__name__)

# Open database connection
db = MySQLdb.connect("remotemysql.com","eJ10VkV0Jh","pCSRNFAXcF","eJ10VkV0Jh" )

# prepare a cursor object using cursor() method
  # Check if connection was successful
if db:
    # Carry out normal procedure
    print("Connection successful")
else:
    # Terminate
    print("Connection unsuccessful")

cursor = db.cursor()
# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")


# Fetch a single row using fetchone() method.
data2 = cursor.fetchone()
print("Conecto a la base de datos externa:")
print(data2)
cursor.execute("SET lc_time_names = 'es_ES'")
cursor.execute("set session sql_mode='TRADITIONAL';")
sql = "select count(date(OrderDate)),DAYNAME(date(OrderDate)),date(OrderDate),DATEDIFF(date(now()),date(OrderDate)),(5 * (DATEDIFF(date(curdate()), date(OrderDate)) DIV 7) + MID('0123444401233334012222340111123400012345001234550', 7 * WEEKDAY(date(OrderDate)) + WEEKDAY(date(curdate())) + 1, 1)) AS DiasAtraso from Estadodellab GROUP BY date(OrderDate) ORDER BY  DiasAtraso DESC"
sqlinfofecha ="select OrderID, CommNr, TrayNumber, CASE WHEN Status = 0 THEN 'Tilaus vastaanote' WHEN Status = 1 THEN 'Rx entrysuccessfull' WHEN Status = 2 THEN 'Out of Stock' WHEN Status = 3 THEN 'In calculation' WHEN Status = 4 THEN 'Waiting for Information' WHEN Status = 5 THEN 'Waiting for frame' WHEN Status = 6 THEN 'Recoger en Stock' WHEN Status = 7 THEN 'Tuotannossa' WHEN Status = 8 THEN 'ALLOY BLOCKER' WHEN Status = 9 THEN 'FREEFORM GENERATOR' WHEN Status = 10 THEN 'FREEFORM POLISH' WHEN Status = 11 THEN 'Conventional RX' WHEN Status = 12 THEN 'LASER' WHEN Status = 13 THEN 'Control de Calidad' WHEN Status = 14 THEN 'Hard Coating' WHEN Status = 15 THEN 'Hard Coating' WHEN Status = 16 THEN 'Entra a AR' WHEN Status = 17 THEN 'Bisel previo a AR' WHEN Status = 18 THEN 'Bisel' WHEN Status = 19 THEN 'Bisel Final' WHEN Status = 20 THEN 'Sale de AR' WHEN Status = 21 THEN 'Control Final' WHEN Status = 22 THEN 'Enviados' WHEN Status = 23 THEN 'Factura' WHEN Status = 24 THEN 'Cancelled' WHEN Status = -2 THEN 'Error' WHEN Status = 25 THEN 'Desbloqueo' ELSE 'No aparece estado en el laboratorio' END AS Estado FROM Estadodellab where OrderDate like {0}" 

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
        try:
            cursor.execute(sql)
            
            dataselect = cursor.fetchall()
	    time.sleep(3)
            json_data = {"chat_id": chat_id, "text": "|Cantidad | Día     | Fecha Calculado| Días de atraso|: ",}
            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data)
			# time.sleep(3)
            for row in dataselect:
                print("Cantidad de trabajos = ", row[0], )
                print("Día = ", row[1])
                print("Fecha calculado = ", row[2])
                print("Dias calendario  = ", row[3])
                print("Dias de proceso  = ", row[4], "\n")
                json_data = {"chat_id": chat_id, "text": "|   "+str(row[0])+"      | "+str(row[1])+"   |  /"+str(row[2].strftime("%Y_%m_%d"))+"   |  "+str(row[4])+"      |",}
                message_url = BOT_URL + 'sendMessage'
                requests.post(message_url, json=json_data)
            #time.sleep(3)

            json_data = {"chat_id": chat_id, "text": "Los días de atraso no tienen en cuenta ni Sábados ni Domingos, Ahora selecciona la fecha de realizado el cálculo, para obtener información de los trabajos de esa fecha.",}
            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data) 
	    return None
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            json_data = {"chat_id": chat_id, "text": "Error en la conexion con la base de datos, por favor intente mas tarde",}
            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data)
            cursor.close()
            time.sleep(2)
            cursor = db.cursor()
            # execute SQL query using execute() method.
            cursor.execute("SELECT VERSION()")


            # Fetch a single row using fetchone() method.
            data2 = cursor.fetchone()
            print("Conecto a la base de datos externa:")
            print(data2)
            return None
            
        
        
            elif message == "Hola" or message =="hola":
                json_data = {"chat_id": chat_id, "text": "Hola, Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
                message_url = BOT_URL + 'sendMessage'
                requests.post(message_url, json=json_data)
        
            elif message.startswith( '/20' ):
                fechaconsulta = datetime.strptime(message,"/%Y_%m_%d").date()
                print("Va a consultar los trabajos con fecha de:", fechaconsulta)
                json_data = {"chat_id": chat_id, "text": "A continuación se muestran los trabajos presentes en el laboratorio de la fecha "+message+": ",}
                message_url = BOT_URL + 'sendMessage'
                requests.post(message_url, json=json_data)
                a="'"+fechaconsulta.strftime("/%Y-%m-%d")[1:]+"%'"
				try:
					cursor.execute(sqlinfofecha.format(a))
					infofecha = cursor.fetchall()
					# time.sleep(3)
					json_data = {"chat_id": chat_id, "text": "|Cálculo   | Nr. Orden     | Gaveta  | Estado en el lab.| ",}
					message_url = BOT_URL + 'sendMessage'
					requests.post(message_url, json=json_data)
					# time.sleep(3)
					return None
				except (MySQLdb.Error, MySQLdb.Warning) as e:
					print(e)
					json_data = {"chat_id": chat_id, "text": "Error en la conexion con la base de datos, por favor intente mas tarde",}
					message_url = BOT_URL + 'sendMessage'
					requests.post(message_url, json=json_data)
					cursor.close()
					time.sleep(2)
					cursor = db.cursor()
					# execute SQL query using execute() method.
					cursor.execute("SELECT VERSION()")


					# Fetch a single row using fetchone() method.
					data2 = cursor.fetchone()
					print("Conecto a la base de datos externa:")
					print(data2)
					return None
				for row2 in infofecha:
					print("Calculo = ", row2[0], )
					print("Nr Orden = ", row2[1])
					print("Gaveta = ", row2[2])
					print("Estado  = ", row2[3], "\n")
					json_data = {"chat_id": chat_id, "text": "|   "+str(row2[0])+"    | "+str(row2[1])+" |  "+str(row2[2])+"  | "+str(row2[3])+"      |",}
					message_url = BOT_URL + 'sendMessage'
					requests.post(message_url, json=json_data)

            
            json_data = {"chat_id": chat_id, "text": "Regresa y selecciona otra fecha o escribe la palabra informe, para mirar de nuevo el listado de informe general.",}
            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data)
        
        
        
            else:
                json_data = {"chat_id": chat_id, "text": "Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
                message_url = BOT_URL + 'sendMessage'
                requests.post(message_url, json=json_data)
        
        

   
           
    
    
    return ''
    cursor.close()

if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
