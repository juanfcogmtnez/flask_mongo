from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import crea, envia
import json
import html.parser as htmlparser


app = Flask(__name__)
app.secret_key = 'esto-es-una-clave-muy-secreta'

@app.route("/")
def hello_world():
	consulta = crea.create_first()
	if consulta == "OK":
		return redirect(url_for('login'))
	else:
		return "la base de datos no se ha cargado correctamente"

@app.route("/login", methods=["POST", "GET"])
def login(message=None):
	if message == None:
		message = 'Por favor introduce tus datos'
	if request.method == 'POST':
		email = request.form['email']
		pwd = request.form['password']
		result = crea.checkpwd(email,pwd)
		if result != "":
			session['nombre'] = result[1]
			session['role'] = result[0]
			return redirect(url_for('hola'))
		else:
			message='Contraseña incorrecta'
	return render_template('login.html', message=message)

@app.route("/hola")
def hola():
	if 'nombre' in session and 'role' in session:
		role = session['role']
		nombre = session['nombre']
		return "Hola "+nombre+" eres "+role
	else:
		return redirect(url_for('login'))

@app.route('/datos-sesion',methods=['GET'])
def datos_sesion():
    if 'email' in session:
        email = session['email']
    else:
        email = ''

    return 'Datos Sesion: ' + email

@app.route("/forget", methods=["POST", "GET"])
def forget():
	message = "Indica tu email"
	if request.method == 'POST':
		diremail = request.form['email']
		direccion = request.url.encode("utf-8")
		direccion = str(direccion)
		direccion = direccion[9:]
		pos = direccion.find("/")
		direccion = direccion[0:pos]
		direccion = direccion.encode("utf-8")
		print(diremail)
		print(direccion)
		envio = envia.send(diremail,direccion)
		if envio != "":
			message = envio
	return render_template('forget.html',message=message)

@app.route("/repwd/<email>", methods=["POST", "GET"])
def repwd(email):
	script = ""
	message = 'Selecciona una contraseña'
	if request.method == 'POST':
		p1 = request.form['password1']
		p2 = request.form['password2']
		message = crea.uppwd(email,p1,p2)
		if message == "La contraseña se ha actualizado con éxito":
			script = "redirect()"
	return render_template('repwd.html',email=email,message=message,script=script)

@app.route("/register", methods=["POST", "GET"])
def register():
	message = ""
	script = ""
	if request.method == 'POST':
		nombre = request.form['nombre']
		email = request.form['email']
		role = 'user'
		p1 = request.form['password1']
		p2 = request.form['password2']
		message = crea.registro(nombre,email,role,p1,p2)
		if message == "Usuario creado, serás redirigido en cinco segundos":
			script = "redirect()"
			parser = htmlparser.HTMLParser()
			script = parser.unescape(script)
	return render_template('register.html',message=message,script=script)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
