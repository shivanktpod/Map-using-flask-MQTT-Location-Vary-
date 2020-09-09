from flask import Flask,render_template
from flask_mqtt import Mqtt

import ssl
import urllib.request as request
app=Flask(__name__)

app.config['MQTT_BROKER_URL']='ailnju7bxk3mm-ats.iot.us-east-1.amazonaws.com'
#app.config['MQTT_BROKER_URL']='https://p4tp0s31gh.execute-api.ap-south-1.amazonaws.com'
app.config['MQTT_BROKER_PORT']=8883
app.config['MQTT_CLIENT_ID']="geocodes"
app.config['MQTT_KEEPALIVE']=60
app.config['MQTT_TLS_ENABLED']=True
app.config['MQTT_TLS_CA_CERTS']="AmazonRootCA1.pem"
app.config['MQTT_TLS_CERTFILE']="aece684b8e-certificate.pem.crt"
app.config['MQTT_TLS_KEYFILE']="aece684b8e-private.pem.key"
app.config['MQTT_TLS_CIPHERS']=None
app.config['MQTT_TLS_CERT_REQS']=ssl.CERT_REQUIRED
app.config['MQTT_TLS_VERSION']=ssl.PROTOCOL_TLSv1_2

mqtt=Mqtt(app)
lat=12.9716
lng=77.5946
api_key='Y7dIJIrCFqMCrLzxlJ1HnEsa76TDkQvG619MzrRxspc'
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

#api_key= 'waD6G64LINl7ieNoERaJ'
#@mqtt.on_log()
#def handle_logging(client, userdata, level, buf):
#   if level == MQTT_LOG_ERR:
#        print('Error: {}'.format(buf))
@mqtt.on_connect()
def handle_connect(client,userdata,flags,rc):
	mqtt.subscribe('iot')
#	if rc==0:
#		print("connected OK Returned code=",rc)
#	else:
#		print("Bad connection Returned code=",rc)
#	print('Connected and waiting for msgs')
mqtt.publish('home/mytopic', 'hello world')
@mqtt.on_message()
def handle_mqtt_messages(client,userdata,msg):
#	print("Msg "+msg)
	global lat,lng
	data=eval(msg.payload.decode())
	lat=data['latitude']
	lng=data['longitude']
	print("received from aws  Lat="+str(lat)+" Long"+str(lng))
print("MQTT Setup done "+"initial value -Lat="+str(lat)+" long="+str(lng))
#Flask code 
#app = Flask(__name__)
@app.route('/')
def map_func():
    print("before render template apikey="+api_key)
    return render_template('map.html',apikey=api_key,latitude=lat, longitude=lng) #map.html is my HTML file name
   # return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

if __name__ == '__main__':
    app.run(debug = False)

# @app.route('/')
# def index():
# 	return render_template('home.html')
# @app.route('/getlatlng')
# def getlatlng_page():
# 	global lat,lng
# 	print("called ajax:",str(lat)+','+str(lng))
# 	return str(lat)+','+str(lng)
# if __name__=='__main__':
# 	app.run(use_reloader=False,debug=True)