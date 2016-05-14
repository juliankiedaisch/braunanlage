from python import config_mgmt, server_client
#GLOBALS werden geladen
filename = "config.ini"
GLOBALS = type("globals", (object,), dict())()
config_mgmt.config_mgmt(filename, GLOBALS)

#Server-Socket wird geoeffnet
server_socket = server_client.server(GLOBALS)
server_socket.start()
