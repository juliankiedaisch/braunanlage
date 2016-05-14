from python import motor, sensor, client_server, config_mgmt

#GLOBALS werden geladen
filename = "config.ini"
GLOBALS = type("globals", (object,), dict())()
config_mgmt.config_mgmt(filename, GLOBALS)

#Client-Socket wird geoeffnet
client_socket = client_server.client(GLOBALS)
client_socket.start()
