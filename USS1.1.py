#Bibliotheken einbinden 
import RPi.GPIO as GPIO 
import time
import sys
import signal
from gpiozero import CPUTemperature
import subprocess
import os

#Kernelmodule laden
#os.system('modprobe w1-gpio')                   
#os.system('modprobe w1-therm')

# Import the ADS1115 module.
# Create an ADS1115 ADC (16-bit) instance.
from ADS1x15 import ADS1115
adc = ADS1115()

# Note you can change the I2C address from its default (0x48)
# bus by passing in these optional parameters:
adc = ADS1115(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.096V.
channel = 0
GAIN = 1

    
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)  
    
#GPIO Pins zuweisen
# GPIO14     > Lüfter
# GPIO4(ge)  > 1wire
# GPIO22(bl) > Relais(3) geschaltete 12V Lampe direkt und Relais(2) für 5V-Lüfter
# GPIO17(sw) > Relais(1) für Pumpe

GPIO.setup(11, GPIO.OUT)
#H-Brücke in1

GPIO.setup(13, GPIO.OUT)
#H-Brücke in2

GPIO.setup(14, GPIO.OUT)
#GPIO.setup(17, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT)


GPIO_TRIGGER = 18   
GPIO_ECHO = 24  
    
#Richtung der GPIO-Pins festlegen (IN / OUT)    
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  
GPIO.setup(GPIO_ECHO, GPIO.IN)



#Variablen auf default setzen, konfigiurieren
filename = ("/home/pi/US-Sensor/Entfernung.txt")
logfile = ("/home/pi/US-Sensor/logfile.txt")

i = 0
n = 0
h = 0
z = 0
Dg = 0

R_on = True
R_off = True

print("USS1.1.py started")
Datum = time.strftime("%Y-%m-%d %H:%M:%S")
fobj_out = open(logfile,"a")
fobj_out.write('\n' + "Reboot " +  Datum + "USS1.1.py started" + '\n' + '\n')
fobj_out.close()
subprocess.call("/home/pi/US-Sensor/Status_email.sh")

class TimeoutException(Exception):

    pass

def _timeout(signum, frame):

    raise TimeoutException()

signal.signal(signal.SIGALRM, _timeout)

# Send the SIGALRM signal in 30 seconds:

try:
    while True:
        #Lüftersteuerung cpu:
        #ip = "www.google.de"
        #if os.system("ping -c 1 " + ip) == 0:
           # print("IP ist erreichbar")
        #else:
           #fobj_out = open(logfile,"a")
           #fobj_out.write('\n' + "wifi-OFF!! " + '\n' + '\n')
           #fobj_out.close()

        cpu = CPUTemperature()
        cput = float(cpu.temperature)
        if cput < 38:
            print("CPU-Lüfter OFF")
            GPIO.output(14, GPIO.LOW) #Lüfter#
        else:
            
            if cput > 40:
                print("CPU-Lüfter ON")
                GPIO.output(14, GPIO.HIGH)



        #US-signal read:
        value = [0]*2
        for i in range(2):
            
            signal.alarm(30)
            n = n + 1
            #setze Trigger auf HIGH    
            GPIO.output(GPIO_TRIGGER, True) 
            # setze Trigger nach 0.01ms aus LOW 
            time.sleep(0.00001) 
            GPIO.output(GPIO_TRIGGER, False)    
    
            StartZeit = time.time() 
            StopZeit = time.time()  
    
            # speichere Startzeit
            while GPIO.input(GPIO_ECHO) == 0:
                StartZeit = time.time()
            
            # speichere Ankunftszeit    
            while GPIO.input(GPIO_ECHO) == 1:
                StopZeit = time.time()  
    
            # Zeit Differenz zwischen Start und Ankunft 
            TimeElapsed = StopZeit - StartZeit  
            # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren 
            # und durch 2 teilen, da hin und zurueck    
            distanz = (TimeElapsed * 34300) / 2
            
            abstand = distanz
            value[i] = abstand
            i = i + 1
            time.sleep(0.0077504)
            

        mw = (value[0] + value[1])/2
       
        
#28-01143b9d88aa
        
        print(mw)
        D = [0]*(z+1)
        D[z] = mw
        Dg = Dg + D[z]
        Dm = Dg/(z+1)
        print("Dm. ", Dm)
        print("Dg: ", Dg)
        print("n: ", n)
        print("z: ",z)
        print("-------------")
        
        if z > 75:
            
            Datum = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu = CPUTemperature()
            fobj_out = open(logfile,"a")
            fobj_out.write(Datum + " n=: " + str(n) + " Mittelwert: " +  str(Dm)+ "  CPU_temp: " + str(cpu.temperature) + " C " + '\n')
            fobj_out.close()
            time.sleep(0.1)
            z = 0
            Dg = 0
            Dm = 0
        else:
            z = z + 1


        


        #Ventilsteuerung:
        if mw > 10:        
            if R_on:
                print("Ventil: OFF")
                Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                cpu = CPUTemperature()
                fobj_out = open(filename,"a")
                fobj_out.write(Datum + " n=: " + str(n) + ": Relais OFF!!!  " + "Distanz: " + str(mw) + " CPU_temp: " + str(cpu.temperature) + "C"  + '\n')
                fobj_out.close()
                time.sleep(0.1)
                 
  
                
                R_on = False
                R_off = True
            
                
                
        
           
        if mw < 10:
            if R_off:
                print("R_OFF")
                Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                cpu = CPUTemperature()
                fobj_out = open(filename,"a")
                fobj_out.write(Datum + " n=: " + str(n) +  ": Relais ON!!!  " + "Distanz: " +  str(mw) + "  CPU_temp: " + str(cpu.temperature) + "C"  + '\n')
                fobj_out.close()
                time.sleep(0.1)
                                   
                
                R_on = True
                R_off = False
                
                
                
                
except TimeoutException:  
    Datum = time.strftime("%Y-%m-%d %H:%M:%S")
    cpu = CPUTemperature()
    fobj_out = open("/home/pi/US-Sensor/logfile.txt","a")
    fobj_out.write('\n' + Datum + " timeout at: " + " n: " + str(n) + " CPU_temp: " + str(cpu.temperature) + "C" + '\n')
    fobj_out.close()
    print("time out at: ", str(n))
    GPIO.cleanup()
    time.sleep(10)
    subprocess.call("/home/pi/US-Sensor/timeout.sh")
    subprocess.call("/home/pi/US-Sensor/reboot.sh")
    sys.exit()

except KeyboardInterrupt:
    fobj_out = open("/home/pi/US-Sensor/logfile.txt","a")
    fobj_out.write(Datum + " keyboard.interrupt: " + " n: " + str(n) + " CPU_temp: " + str(cpu.temperature) + "C" +  '\n')
    fobj_out.close()
    print("process terminated")
  
    GPIO.cleanup()
    sys.exit()
