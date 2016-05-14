#Hier wird die Kommunikation zwischen Client und Server verwaltet

import socket, json
import netifaces as ni
from threading import Thread
import time, Queue
from uuid import getnode as get_mac
#Client
class client(Thread):
    def __init__(self, global_obj):
        self.global_obj = global_obj
        self.socket = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
        self.ip = self.get_ip()
        self.server_ip = None
        print self.ip
        self.request_port = 8800
        self.socket.bind( (self.ip,self.request_port) )
        #self.socket.listen(10)
        Thread.__init__(self)
    def run(self):
        #Es wird gescannt
        t1 = Thread(target=self.scan_for_server, args=(['clienthere', self.global_obj.client_name],))
        t1.start()
        #und auf antwort gewartet
        t2 = Thread(target=self.listen_for_server, args=(str('serverhere'),))
        t2.start()
        #warten bis Verbindung zum server etabliert wurde
        #while server_ip = None
    def get_ip(self):
        return ni.ifaddresses(self.global_obj.server_network)[2][0]['addr']
    def scan_for_server(self, daten):
        ip = self.ip[:12]
        while True:
            #print ip
            for x in range(1,255):
                cur_ip = ip + str(x)
                try:
                    self.socket.sendto( json.dumps(daten), (cur_ip,self.request_port) )
                except:
                    print error
                    pass
    def listen_for_server(self, message):
        while True:
            data, addr = self.socket.recvfrom(1024)
                                    # Die Puffergroese muss immer eine Potenz
                                    # von 2 sein
            print addr
            if json.loads(data)[0] == message:
                self.server_ip = addr[0]
