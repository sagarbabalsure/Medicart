import pymysql.cursors

def connection():
	db = pymysql.connect(
						host = 'localhost',
						user = 'root',
						password = 'sagar',
						db='MEDICAL',
						cursorclass=pymysql.cursors.DictCursor
						)
	cur = db.cursor()
	return cur,db