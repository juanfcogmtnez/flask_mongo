from werkzeug.security import generate_password_hash, check_password_hash

def guardar(texto):
	hashed_password = generate_password_hash(texto)
	print (hashed_password)

def checkpwd(texto):
	
	print(check_password_hash('',texto))

checkpwd('Jfgm_4778')


