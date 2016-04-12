import sqlite3

class database():

	def __init__(self, name):
		self.connection = sqlite3.connect('database/' + name, check_same_thread=False)
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
