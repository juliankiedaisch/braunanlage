from python import test_kochen, kochen, engine
import Queue

main_queue = Queue.Queue()

#Motor 1 GPIOs
gpios1 = [22,23,24,25]
#Motor 2 GPIOs
gpios2 = [17,18,11,10]
#GPIO Manager
gpiomanager = engine.gpio_manager()
engine_list = [0 for x in range(2)]
engine_list[0] = engine.engine(gpios1, "engine1", main_queue, gpiomanager)
engine_list[1] = engine.engine(gpios2, "engine2", main_queue, gpiomanager)

a = test_kochen.test_kochen(engine_list)
print a.sensor.temperatur
b = kochen.kochen(engine_list, [a.sensor], main_queue)
b.kalibrieren()
