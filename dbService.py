def selectDevice(deviceId):
    deviceList = [
        {"deviceId": 1, "deviceName": "血壓機01", "deviceAddress": "資訊大樓1F電梯口"},
        {"deviceId": 2, "deviceName": "血壓機02", "deviceAddress": "學校大門入口處"},
        {"deviceId": 3, "deviceName": "血壓機03", "deviceAddress": "資訊大樓2501研究室"}
    ]
    return [device for device in deviceList if device.get('deviceId')==deviceId][0]