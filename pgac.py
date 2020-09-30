from flask import Flask, render_template, request, redirect, url_for
from flask_qrcode import QRcode
import psycopg2
from serial import Serial, SerialException
from operacoes import Operacoes
import time
import yaml
import os

# Arquivo com as configurações da aplicação
conf = yaml.load(open('conf/application.yml'))

# Comunicação serial com o Arduino/Catraca
try:
    ser = Serial('COM3', 9600)
except SerialException:
    try:
        ser = Serial('/dev/ttyACM0', 9600)
    except SerialException:
        ser = 0
time.sleep(2)

# Configurações do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = conf['app']['api_secret_key'],
qrcode = QRcode(app)

#Conexão com o Banco de dados
#connection, cursor = Operacoes.conexao_bd_local()
connection, cursor = Operacoes.conexao_bd_rds(conf)

# Define a página inicial da aplicação
@app.route("/", methods = ['POST','GET'])
def index():
    return render_template("index.html", qrcode_key=conf['qrcode']['qrcode_key'])

# API para autenticação e comunicação com a catraca
@app.route('/autenticacao', methods=['POST'] )
def autenticacao():
    req_data = request.get_json()
    id_usuario = req_data['id_usuario']
    saldo = Operacoes.retorna_saldo_usuario(cursor,id_usuario)
    print(saldo)
    if saldo >= 450:
        if ser != 0:
            ser.write(b'H')
        print("Saldo suficiente!")
        Operacoes.atualiza_saldo(connection,cursor,saldo,id_usuario)
        return '1'
    else:
        if ser != 0:
            ser.write(b'L')
        print("Saldo insuficiente!")
        return '0'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True, port=port, use_reloader=False)