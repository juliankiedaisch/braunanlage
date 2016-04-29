import Queue, time
from python import database

class log():

    def __init__(self, rezept_id):
        self.queue = Queue.Queue()
        self.db = database.database("rezept_log")
        self.id = rezept_id

        #Tabelle wird erstellt, falls nicht vorhanden
        sql = "CREATE TABLE IF NOT EXISTS rezept_log (koch_id INTEGER, rezept_id INTEGER, type INTEGER, info TEXT, zeit INTEGER)"
        self.db.sql_command(sql)

    def input(self, type, info)
