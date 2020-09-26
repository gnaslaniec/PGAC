from flask import Flask, render_template, request, redirect, url_for
from flask_qrcode import QRcode
import psycopg2
from serial import Serial
from operacoes import Operacoes
import time
import yaml

# Arquivo com as configurações da aplicação
conf = yaml.load(open('conf/application.yml'))

# Comunicação serial com o Arduino/Catraca
#ser = Serial('COM3', 9600)
ser = Serial('/dev/ttyACM0', 9600)
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
    return render_template("index.html")

# API para autenticação e comunicação com a catraca
@app.route('/autenticacao', methods=['POST'] )
def autenticacao():
    req_data = request.get_json()
    id_usuario = req_data['id_usuario']
    #nome = req_data['nome']
    saldo = Operacoes.retorna_saldo_usuario(cursor,id_usuario)
    print(saldo)
    if saldo >= 450:
        ser.write(b'H')
        print("Saldo suficiente!")
        Operacoes.atualiza_saldo(connection,cursor,saldo,id_usuario)
        return '1'
    else:
        ser.write(b'L')
        print("Saldo insuficiente!")
        return '0'

if __name__ == "__main__":
    app.run(debug=True, port=3000, use_reloader=False)
