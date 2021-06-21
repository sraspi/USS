import time
import datetime
import sys
import subprocess


e = [0]*(100)      #Array von th0-th24
v = [0]*(100)      #Array 0-24 True/false
x = 0             #Stunden 0-24

filename = ("/home/pi/US-Sensor/Entfernung.txt")





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
            if data == t_mail:
                print("USS still running")
                #subprocess.call("/home/pi/US-Sensor/mail_OK.sh")
            else:
                Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                subprocess.call("/home/pi/US-Sensor/mail_error.sh")
                fobj_out = open(filename,"a")
                fobj_out.write("---------------------------------------------" + '\n' + Datum + " reboot follows....." + '\n')
                fobj_out.close()

                print("USS-error")
                subprocess.call("/home/pi/US-Sensor/reboot.sh")
   
try:
    print("app is running")
    c_r()

        
   
except KeyboardInterrupt:
    print("process terminated")
    sys.exit()


