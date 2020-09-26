from flask import Flask, flash, render_template, request, redirect, url_for
from flask_qrcode import QRcode
from flask_mysqldb import MySQL
import mysql.connector
from serial import Serial
from operacoes import Operacoes
import time

# Comunicação serial com o Arduino/Catraca
ser = Serial('COM3', 9600)
time.sleep(2)
# Configurações do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jp8fSDuJBD9dklluvxk2cQ'
qrcode = QRcode(app)
MySQL(app)
#Conexão com o Banco de dados
db = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="root",
   database='pgac',
   auth_plugin='mysql_native_password'
)
cursor = db.cursor(buffered=True)

# Define a página inicial da aplicação
@app.route("/", methods = ['POST','GET'])
def index():
    return render_template("index.html")
# API para autenticação e comunicação com a catraca
@app.route('/autenticacao', methods=['POST'] )
def autenticacao():
    req_data = request.get_json()
    id_usuario = req_data['id_usuario']
    nome = req_data['nome']
    saldo = Operacoes.retorna_saldo_usuario(cursor,id_usuario)
    if saldo >= 4.50:
        ser.write(b'H')
        print("Saldo suficiente!")
        Operacoes.atualiza_saldo(db,cursor,saldo,id_usuario)
        return '1'
    else:
        ser.write(b'L')
        print("Saldo insuficiente!")
        return '0'
    

if __name__ == "__main__":
    app.run(debug=True, port=3000, use_reloader=False)