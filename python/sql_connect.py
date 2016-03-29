class sql_connect():

	def __init__(self, name):
		self.connection = sqlite3.connect('database/' + name)
		self.cursor = self.connection.cursor()
	def get_beer_types(self):
		sql =

	def sql_command(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()
	def __del__(self)
		self.connection.close()
