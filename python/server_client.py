import socket, json
import netifaces as ni
from threading import Thread
import time

class server(Thread):
    def __init__(self, global_obj):
        self.global_obj = global_obj
        self.socket = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
        self.ip = self.get_ip()
        print self.server_ip
        self.request_port = 8800
        self.socket.bind( (self.ip,self.request_port) )
        #self.socket.listen(10)
        Thread.__init__(self)
    def run(self):
        #Wenn Server:
        if self.global_obj.server_main == "1":
                t2 = Thread(target=self.listen_for_clients, args=('clienthere',))
                t2.start()
        #Wenn client:
        else:
            #Es wird gescannt
            t1 = Thread(target=self.scan_for_clients, args=(['clienthere', self.global_obj.server_name],))
            t1.start()
            #und auf antwort gewartet
            t2 = Thread(target=self.listen_for_clients, args=('serverhere'))
            t2.start()
    def get_ip(self):
        return ni.ifaddresses(self.global_obj.server_network)[2][0]['addr']
    def scan_for_clients(self, daten):
        ip = self.server_ip[:12]
        while True:
            #print ip
            for x in range(1,255):
                cur_ip = ip + str(x)
                try:
                    self.socket.sendto( json.dumps(daten), (cur_ip,self.request_port) )
                except:
                    print error
                    pass
    def listen_for_clients(self, message):
        while True:
            data, addr = self.socket.recvfrom(1024)
                                    # Die Puffergroese muss immer eine Potenz
                                    # von 2 sein
            print addr
            if json.loads(data)[0] == message:
                #Wenn Server:
                if self.global_obj.server_main == "1":
                    self.client_login(json.loads(data)[1], addr)
                #Wenn Client:
                else:
                    pass
    def client_login(self, daten, addr):
        try:
            self.socket.sendto( json.dumps(['serverhere', self.global_obj.server_name]), addr )
        except:
            print error
            pass
