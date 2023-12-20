import AWSIoTPythonSDK.MQTTLib as mqtt
import time
from mpu6050 import mpu6050
from time import sleep
from libsvm.svmutil import *
from datetime import datetime

#Arrays to store 5 consecutive values of the gyroscope
ygyro_array = [0] * 10
i= 0
wait_time = 2
normalized_val = 60.0

IsDoorEventActive = False
EventTime = 0
current_state = ""
prev_state = ""

topic = "sensor/data"
sensor = mpu6050(0x68)
client = mqtt.AWSIoTMQTTClient("testDevice")
client.configureEndpoint("a31v2ldi3ernp8-ats.iot.us-east-1.amazonaws.com",8883)
client.configureCredentials("certificates/AmazonRootCA1.pem","certificates/dff8c9d56df375e08c1edc8396aa349b6ae9ee90264122a14c56d69ae842a158-private.pem.key","certificates/dff8c9d56df375e08c1edc8396aa349b6ae9ee90264122a14c56d69ae842a158-certificate.pem.crt")

client.connect()

svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
svm_problem = svm_problem([1, 1, 1, 1, 0, 0, 0, 0], [[0, 1, 2, 1, 0], [ 0, 0.5 , 1, 2, 1], [0, 1, 2, 1, 0], [ 0, 0.5 , 1, 2, 1], [0, -1, -2, -1,0],  [0, -.5,  -1, -2, -1], [0, -1, -2, -1,0],  [0, -.5,  -1, -2, -1]])

svm_param = svm_parameter()

svm_param.kernel_type = LINEAR
svm_param.C = 25

training_model = svm_train(svm_problem, svm_param)

while True:
    sleep(0.005)
    current_time = time.time()
    gyro_data = sensor.get_gyro_data()
    gyro_y = gyro_data['y']/normalized_val
   
    if(IsDoorEventActive and (current_time - EventTime) > wait_time):
        IsDoorEventActive = False
       
        predicted_state = training_model.predict(ygyro_array)
        if(predicted_state != prev_state):
            if(predicted_state == 1):
                current_time = datetime.now()
                payload = "Status- {}, Time Stamp- {}".format("Open", str(current_time))
                client.publish(topic,str(payload) , 0)
                print("The door is Open now")
           
            else:
                current_time = datetime.now()
                payload = "Status- {}, Time Stamp- {}".format("Closed", str(current_time))
                client.publish(topic,str(payload), 0)
                print("The door is closed now")
       
        prev_state = predicted_state
       
    elif(abs(gyro_y) > 1):
        ygyro_array[i] = gyro_y
        i = (i + 1) % len(ygyro_array)
        IsDoorEventActive = True
        EventTime = current_time
        
