import socket
Quelle='192.168.178.39' # Adresse des eigenen Rechners
Port=8800

e_udp_sock = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM ) #s.o.
e_udp_sock.bind( (Quelle,Port) )
print '########Dies ist der Empfaenger########'
print 'Neue Verbindung:'
print 'Quelle',Quelle
print 'Port=',Port




def empfange():



    while 1:                                        # Endlosschleife
        data, addr = e_udp_sock.recvfrom( 1024 )
        print "empfangene Nachricht:", data
        print "Clientadresse:", addr          # Adresse besteht aus IP und Port


empfange()
