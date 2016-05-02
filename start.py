from tornado import websocket, web, ioloop
import json
import time
import thread
import Queue
from python import temp_sens, engine_test, rezept, kochen, test_kochen, log
cl = []

#Verknuepfen von Datavalue zu Datalist
class data_communication():
	def __init__(self, queue, cl_class):
	# Json Kommunikation
		self.queue = queue
		self.cl = cl_class
		self.data_input()
	def data_input(self):
		while True:
			cl_local = self.cl
			data = {"message": self.queue.get()}
			for c in cl_local:
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
			main_queue.put(["rezept_liste", rezept_class.make_rezept(message[1])])
	#Rezept wird zum bearbeiten angefragt
		elif key == "b_rezept":
			main_queue.put(["b_rezept",rezept_class.get_rezept(message[1])])
	#Rezept wird geloescht
		elif key == "rezept_loeschen":
			main_queue.put(["rezept_liste", rezept_class.delete_rezept(message[1])])
	#Biertyp soll bearbeitet werden
		elif key == "b_biertyp":
		#Was soll gemacht werden. Hinzufuegen=1, Loeschen=0
			a = message[1][0]
		#ID bei loeschen, name bei hinzufuegen
			b = message[1][1]
		#Loeschen
			if a==0:
				main_queue.put(["b_biertyp",class_biertyp.delet_biertyp(b)])
		#Hinzufuegen
			elif a==1:
				main_queue.put(["b_biertyp",class_biertyp.add_biertyp(b)])
		elif key == "kalibrieren":
			a = message[1]
			if a == 1:
				thread.start_new_thread(koch_object.kalibrieren, (),)

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
		pass

	@web.asynchronous
	def post(self):
		pass


def main_clock(dc):
	while True:
		dc.put(["server_clock", time.strftime("%H:%M:%S")])
		time.sleep(1)

def erste_daten():
#Aktuelle Position des Schrittmotors 1 anzeigen
	main_queue.put(["engine1", engine_list[0].current_position_prozent])
#Maximale Position des Schrittmotors 1 anzeigen
	main_queue.put(["engine1_max", engine_list[0].max_position])
#Minimale Position des Schrittmotors 1 anzeigen
	main_queue.put(["engine1_min", engine_list[0].min_position])
#Aktuelle Position des Schrittmotors 2 anzeigen
	main_queue.put(["engine2", engine_list[1].current_position_prozent])
#Maximale Position des Schrittmotors 2 anzeigen
	main_queue.put(["engine2_max", engine_list[1].max_position])
#Minimale Position des Schrittmotors 2 anzeigen
	main_queue.put(["engine2_min", engine_list[1].min_position])

#Alle Biertypen werden abgerufen und an den Client geschickt
	main_queue.put(["b_biertyp", [class_biertyp.show_all_biertypen()]])
#Alle Rezepte werden in eine Liste geladen
	main_queue.put(["rezept_liste", rezept_class.get_rezept_liste()])
#Alle Brauvorgaenge werden angezeigt
	main_queue.put(["log_liste_full"], log_class.log_liste_all()])

app = web.Application([
	(r'/', IndexHandler),
	(r'/ws', SocketHandler),
	(r'/api', ApiHandler),
	#(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
	(r'/(.*)', web.StaticFileHandler, {'path': './'}),
	#(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
	main_queue = Queue.Queue()
	thread.start_new_thread(data_communication, (main_queue, cl))
#Klasse Biertyp wird initialisiert
	class_biertyp = rezept.biertyp("kochen.db")
#Klasse Rezept wird initialisiert
	rezept_class = rezept.rezept("kochen.db")
	app.listen(8888)
#Server Uhr
	thread.start_new_thread(main_clock, (main_queue,))
#Kommunikation mit Client
#thread.start_new_thread(communication_class.json_communication, (),)
#Temperatur auslesen
	up = temp_sens.sensor(main_queue,"temp_up","sensors.db")
	down = temp_sens.sensor(main_queue,"temp_down","sensors.db")
#Motor 1 GPIOs
	gpios1 = [22,23,24,25]
#Motor 2 GPIOs
	gpios2 = [17,18,11,10]
#GPIO Manager
	gpiomanager = engine_test.gpio_manager()
	engine_list = [0 for x in range(2)]
	engine_list[0] = engine_test.engine(gpios1, "engine1", main_queue, gpiomanager)
	engine_list[1] = engine_test.engine(gpios2, "engine2", main_queue, gpiomanager)
#Testkochen Sensoren:
	test_kochen_object = test_kochen.test_kochen(engine_list)
#Kochen:
	koch_object = kochen.kochen(engine_list, [test_kochen_object.sensor], main_queue)
#Threads zum Temperaturauslesen werden gestartet
	thread.start_new_thread(up.get_temp, (),)
	thread.start_new_thread(down.get_temp, (),)
#Log wird gesetzt
	log_class = log.log("kochen.db")
	ioloop.IOLoop.instance().start()
