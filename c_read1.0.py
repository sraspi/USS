import time
import datetime
import sys
import subprocess


e = [0]*(100)      #Array von th0-th24
v = [0]*(100)      #Array 0-24 True/false
x = 0             #Stunden 0-24




for x in range(0, 24):
    e[x] = x
    v[x]= True
    
def c_r():
    x = 0
    th = datetime.datetime.now()  
    t_mail = th.hour  
        
    for x in range (0, 24):
        if t_mail  ==  e[x] and v[x]:
            time.sleep(2)
            f = open("/home/pi/US-Sensor/check.txt", "r")
            data = f.read()
            data = [int(i) for i in data]
            data = sum(data)
            f.close()
            v[x] = False
            print(data, x)
            if data == (x):
                print("USS still running")
                subprocess.call("/home/pi/US-Sensor/mail_OK.sh")
            else:
                subprocess.call("/home/pi/US-Sensor/mail_error.sh")
                print("USS-error")
   
try:
    print("app started")
    while True:
        c_r()
   
except KeyboardInterrupt:
    print("process terminated")
    sys.exit()


