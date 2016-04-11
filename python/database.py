import sqlite3

class database():

	def __init__(self, name):
		self.connection = sqlite3.connect('database/' + name)
		self.cursor = self.connection.cursor()
	def sql_command(self, sql):
		self.cursor.execute(sql)
		self.connection.commit()
	def sql_return(self):
		return self.cursor.fetchone()
	def __del__(self):
		self.connection.close()

class motorsteuerung(database):
	def __init__(self, engine):
		#Datenbank fuer die motorsteuerung
		self.engine_db = "engine.db"
		self.engine = engine
		self.db = database.__init__(self, self.engine_db)
		#Tables werden erstellt, falls sie noch nicht existiert:
		sql = "CREATE TABLE IF NOT EXISTS engines (id INTEGER PRIMARY KEY, name TEXT, position INTEGER)"
		database.sql_command(self, sql)
		#Der Motor wird eingetragen, falls er noch nicht existiert
		sql = "INSERT INTO engines (name,position) SELECT '%s', '%s' WHERE NOT EXISTS(SELECT 1 FROM engines WHERE name = '%s')" % (self.engine, 0, self.engine)
		database.sql_command(self, sql)
		#ID des Motors wird abgefragt
		sql = "SELECT id FROM engines WHERE name='%s'" % self.engine
		database.sql_command(self, sql)
		self.id = database.sql_return(self)[0]
	def get_engine_position(self):
		sql = "SELECT position FROM engines WHERE id='%s'" % self.id
		database.sql_command(self, sql)
		return database.sql_return(self)[0]
	#Ueberpruefen, ob der Motor schon eingetragen ist
	#p_type=0: Relative Aenderung der Position
	#p_type=1: Absolute Aenderung der Position
	def set_engine_position(self, position, p_type):
		#Relative Aenderung
		if p_type==0:
			old = self.get_engine_position()
			new = int(old) + int(position)
			sql = "UPDATE engines SET position='%s' WHERE id = '%s'" % (new, self.id)
			database.sql_command(self, sql)
		#Absolute Aenderung
		elif p_type==1:
			new = int(position)
			sql = "UPDATE engines SET position='%s' WHERE id = '%s'" % (new, self.id)
			database.sql_command(self, sql)
