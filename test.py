from python import engine

gpios1 = [22,23,24,25]
engine_list = [0 for x in range(2)]
engine_list[0] = engine.engine(gpios1, "engine1", communication_class)
