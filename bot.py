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


def conectionDB():
  data = request.json
  chat_id = data['message']['chat']['id']
  message = data['message']['text']
  # Open database connection
  db = MySQLdb.connect("ryclab.com","ryclabco","ryclab*+2015","ryclabco_wp557" )
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
  cursor.execute("SELECT VERSION();")
  # Fetch a single row using fetchone() method.
  data2 = cursor.fetchone()
  print("Conecto a la base de datos externa:")
  print(data2)
  cursor.execute("SET lc_time_names = 'es_ES';")
  cursor.execute("set session sql_mode='TRADITIONAL';")
  sql = "select count(date(fecha_calculado)),DAYNAME(date(fecha_calculado)),date(fecha_calculado),DATEDIFF(date(now()),date(fecha_calculado)),(5 * (DATEDIFF(date(curdate()), date(fecha_calculado)) DIV 7) + MID('0123444401233334012222340111123400012345001234550', 7 * WEEKDAY(date(fecha_calculado)) + WEEKDAY(date(curdate())) + 1, 1)) AS DiasAtraso from trabajos_lab WHERE Estado != 'Enviado' AND date(fecha_calculado)>DATE_SUB(NOW(),INTERVAL 15 DAY) GROUP BY date(fecha_calculado) ORDER BY  DiasAtraso DESC;"
  cursor.execute(sql)
  dataselect = cursor.fetchall()
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
  cursor.close()
  
  
def fechaconsultaDB(a):
  data = request.json
  chat_id = data['message']['chat']['id']
  message = data['message']['text']
  # Open database connection
  db = MySQLdb.connect("ryclab.com","ryclabco","ryclab*+2015","ryclabco_wp557" )
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
  cursor.execute("SELECT VERSION();")
  # Fetch a single row using fetchone() method.
  data2 = cursor.fetchone()
  print("Conecto a la base de datos externa:")
  print(data2)
  cursor.execute("SET lc_time_names = 'es_ES';")
  cursor.execute("set session sql_mode='TRADITIONAL';")
  sqlinfofecha ="select NumCalculo, NumOrden, Gaveta, Estado FROM trabajos_lab where fecha_calculado like {0} AND (Estado != 'Enviado' OR 'Cancelado') AND date(fecha_calculado)>DATE_SUB(NOW(),INTERVAL 15 DAY)" 
  cursor.execute(sqlinfofecha.format(a))
  infofecha = cursor.fetchall()
  # time.sleep(3)
  json_data = {"chat_id": chat_id, "text": "|Cálculo   | Nr. Orden     | Gaveta  | Estado en el lab.| ",}
  message_url = BOT_URL + 'sendMessage'
  requests.post(message_url, json=json_data)
  # time.sleep(3)
  for row2 in infofecha:
      print("Calculo = ", row2[0], )
      print("Nr Orden = ", row2[1])
      print("Gaveta = ", row2[2])
      print("Estado  = ", row2[3], "\n")
      json_data = {"chat_id": chat_id, "text": "|   "+str(row2[0])+"    | "+str(row2[1])+" |  "+str(row2[2])+"  | "+str(row2[3])+"      |",}
      message_url = BOT_URL + 'sendMessage'
      requests.post(message_url, json=json_data)
  cursor.close()
  
  
def OrdenconsultaDB(orden):
  data = request.json
  chat_id = data['message']['chat']['id']
  message = data['message']['text']
  # Open database connection
  db = MySQLdb.connect("ryclab.com","ryclabco","ryclab*+2015","ryclabco_wp557" )
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
  cursor.execute("SELECT VERSION();")
  # Fetch a single row using fetchone() method.
  data2 = cursor.fetchone()
  print("Conecto a la base de datos externa:")
  print(data2)
  cursor.execute("SET lc_time_names = 'es_ES';")
  cursor.execute("set session sql_mode='TRADITIONAL';")
  sqlorden ="select NumCalculo, NumOrden, Gaveta, Estado, Cliente, Disenio FROM trabajos_lab where NumOrden like CONCAT({0},'%') AND date(fecha_calculado)>DATE_SUB(NOW(),INTERVAL 15 DAY)" 
  cursor.execute(sqlorden.format(orden))
  infofecha = cursor.fetchall()
  # time.sleep(3)
  json_data = {"chat_id": chat_id, "text": "|Cálculo   | Nr. Orden     | Gaveta  | Estado en el lab.| Cliente | Diseño | ",}
  message_url = BOT_URL + 'sendMessage'
  requests.post(message_url, json=json_data)
  # time.sleep(3)
  for row2 in infofecha:
      print("Calculo = ", row2[0], )
      print("Nr Orden = ", row2[1])
      print("Gaveta = ", row2[2])
      print("Gaveta = ", row2[3])
      print("Gaveta = ", row2[4])
      print("Estado  = ", row2[5], "\n")
      json_data = {"chat_id": chat_id, "text": "|   "+str(row2[0])+"    | "+str(row2[1])+" |  "+str(row2[2])+"  | "+str(row2[3])+"      | "+str(row2[4])+"      | "+str(row2[5])+"      |",}
      message_url = BOT_URL + 'sendMessage'
      requests.post(message_url, json=json_data)
  cursor.close()
  
def Danios():
  data = request.json
  chat_id = data['message']['chat']['id']
  message = data['message']['text']
  # Open database connection
  db = MySQLdb.connect("ryclab.com","ryclabco","ryclab*+2015","ryclabco_wp557" )
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
  cursor.execute("SELECT VERSION();")
  # Fetch a single row using fetchone() method.
  data2 = cursor.fetchone()
  print("Conecto a la base de datos externa:")
  print(data2)
  cursor.execute("SET lc_time_names = 'es_ES';")
  cursor.execute("set session sql_mode='TRADITIONAL';")
  sql = "SELECT COUNT(fecha) AS Cantidad,Fecha FROM Danios WHERE date(Fecha)>DATE_SUB(NOW(),INTERVAL 30 DAY) GROUP BY date(fecha) ORDER BY fecha DESC;"
  cursor.execute(sql)
  dataselect = cursor.fetchall()
  json_data = {"chat_id": chat_id, "text": "|#Daños  | Fecha   |: ",}
  message_url = BOT_URL + 'sendMessage'
  requests.post(message_url, json=json_data)
  # time.sleep(3)
  for row in dataselect:
      print("Cantidad de Daños = ", row[0], )
      print("Fecha = ", row[1], "\n")
      json_data = {"chat_id": chat_id, "text": "|   "+str(row[0])+"     |  /"+"Daños--"+str(row[1].strftime("%Y_%m_%d"))+"    |",}
      message_url = BOT_URL + 'sendMessage'
      requests.post(message_url, json=json_data)
  #time.sleep(3)
  cursor.close()

  
def fechadanioconsultaDB(a):
  data = request.json
  chat_id = data['message']['chat']['id']
  message = data['message']['text']
  # Open database connection
  db = MySQLdb.connect("ryclab.com","ryclabco","ryclab*+2015","ryclabco_wp557" )
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
  cursor.execute("SELECT VERSION();")
  # Fetch a single row using fetchone() method.
  data2 = cursor.fetchone()
  print("Conecto a la base de datos externa:")
  print(data2)
  cursor.execute("SET lc_time_names = 'es_ES';")
  cursor.execute("set session sql_mode='TRADITIONAL';")
  sqlinfofecha ="select Calculo, Descripcion FROM Danios where fecha like CONCAT({0},'%')" 
  cursor.execute(sqlinfofecha.format(a))
  infofecha = cursor.fetchall()
  # time.sleep(3)
  json_data = {"chat_id": chat_id, "text": "|Cálculo   | Daño     |",}
  message_url = BOT_URL + 'sendMessage'
  requests.post(message_url, json=json_data)
  # time.sleep(3)
  for row2 in infofecha:
      print("Calculo = ", row2[0], )
      print("Nr Orden = ", row2[1], "\n")
      json_data = {"chat_id": chat_id, "text": "|   "+str(row2[0])+"    | "+str(row2[1])+"   |",}
      message_url = BOT_URL + 'sendMessage'
      requests.post(message_url, json=json_data)
  cursor.close()
  
  
  
@app.route('/', methods=['POST'])
def main():
    data = request.json
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    print(data)  # Comment to hide what Telegram is sending you


    if message == "Informe" or message == "informe":
        print("Entro al if")
        json_data = {"chat_id": chat_id, "text": "En el laboratorio RYC se encuentran trabajos de: ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        conectionDB()
       
        json_data = {"chat_id": chat_id, "text": "Los días de atraso no tienen en cuenta ni Sábados ni Domingos, Ahora selecciona la fecha de realizado el cálculo, para obtener información de los trabajos de esa fecha.",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)        
            
            
        
        
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
        fechaconsultaDB(a)
                    
        json_data = {"chat_id": chat_id, "text": "Regresa y selecciona otra fecha o escribe la palabra informe, para mirar de nuevo el listado de informe general.",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        
         
    elif message == "Consultar Orden":
        json_data = {"chat_id": chat_id, "text": "Para consultar el estado de una Orden, Por favor escriba la palabra: \"Orden\" y a continuación el número de Orden a consultar",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        
    elif message.startswith( 'Orden ' ):
        orden=str(message[5:])
        print("Información sobre la orden número: ", orden)
        json_data = {"chat_id": chat_id, "text": "A continuación se muestran la información relacionada al número de Orden"+orden+": ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        OrdenconsultaDB(orden)

    elif message == "Daños" or message == "daños":
        print("Entro al if")
        json_data = {"chat_id": chat_id, "text": "En el laboratorio RYC se Registran los siguientes daños: ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        Danios()
       
        json_data = {"chat_id": chat_id, "text": "Los daños mostrados son los registrados en un periodo de 30 Días calendario.",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)  

    elif message.startswith( '/Daños--' ):
        feeecha= message.split('-',2)[2]
        fechaconsulta = datetime.strptime(feeecha,"%Y_%m_%d").date()
        print("Va a consultar los daños registrados con fecha de:", fechaconsulta)
        json_data = {"chat_id": chat_id, "text": "A continuación se muestran los Daños presentes en el laboratorio de la fecha "+feeecha+": ",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        a="'"+fechaconsulta.strftime("/%Y-%m-%d")[1:]+"%'"
        fechadanioconsultaDB(a)
                    
        json_data = {"chat_id": chat_id, "text": "Regresa y selecciona otra fecha o escribe la palabra Danios, para mirar de nuevo el listado de Daños.",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)        
        
        
    else:
        json_data = {"chat_id": chat_id, "text": "Por favor escriba la palabra: Informe, para dar el informe de trabajos presentes en el laboratorio",}
        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        

   
           
    
    
    return ''
    #cursor.close()

if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
