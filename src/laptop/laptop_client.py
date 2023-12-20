import time
import paho.mqtt.client as mqtt
import ssl

Connected = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
  
        print("Connected to broker")
        Connected = True 
        client.subscribe("sensor/data")
  
    else:
  
        print("Connection failed")

def on_message(client, userdata, message):
    print(message.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message= on_message 
  
client.tls_set(ca_certs="certificates/AmazonRootCA1.pem", certfile="certificates/dff8c9d56df375e08c1edc8396aa349b6ae9ee90264122a14c56d69ae842a158-certificate.pem.crt", keyfile="certificates/dff8c9d56df375e08c1edc8396aa349b6ae9ee90264122a14c56d69ae842a158-private.pem.key", tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a31v2ldi3ernp8-ats.iot.us-east-1.amazonaws.com", 8883, 60)
  
  
client.loop_start()
 
while Connected != True:
    time.sleep(0.2)
  
while True:
        time.sleep(0.01)
