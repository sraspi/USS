def ps(pingstatus):
    import subprocess
    import os
    import time
    Datum = time.strftime("%Y-%m-%d %H:%M:%S")
    pingstatus = ""


    for i in range(10):
        
        hostname = "www.google.com"
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            pingstatus = "Network Active"
            
        else:
            pingstatus = "Network Error"
            subprocess.call("/home/pi/US-Sensor/recon.sh")
            Datum = time.strftime("%Y-%m-%d %H:%M:%S")
            h = open("/home/pi/US-Sensor/wifi.log","a")
            h.write(Datum + "  wifi-status: " + pingstatus + '\n')
            h.close()
           
            time.sleep(10)
        return pingstatus
      



