import socket
Quelle='192.168.178.39' # Adresse des eigenen Rechners
Port=8888

e_udp_sock = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM ) #s.o.
e_udp_sock.bind( (Quelle,Port) )    #Im IP-Adresse und Port werden
                    # durch bind miteinander verknuepft.
print '########Dies ist der Empfaenger########'
print 'Neue Verbindung:'
print 'Quelle',Quelle
print 'Port=',Port




def empfange():
    while 1:                                        # Endlosschleife
        data, addr = e_udp_sock.recvfrom( 1024 )# Puffer-Groese ist 1024 Bytes.
                            # Die Puffergroese muss immer eine Potenz
                            # von 2 sein
        if data == "brautest":
            print "Client sucht Server:", addr[0]         # Adresse besteht aus IP und Port
            e_udp_sock.sendto( "abcdefg123", addr )

empfange() #Programm wartet in einer Endlosschleife auf eingehende Nachrichten, Herkunftsort ist egal.
