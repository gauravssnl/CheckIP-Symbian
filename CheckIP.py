import socket
import urllib
import sys
import appuifw
import e32
import globalui
import os
import Console

ru = lambda text : text.decode("utf-8" , "ignore")
ur =  lambda text : text.encode("utf-8" , "ignore")
timer = e32.Ao_timer()
lock = e32.Ao_lock()

def quit():
    os.abort()

def slow_print(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        timer.after(3.0/180)
    timer.cancel()    

def app():
    console = Console.Console(True)
    appuifw.app.title = ru("CheckIP")
    appuifw.app.exit_key_handler = quit
    global body
    body = appuifw.app.body = console.text
    body.color = (255,0,0)
    body.font = "title",22
    slow_print("CheckIP by gauravssnl\n")
    body.font = "title",17
    body.color = (255,0,255)
    slow_print("Features :\n")
    body.color = (0,0,255)
    slow_print("---Check Local IP\n")
    slow_print("---Check Internet IP\n")
    appuifw.app.menu = [(ru("Check Internet IP"), internetIP ) , (ru("Check Local IP") , localIP) ,(ru("About") ,about),(ru("Exit"),quit)]
    

def internetIP():
    appuifw.app.menu = []
    host = "http://checkip.amazonaws.com/"
    try :
        data = urllib.urlopen(host).read()
        body.color = (0,255,0)
        slow_print("Your Internet IP :\n")
        body.color = (0,0,255)
        slow_print(data)
    except:
        body.color = (255,255,0)
        slow_print("Internet Connection Failed\n")
    appuifw.app.menu = [(ru("Check Internet IP"), internetIP ) , (ru("Check Local IP") , localIP) ,(ru("About") ,about),(ru("Exit"),quit)]    
        

def localIP():
    appuifw.app.menu = [ ]
    try :
        id_list = [ap["iapid"] for ap in socket.access_points()]
        name_list = [ap["name"] for ap in socket.access_points()]
        apnid = socket.select_access_point()
        apn = socket.access_point(apnid)
        apn.start()
        ip = apn.ip()
        body.color = (0,255,0)
        slow_print("Your Local IP :\n")
        body.color = (0,0,255)
        slow_print(ip )
        slow_print(" \n")
    except:
        body.color = (255,255,0)
        slow_print("No Access Point Selected\n")
    appuifw.app.menu = [(ru("Check Internet IP"), internetIP ) , (ru("Check Local IP") , localIP) ,(ru("About") ,about),(ru("Exit"),quit)]    

def about():
    e32.ao_sleep(0.01)
    globalui.global_msg_query(ru("Developer: gauravssnl") , ru("CheckIP"))
                



app()
lock.wait()            