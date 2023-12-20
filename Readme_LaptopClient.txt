Function:
1. Displays the status of the DOOR (open/close) along with the timestamp.
2. Creates mqtt client that connects to AWS cloud port. ( Using certificates,key and  and endpoint details of AWS IOT core)
3. On connection success, Subscribes to the topic sensor/data
4. Every 10ms,code checks for any messages and if any message is received for sensor/data topic from AWS cloud via MQTT protocol, it displays as it is received.

How to RUN:
1. Make sure all the certificates and key files related to AWS cloud are in "certificates" folder and 
execute the python file using the command >> python laptop_client.py