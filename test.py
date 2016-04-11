from python import kochen, temp_sens, engine
import thread
#Verknuepfen von Datavalue zu Datalist
class data_communication():
	#Definition von Datalist:
	datavalue = ["server_clock", "temp_up", "temp_down", "power", "engine1", "engine1_max", "engine1_min"]
	datalist = [0 for x in range(len(datavalue))]
	def data_input(self,data,value):
		data_communication.datalist[data_communication.datavalue.index(data)] = value

communication_class = data_communication()
up = temp_sens.sensor(communication_class,"temp_up","500000071D4C0328")
down = temp_sens.sensor(communication_class,"temp_down","570000071CE8A828")
thread.start_new_thread(up.get_temp, (),)
thread.start_new_thread(down.get_temp, (),)

gpios1 = [22,23,24,25]
engine_list = [0 for x in range(1)]
engine_list[0] = engine.engine(gpios1, "engine1", communication_class)

k = kochen.kochen(engine_list, [up,down], communication_class)
k.kallibrieren()
