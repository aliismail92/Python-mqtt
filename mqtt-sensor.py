import paho.mqtt.client as mqttClient
import time

data = []
humidity = -1
msg_received = False
led = -1
 
def on_connect(client, userdata, flags, rc):
    
    
    if rc == 0:
 
        print("Connected to broker with code", rc)
 
        client.connected_flag = True                #Signal connection 


    else:
 
        print("Connection failed with code", rc)
 
def on_message(client, userdata, message):
    print ("Message received: ", message.payload)
    global msg_received
    global humidity
    global led
    
    msg_received = True
    humidity =float(str(message.payload, 'utf-8'))
    
    if str(message.topic, 'utf-8') =="But/led":
        led = int(str(message.payload, 'utf-8'))
   
    data.append(humidity)
    
 
 
broker_address= "192.168.0.107"  #Broker address
port = 1883                         #Broker port
user = "mqtt1"                    #Connection username
password = "mqtt1"            #Connection password

mqttClient.Client.connected_flag=False 
client = mqttClient.Client("Python")#, protocol=mqttClient.MQTTv31)               #create new instance
client.username_pw_set(username="mqtt1",password="mqtt1")    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
count  = 0
while not client.connected_flag:    #Wait for connection
    time.sleep(1)
    print ("waiting for connection", count)
    count +=1
    
topics = [("sens/hum",2), ("But/led",2)]
client.subscribe(topics)
#client.subscribe("But/led", 2)
#i = 0 
#while i < 50:
try:
    while True:
        time.sleep(1)
        if msg_received == True:
            
            if led == 1:
                print ("led ", 1)
            elif led == 0:
                print ("led", 0)
                
            if humidity > 50 and humidity <75:
                print ("humidity medium")
                
            elif humidity > 75:
                print ("Humidity High")
            elif humidity < 50 and humidity>1:
                print("Humidity low")
            msg_received = False
            print(humidity)
       # i += 1
        

except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()