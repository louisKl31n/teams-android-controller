from csv import writer
import requests
from datetime import datetime
import time
from controller import Controller as contr


if __name__ == '__main__' :
    web_server = "http://127.0.0.1:5000"
    appium_server = "http://127.0.0.1:4723"
    device_name1 = 'RFCX218QHKX'
    email1 = 'user03.ITS@tpmorangefrpp.onmicrosoft.com'
    token1 = 0
    

    while True:
        current_time = datetime.now().time()
        response = requests.post(web_server+'/connect', json={'deviceName': device_name1})
        token1 = response.json()['token']

        #TeamsLaunching
        contr.connect_to_device("http://127.0.0.1:4723").start_activity('com.microsoft.teams','com.microsoft.skype.teams.Launcher')

        requests.post(web_server+'/log-in', json={
                'deviceName': device_name1,
                'email': email1,
                'password': '1Sac2billes!',
                'token': token1,
        })
        
        time.sleep(20)
 