from tornado import websocket, web, ioloop
import json
import time
import thread
from python import temp_sens, engine, rezept
cl = []

#Verknuepfen von Datavalue zu Datalist
class data_communication():
	def __init__(self):
	# Json Kommunikation
		self.test = "test"
	def data_input(self,name,value):
		data = {"message": [name, value]}
		for c in cl:
			c.write_message(json.dumps(data))


class IndexHandler(web.RequestHandler):
	def get(self):
		self.render("index.html")


class SocketHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		if self not in cl:
			cl.append(self)
			print self
			erste_daten()
	#Message from Client Handler
	def on_message(self, message):
		message = json.loads(message)
		key = message[0];
		if key == "rezept":
			communication_class.data_input("rezept_liste", rezept_class.make_rezept(message[1]))
	#Rezept wird zum bearbeiten angefragt
		elif key == "b_rezept":
			communication_class.data_input("b_rezept",rezept_class.get_rezept(message[1]))
	#Rezept wird geloescht
		elif key == "rezept_loeschen":
			communication_class.data_input("rezept_liste", rezept_class.delete_rezept(message[1]))
	#Biertyp soll bearbeitet werden
		elif key == "b_biertyp":
		#Was soll gemacht werden. Hinzufuegen=1, Loeschen=0
			a = message[1][0]
		#ID bei loeschen, name bei hinzufuegen
			b = message[1][1]
		#Loeschen
			if a==0:
				communication_class.data_input("b_biertyp",class_biertyp.delet_biertyp(b))
		#Hinzufuegen
			elif a==1:
				communication_class.data_input("b_biertyp",class_biertyp.add_biertyp(b))
		elif key == "engine":
		#ID des Schrittmotors
			a = message[1][0]
		#Einfach nur drehen oder Parameter anpassen
			b = message[1][1]
		#Anzahl der zu gehenden Schritte
			c = message[1][2]
		#Schritte relativ oder absolut (bei einfach drehen)
		#Max oder Min bei Einstellung der Parameter
			d = message[1][3]
		#Parameter KONFIGURIEREN
			if b==1:
				thread.start_new_thread(engine_list[a].set_engine_parameter, (c,d),)
		#Motor mit uebergebener Anzahl von Schritten drehen lassen
			elif b==0:
				thread.start_new_thread(engine_list[a].set_engine_position, (c,d),)
		#Voll an und abdrehen
			elif b==2:
				if c==1:
					thread.start_new_thread(engine_list[a].engine_on, (),)
				elif c==0:
					thread.start_new_thread(engine_list[a].engine_out, (),)

	def on_close(self):
		if self in cl:
			cl.remove(self)

class ApiHandler(web.RequestHandler):

	@web.asynchronous
	def get(self, *args):
		self.finish()
		id = self.get_argument("id")
		value = self.get_argument("value")
		data = {"id": id, "value" : value}
		data = json.dumps(data)
		for c in cl:
			c.write_message(data)

	@web.asynchronous
	def post(self):
		pass


def main_clock(dc):
	while True:
		dc.data_input("server_clock", time.strftime("%H:%M:%S"))
		time.sleep(1)

def erste_daten():
#Aktuelle Position des Schrittmotors 1 anzeigen
	communication_class.data_input("engine1", engine_list[0].current_position)
#Maximale Position des Schrittmotors 1 anzeigen
	communication_class.data_input("engine1_max", engine_list[0].max_position)
#Minimale Position des Schrittmotors 1 anzeigen
	communication_class.data_input("engine1_min", engine_list[0].min_position)
#Aktuelle Position des Schrittmotors 2 anzeigen
	communication_class.data_input("engine2", engine_list[1].current_position)
#Maximale Position des Schrittmotors 2 anzeigen
	communication_class.data_input("engine2_max", engine_list[1].max_position)
#Minimale Position des Schrittmotors 2 anzeigen
	communication_class.data_input("engine2_min", engine_list[1].min_position)

#Alle Biertypen werden abgerufen und an den Client geschickt
	communication_class.data_input("b_biertyp", [class_biertyp.show_all_biertypen()])
#Alle Rezepte werden in eine Liste geladen
	communication_class.data_input("rezept_liste", rezept_class.get_rezept_liste())


app = web.Application([
	(r'/', IndexHandler),
	(r'/ws', SocketHandler),
	(r'/api', ApiHandler),
	#(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
	(r'/(.*)', web.StaticFileHandler, {'path': './'}),
	#(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
	communication_class = data_communication()
#Klasse Biertyp wird initialisiert
	class_biertyp = rezept.biertyp("rezept.db")
#Klasse Rezept wird initialisiert
	rezept_class = rezept.rezept("rezept.db")
	app.listen(8888)
#Server Uhr
	thread.start_new_thread(main_clock, (communication_class,))
#Kommunikation mit Client
#thread.start_new_thread(communication_class.json_communication, (),)
#Temperatur auslesen
	up = temp_sens.sensor(communication_class,"temp_up","sensors.db")
	down = temp_sens.sensor(communication_class,"temp_down","sensors.db")
#Motor 1 GPIOs
	gpios1 = [22,23,24,25]
#Motor 2 GPIOs
	gpios2 = [18,17,21,4]
#GPIO Manager
	gpiomanager = engine.gpio_manager()
	engine_list = [0 for x in range(2)]
	engine_list[0] = engine.engine(gpios1, "engine1", communication_class, gpiomanager)
	engine_list[1] = engine.engine(gpios2, "engine2", communication_class, gpiomanager)
#Threads zum Temperaturauslesen werden gestartet
	thread.start_new_thread(up.get_temp, (),)
	thread.start_new_thread(down.get_temp, (),)
	ioloop.IOLoop.instance().start()
