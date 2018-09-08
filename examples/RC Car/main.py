from server import server
from const import gpio
from machine import Pin

d4 = Pin(gpio("D4"),Pin.OUT)
d4.on()

def print_speed(parm,http_object):                                  #TODO code for creating pwm to controll speed
    print(http_object['speed'])

def print_dir(parm,http_object):                                    #TODO code for controlling car direction
    if http_object['dir'] == 'stop' :
        d4.on()
    else:
        d4.off()
    print(http_object['dir'])

server.set_resource_folder('rcSite')
server.set_handeler({'/':[server.serve,'web.html']})
server.set_handeler({'speed':[print_speed,None]})
server.set_handeler({'dir':[print_dir,None]})
server.run_server()
