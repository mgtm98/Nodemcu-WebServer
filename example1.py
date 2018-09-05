import socket
import server

server.set_resource_folder("web")

server.set_handeler({"/" : [server.serve,"main.html"]})
server.set_handeler({"test" : [server.serve."test.html"]})

server.run_server()
