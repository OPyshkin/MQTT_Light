import paho.mqtt.client as paho

class toggle:
    def __init__(self, lightstatus, movstatus, relay):
        self.lightstatus = lightstatus
        self.movstatus = movstatus
        self.relay = relay
    def getLight(self):
        return self.lightstatus
    def setLight(self, light):
        self.lightstatus = light

ctrl = toggle("_", "_", "_")
#print ctrl.getLight()

print ctrl.getLight()
def on_subscribe(client, userdata, mid, granted_qos):
    #print("Subscribed: "+str(mid)+" "+str(granted_qos))
    pass

def on_message(client, userdata, msg):
    data = msg.payload
    ctrl.setLight(data)
    if float(data)<680:
        client.subscribe("ctrl/movsens", qos = 0)
        client.message_callback_add("ctrl/movsens", on_message1)
    else:
        client.unsubscribe("ctrl/movsens")
        
        client.publish("ctrl/relay", "0" , qos=1,retain=False)
        
        
    print data
    

def on_message1(client, userdata, msg): #Sending logs to server
    if msg.payload == "1":
        print "toggle on" 
        client.publish("ctrl/relay", "1" , qos=1,retain=False)
    elif msg.payload == "0":
        print "toggle off"
        client.publish("ctrl/relay", "0" , qos=1,retain=False)
    
    
   




login = "slprpixn"
password = "hVyc0pHDpyUc"
URL = "m23.cloudmqtt.com"
PORT = 14740


client = paho.Client()
client.username_pw_set(login, password)
client.connect(URL, PORT)


client.on_subscribe = on_subscribe
client.subscribe("ctrl/lightsens", qos=1)
client.message_callback_add("ctrl/lightsens", on_message)
print "Program start"

client.loop_forever()
