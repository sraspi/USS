import time

def p(W):
    #Bibliotheken einbinden 
    import time
    import sys
    import subprocess
    import os
    ip = "www.google.de"

    try:
        WLAN = 0
        W = 0
        while W < 3 and WLAN == 0:
            time.sleep(1)
            print(W)
            
            if os.system("ping -c 1 " + ip) == 0:
                print("IP ist erreichbar")
                WLAN = 1
            else:
                subprocess.call("/home/pi/US-Sensor/recon.sh")
                print("wlan reconnected")
                WLAN = 0
                W = W + 1                

 
        if WLAN == 1:
            print("connected, go on!")
            
        else:
            print("not connected, wifi error, W:" + str(W))
          
        return W     
       
    except KeyboardInterrupt:
        print("process terminated")
        sys.exit()

W = (p(0))
print("W:", W)
try:
    timestr = time.strftime("%Y%m%d_%H%M%S")
    fobj_out = open("/home/pi/NAS/USS.log",  "a" )
    fobj_out.write("\n" + "\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "     t: "  + "USS5.0 started ,W:" + str(W) + '\n' )
    fobj_out.close()
except:
    timestr = time.strftime("%Y%m%d_%H%M%S")
    fobj_out = open("/home/pi/data/USS.log",  "a" )
    fobj_out.write("\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "     t: " + "W:" + str(W) + "network ERROR!!" + '\n' )
    fobj_out.close()