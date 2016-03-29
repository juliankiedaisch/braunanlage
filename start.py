from tornado import websocket, web, ioloop
import json
import time
import thread
from python import temp_sens, engine
cl = []

#Verknuepfen von Datavalue zu Datalist
class data_communication():
	#Definition von Datalist:
	datavalue = ["server_clock", "temp_up", "temp_down", "power", "engine1"]
	datalist = [0 for x in range(len(datavalue))]

	# Json Kommunikation
	def json_communication(self):
		data = {}
		while True:
			for x in range(0,len(data_communication.datavalue)):
				data[data_communication.datavalue[x]] = data_communication.datalist[x]
			for c in cl:
				c.write_message(json.dumps(data))
			time.sleep(1)

	def data_input(self,data,value):
		data_communication.datalist[data_communication.datavalue.index(data)] = value

class IndexHandler(web.RequestHandler):
	def get(self):
		self.render("index.html")


class SocketHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		if self not in cl:
			cl.append(self)
	#Message from Client Handler
	def on_message(self, message):
		key = message[0];
		if key == "beertyps":
			print message[1];
		elif key == "engine":
			a = message[1][0]
			b = message[1][1]
			c = message[1][2]
			if b == 1:
				engine_list[a].warm_up(c)
			else:
				engine_list[a].cool_down(c)

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

app = web.Application([
	(r'/', IndexHandler),
	(r'/ws', SocketHandler),
	(r'/api', ApiHandler),
	(r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
	(r'/(.*)', web.StaticFileHandler, {'path': './'}),
	(r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
	communication_class = data_communication()
	app.listen(8888)
	#Server Uhr
	thread.start_new_thread(main_clock, (communication_class,))
	#Kommunikation mit Client
	thread.start_new_thread(communication_class.json_communication, (),)
	#Temperatur auslesen
	up = temp_sens.sensor(communication_class,"temp_up","500000071D4C0328")
	down = temp_sens.sensor(communication_class,"temp_down","570000071CE8A828")
	#Motor 1
	position = [22,23,24,25]
	engine_list[0] = engine.engine(position, communication_class)
	communication_class.data_input("engine1", engine_list[0].get_engine_position)
	thread.start_new_thread(up.get_temp, (),)
	thread.start_new_thread(down.get_temp, (),)
	ioloop.IOLoop.instance().start()
