import socket

gSocket = '' #to store the answering socket
handeler = {} #to store handelers ( key --> path requested, value --> [function to be exuted, its parameters])
resources = '' #to store the resources path

def analyze(req): #returns a tuple (the path requested,Http parameters)
    if len(req) < 5 : return (None,{})
    index = 5
    data = ""
    dataObj = {}
    key = ''
    path = ''
    #print(req)
    while True : 
        if req[index] == 63 :   #?
            if len(data) == 0 :
                path = '/'
            else :
                path = data
            data = ''
            index += 1
        elif req[index] == 61 : #=
            key = data
            data = ''
            index += 1
        elif req[index] == 38 : #&
            dataObj[key] = data
            data = ""
            index += 1
        elif req[index] == 32 : #space
            #print(" space found ")
            if len(data) == 0 and len(path) == 0 :
                #print("path is / ")
                path = "/"
            elif len(key) > 0 : dataObj[key] = data
            else : path = data
            break
        else : 
            data += chr(req[index])
            index += 1 
    print((path,dataObj))
    return (path,dataObj)

	
def handel(path,object,socket):
    global gSocket,resources
    gSocket = socket
    if path in handeler:
        parm = handeler[path][1]
        handeler[path][0](parm,object) #handeler is a dictionary where the key is the path and the value is a list the first item is the function and the second item is its parameters
        print("DONE")
    else :
		#print("resource file is : " + resources)
		try:
			file = open(resources+"res/"+path,"r")
			while True :
				d = file.read(1024)
				if len(d) == 0 : break
				socket.write(d)
			print("DONE")
		except :
			gSocket.write("404 file not found")
			print("ERROR")

def run_server() :
	addr = socket.getaddrinfo("0.0.0.0",8080)[0][-1]
	s = socket.socket()
	s.bind(addr)
	s.listen(3)
	#messege = "connect your browser to to "+str(ip)+":8080"
	#print(messege)
	#del messege
	while True:
		res = s.accept()
		client_s = res[0]
		client_addr = res[1]
		print("")
		print("client address: ",client_addr)
		req = client_s.recv(1024)
		client_s.write("HTTP/1.0 200 OK \r\n\r\n")
		print("req : " + str(req))
		path,object = analyze(req)
		handel(path,object,client_s)
		client_s.close()
		
def serve(name,object) :
	global resources
	#print("openning : " + resources+name)
	f = open(resources+name,"r")
	while True :
		d = f.read(4096)
		if len(d) == 0 : break
		gSocket.write(d)

def set_handeler(functions):
    for key in functions :
        handeler[key] = functions[key]

def set_resource_file(path):
	global resources
	resources = path+'/'