import string
import random
import subprocess
from controller import Controller
from appium.webdriver.appium_service import AppiumService
from flask import Flask, request,jsonify

app = Flask(__name__)
devices = {}
appium_servers ={
    'http://127.0.0.1:4724':'free',
    'http://127.0.0.1:4723':'free'
}


def authenticate_request(request):
    data = request.json
    device_name = data['deviceName']
    token = data['token']
    print(devices)
    for device in devices.values():
        print('device')
        print(device)
        print(device.appium_server_ip)
        print(device.driver)
    if devices[device_name].token == token :
        return devices[device_name]
    else :
        return False

def response(status_code,text) :
    resp = jsonify(text)
    resp.status_code = status_code
    return resp

@app.route('/connect', methods=['POST'])
def api_connect():
    device_name = request.json['deviceName']
    global devices
    global appium_servers
    already_in_use = False
    print(devices)
    for device in devices.values() :
        print(device.device_name)
        if device.device_name == device_name :
            already_in_use = True
    if already_in_use == False :
        new_device = Controller(device_name)
        new_device.token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        for appium_server_address, appium_server_status in appium_servers.items() :
            if(appium_server_status=='free'):
                new_device_appium_server_address = appium_server_address
        appium_servers[appium_server_address] = 'used'
        if new_device.teams_launch_app(new_device_appium_server_address):
            devices[device_name] = new_device
            print(devices)
            response = jsonify({
                'token': new_device.token
            })
            response.status_code = 200
    else :
        response = jsonify('Device : '+device_name+' is already in use')
        response.status_code = 401
    return response

@app.route('/log-in', methods=['POST'])
def api_log_in():
    device = authenticate_request(request)
    email = request.json['email']
    #password = request.json['password']
    if(device != False) :
        device.teams_log_in(email)
        response = jsonify('Log in worked as expected')
        response.status_code = 200
    else :
        response = jsonify('Authentication with deviceName and token failed')
        response.status_code = 401
    return response


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=5000)
    appium_service = AppiumService()
    appium_service.start(args=['-p 4723','--allow-insecure=Adb-shell'])
    appium_service.start(args=['-p 4724','--allow-insecure=Adb-shell'])
    subprocess.run(["adb","start-server"])
    subprocess.run(["./startAppiumServers"])

    
