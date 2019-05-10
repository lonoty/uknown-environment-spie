from rplidar import RPLidar
listo=False
while (listo !=True):
    try:
        lidar = RPLidar('/dev/ttyUSB0')
        info = lidar.get_info()
        print(info)
        health = lidar.get_health()
        print(health)
        listo=True
    except:
        continue

data=[]
i=0

for scan in lidar.iter_scans(500):
    data=scan

    i=i+1
    if i==1:
        break
    
data.sort(key=lambda tup: tup[1])   
print(data)
print(len(data))
print(data[0])

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
