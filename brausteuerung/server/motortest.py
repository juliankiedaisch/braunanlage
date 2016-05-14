from python import engine


class dcc():

	def data_input(self, name, value):
		print name + ":" + str(value)
 
dc = dcc()
position = [22,23,24,25]
test = engine.engine(position, dc)
test.cool_down(512)
