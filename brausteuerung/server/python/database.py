import MySQLdb as mdb

class database():

	def __init__(self, location,user, pwd, db):
		self.connection = mdb.connect(location, user, pwd, db)
		self.cursor = self.connection.cursor()
	def sql_command(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()
	def sql_return(self):
		return self.cursor.fetchone()
	def sql_return_all(self):
		return self.cursor.fetchall()
	def __del__(self):
		self.connection.close()
