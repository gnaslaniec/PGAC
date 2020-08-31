from flask import Flask, flash, render_template, request, send_file, redirect, url_for
from flask_qrcode import QRcode
# from serial import Serial
import time
import atexit

# ser = Serial('COM3', 9600)
time.sleep(2)
# print(ser.name)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jp8fSDuJBD9dklluvxk2cQ'    
qrcode = QRcode(app)

@app.route("/", methods = ['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/autenticacao', methods=['POST'] )
def turn_on():
    req_data = request.get_json()

    print(req_data)

    id_usuario = req_data['id_usuario']
    nome = req_data['nome']
    saldo = req_data['saldo']
    if saldo >= 4.50:
        # ser.write(b'H')
        print("Saldo suficiente!")
    else:
        # ser.write(b'L')
        print("Saldo insuficiente!")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=3000, use_reloader=False)