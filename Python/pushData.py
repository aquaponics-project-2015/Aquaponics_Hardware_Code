import sys
import datetime
import time
import json
import requests
#Can be Downloaded from this Link
#https://pypi.python.org/pypi/pyserial
import serial
#Can be Downloaded from this Link
#http://docs.python-requests.org/en/latest/
baseURL = "http://54.152.138.146:9000"
ser = serial.Serial('COM3', 9600, timeout = 10) #You may have to change the port depending on your computer
time.sleep(2)

def main():
    while True:
        
        val = ser.readline()
        print val
        valuesArray = val.split(',')
        print valuesArray
        if int(valuesArray[0])==1 :
            water = float(valuesArray[1])
            ph = float(valuesArray[2])
            temp = float(valuesArray[3])
            postEnvToServer(temp,ph,water)
        if int(valuesArray[0])==2:
            state = valuesArray[1]
            if state =='On':
                postPumpToServer(True)
            else:
                postPumpToServer(False)
        
def getValue():
    val = ''
    this = True
    while this:
        byte = ser.read()
        if byte == '\r' or byte=='\n':
            this = False
        if (byte != '\r') and (byte != '\n'):
            val+=(byte)
    return val

def postEnvToServer(temp ,ph ,waterlevel):
    endpointURL = baseURL+"/system/newSystem"
    theTime = time.time() *1000
    print theTime
    payload = {"waterLevel":waterlevel,"ph":ph,"temperature":temp,"datetime":theTime}
    headers = {'Content-Type': 'application/json'}
    dump =json.dumps(payload)
    print dump
    r = requests.post(endpointURL,headers=headers, data = json.dumps(payload))
    print r.url 
    print r.status_code

def postPumpToServer(status):
    endpointURL = baseURL+"/pump/newPump"
    theTime = time.time() *1000
    payload = {"status":status, "datetime":theTime}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(endpointURL, headers=headers, data = json.dumps(payload))
    print r.url 
    print r.status_code
 
main()
