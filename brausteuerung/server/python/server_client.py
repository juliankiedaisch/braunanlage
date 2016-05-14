#Hier wird die Kommunikation zwischen Client und Server verwaltet

import socket, json
import netifaces as ni
from threading import Thread
import time
from python import database
from uuid import getnode as get_mac

class server(Thread):
    def __init__(self, global_obj):
        self.global_obj = global_obj
        self.socket = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
        self.ip = self.get_ip()
        print self.ip
        self.request_port = 8800
        self.socket.bind( (self.ip,self.request_port) )
        #self.socket.listen(10)
        self.db = database.database(self.get_ip(),global_obj.db_config_username, global_obj.db_config_pwd, global_obj.db_config_db)
        #Table fuer die Clients wird erstellt
        sql = "CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, ip Text, mac Text)"
        self.db.sql_command(sql)
        self.client_list = []
        Thread.__init__(self)
    def run(self):
        t2 = Thread(target=self.listen_for_clients, args=('clienthere',))
        t2.start()
    def get_ip(self):
        return ni.ifaddresses(self.global_obj.server_network)[2][0]['addr']
    def scan_for_clients(self, daten):
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
    def listen_for_clients(self, message):
        print "here"
        while True:
            data, addr = self.socket.recvfrom(1024)
                                    # Die Puffergroese muss immer eine Potenz
                                    # von 2 sein
            print addr
            #Ist es wirklich ein Client
            if json.loads(data)[0] == message:
                self.client_login(json.loads(data)[1], addr)

    def client_login(self, daten, addr):
        try:
            self.socket.sendto( json.dumps(['serverhere', self.global_obj.server_name]), addr )
        except:
            pass
        if daten[0] not in self.client_list:
            #Wird in die Clientlist geschrieben
            self.client_list.append(daten[0])
            print "%s (%s) hat sich am Server angemeldet" % (daten[1], addr[0])
            #Wird in die Datenbank geschrieben
            sql = "INSERT INTO clients SET name='%s', location='%s', mac='%s'" % (daten[1], addr[0], daten[0])
