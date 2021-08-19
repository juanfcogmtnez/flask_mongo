import pymongo
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

myclient = pymongo.MongoClient('mongodb://mongo:27017/')

db = myclient.list_database_names()

def create_first():

	if 'users' in db:
		return "OK"

	else:
		pass_texto_plano = "Jfgm_4778"
		pass_hasheada = generate_password_hash(pass_texto_plano)
		mydb = myclient["users"]
		mycol = mydb["user"]
		x = mycol.insert_one({"nombre":"juan","email":"jfgarcia@simalga.com","pwd":pass_hasheada,"role":"admin"})
		return "OK"

def checkpwd(email,texto):
	mydb = myclient["users"]
	mycol = mydb["user"]
	myquery = {"email":email}
	mydoc = mycol.find(myquery)
	for x in mydoc:
		print (x)
	pass_hasheada = x['pwd']
	role = x['role']
	nombre = x['nombre']
	print(texto)
	if check_password_hash(pass_hasheada,texto):
		return(role,nombre)
	else:
		return("Error")
	return (role,nombre)

def uppwd(email,p1,p2):
	if p1 != p2:
		return "Las contraseñas no coinciden"
	else:
		db = myclient.users
		collection = db.user
		filter = { 'email': email }
		newpass = generate_password_hash(p1)
		newvalues = { "$set": { 'pwd': newpass } }
		collection.update_one(filter, newvalues)
		return "La contraseña se ha actualizado con éxito"

def registro(nombre,email,role,p1,p2):
	if p1 != p2:
		return "Las contraseñas no coinciden"
	else:
		newpass = generate_password_hash(p1)
		db = myclient.users
		collection = db.user
		filter = { 'email': email }
		mydoc = collection.find(filter)
		lista = []
		for x in mydoc:
			lista.append(x)
		if lista != []:
			return "Un usuario con ese email ya existe"
		newrecord = {"nombre":nombre,"email":email,"role":role,"pwd":newpass}
		rec = collection.insert_one(newrecord)
		return "Usuario creado, serás redirigido en cinco segundos" 	
