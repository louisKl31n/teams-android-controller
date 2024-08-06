from csv import writer
import requests
from datetime import datetime
import time


if __name__ == '__main__' :
    web_server = "http://127.0.0.1:5000"
    device_name1 = 'RFCX218QHKX'
    email1 = 'user03.ITS@tpmorangefrpp.onmicrosoft.com'
    token1 = 0
    phoneNumberWebexBeta1 = '0789182612'

    while True:
        current_time = datetime.now().time()
        
        
        response = requests.post(web_server+'/connect', json={'deviceName': device_name1})
        token1 = response.json()['token']



        requests.post(web_server+'/log-in', json={
                'deviceName': device_name1,
                'email': email1,
                'token': token1,
        })
        
        time.sleep(20)
 