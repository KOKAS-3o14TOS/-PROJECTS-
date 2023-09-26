import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

flag = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("esp32/alarm1",0), ("esp32/alarm2",1),("esp32/alarm3",2),("esp32/alarm4",2)])

# The callback for when a PUBLISH message is received from the server.
# Possibilities for sequence break, where only traffic light stays on green until its respective button is unpushed.
def on_message(client, userdata, msg):
    global flag

    #First possible break of the sequence, where the first traffic light is green and the rest are red and stays until button is unpushed.
    #Executes if the button for the first traffic light is pushed.
    #Result is saved in a flag for later reference.
    #Connection via broker IP address.
    if msg.topic == "esp32/alarm1":
        print(str(msg.payload) + "/")
        if str(msg.payload) == "b'on'":
            print(flag)
            flag = True
            msgs = [("esp32/green1","on"),("esp32/green2","off"),("esp32/green3","off"),("esp32/green4","off")]
            publish.multiple(msgs,hostname="192.168.1.7",port=1883,keepalive=60)
        elif str(msg.payload) == "b'off'":
            flag = False

    #Second possible break of the sequence, where the second traffic light is green and the rest are red and stays until button is unpushed.
    #Executes if the button for the second traffic light is pushed.
    #Result is saved in a flag for later reference.
    #Connection via broker IP address.
    elif msg.topic == "esp32/alarm2":
        if str(msg.payload) == "b'on'":
            msgs = [("esp32/green1","off"),("esp32/green2","on"),("esp32/green3","off"),("esp32/green4","off")]
            publish.multiple(msgs,hostname="192.168.1.7",port=1883,keepalive=60)
            flag = True    
        elif str(msg.payload) == "b'off'":
            flag = False

    #Third possible break of the sequence, where the third traffic light is green and the rest are red and stays until button is unpushed.
    #Executes if the button for the third traffic light is pushed.
    #Result is saved in a flag for later reference.
    #Connection via broker IP address.
    elif msg.topic == "esp32/alarm3":
        if str(msg.payload) == "b'on'":
            msgs = [("esp32/green1","off"),("esp32/green2","off"),("esp32/green3","on"),("esp32/green4","off")]
            publish.multiple(msgs,hostname="192.168.1.7",port=1883,keepalive=60)
            flag = True    
        elif str(msg.payload) == "b'off'":
            flag = False

    #Fourth possible break of the sequence, where the fourth traffic light is green and the rest are red and stays until button is unpushed.
    #Executes if the button for the fourth traffic light is pushed.
    #Result is saved in a flag for later reference.
    #Connection via broker IP address.
    elif msg.topic == "esp32/alarm4":
        if str(msg.payload) == "b'on'":
            msgs = [("esp32/green1","off"),("esp32/green2","off"),("esp32/green3","off"),("esp32/green4","on")]
            publish.multiple(msgs,hostname="192.168.1.7",port=1883,keepalive=60)
            flag = True    
        elif str(msg.payload) == "b'off'":
            flag = False
    
    print(msg.topic+" "+str(msg.payload))


#Results for the client.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#Connection and re-connection to broker.
client.connect("192.168.1.7", 1883, 60)


# Normal sequence of traffic light, only one is green at a time, passes trough every traffic light and restarts infinitely.
client.loop_start()
num = 0
while True:
    #print(flag)
    while flag == False:
        msg = [("esp32/green1","on"),("esp32/green2","off"),("esp32/green3","off"),("esp32/green4","off")]
        publish.multiple(msg,hostname="192.168.1.7",port=1883,keepalive=60)
        time.sleep(1)

        if flag != False:
            break

        msg = [("esp32/green1","off"),("esp32/green2","on"),("esp32/green3","off"),("esp32/green4","off")]
        publish.multiple(msg,hostname="192.168.1.7",port=1883,keepalive=60)
        time.sleep(1)
        
        if flag != False:
            break

        msg = [("esp32/green1","off"),("esp32/green2","off"),("esp32/green3","on"),("esp32/green4","off")]
        publish.multiple(msg,hostname="192.168.1.7",port=1883,keepalive=60)
        time.sleep(1)
        
        if flag != False:
            break

        msg = [("esp32/green1","off"),("esp32/green2","off"),("esp32/green3","off"),("esp32/green4","on")]
        publish.multiple(msg,hostname="192.168.1.7",port=1883,keepalive=60)
        time.sleep(1)
        
        if flag != False:
            break
 
        

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.