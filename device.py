import json
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import random
from random import uniform

connflag = False

#print(ssl.OPENSSL_VERSION)

def on_connect(client,userdata,flags,rc):
    global connflag
    connflag =True
    print("Connection required result:"+str(rc))

def on_message(client,userdata,msg):
	print(msg.topic+" "+str(msg.payload))
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
latitude = 12.9716
longitude = 77.5946
awshost = "ailnju7bxk3mm-ats.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "geocode"
thingName="geocode"
caPath = "AmazonRootCA1.pem"
certPath = "f3fc725581-certificate.pem.crt"
keyPath = "f3fc725581-private.pem.key"
mqttc.tls_set(caPath,certfile=certPath,keyfile=keyPath,cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
mqttc.connect(awshost,awsport,keepalive=60)
mqttc.loop_start()
while 1==1:
    sleep(5)
    if connflag == True:
      new_lat = latitude+random.random()/100
      new_lon = longitude+random.random()/100
      payload = json.dumps({'latitude':new_lat,'longitude':new_lon})
      mqttc.publish("iot", payload, qos=0)
      print("msg sent: " + "%s"%payload )
    else:
        print("waiting for connection...")
