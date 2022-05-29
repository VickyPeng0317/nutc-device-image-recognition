def selectDevice(deviceId):
    deviceList = [
        {"deviceId": 1, "deviceName": "體溫量測設備", "deviceAddress": "資訊大樓-2501", "type": "體溫影像辨識"},
        {"deviceId": 2, "deviceName": "血壓機02", "deviceAddress": "學校大門入口處", "type": "血壓影像辨識"},
        {"deviceId": 3, "deviceName": "血壓機03", "deviceAddress": "資訊大樓2501研究室", "type": "體溫影像辨識"}
    ]
    return [device for device in deviceList if device.get('deviceId')==deviceId][0]