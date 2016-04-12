import sqlite3

class database():

	def __init__(self, name):
		self.connection = sqlite3.connect('/home/pi/brausteuerung/database/' + name, check_same_thread=False)
		self.cursor = self.connection.cursor()
	def sql_command(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()
	def sql_return(self):
		return self.cursor.fetchone()
	def __del__(self):
		self.connection.close()
