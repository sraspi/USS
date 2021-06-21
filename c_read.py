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
            f = open("/home/pi/US-Sensor/check.txt", "r")
            data = f.read()
            data = int(data)
            f.close()
            print(data)
            
            v[x] = False
            #print("data: ",data," x: ",x, " t_mail: ", t_mail)
            if data == t_mail:
                print("USS still running")
                subprocess.call("/home/pi/US-Sensor/mail_OK.sh")
            else:
                subprocess.call("/home/pi/US-Sensor/mail_error.sh")
                print("USS-error")
                #subprocess.call("/home/pi/US-Sensor/reboot.sh")
   
try:
    while True:
        print("app is running")
        c_r()
        time.sleep(10)
        
   
except KeyboardInterrupt:
    print("process terminated")
    sys.exit()


