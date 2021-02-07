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

d = 0
i = 0
n = 0
h = 0
z = 0
Dg = 0
u = [0]*50
diff = [0]*50

R_on = True
R_off = True

print("USS1.8.py started")
Datum = time.strftime("%Y-%m-%d %H:%M:%S")
fobj_out = open(logfile,"a")
fobj_out.write('\n' + "Reboot " +  Datum + " USS1.8.py started" + '\n' + '\n')
fobj_out.close()
#subprocess.call("/home/pi/US-Sensor/Status_email.sh")


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    TRIG = 18
    ECHO = 24
    maxTime = 0.04

    while True:
        d = d + 1
        u = [0]*50
        for n in range (50):
            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.setup(ECHO,GPIO.IN)

            GPIO.output(TRIG,False)

            time.sleep(0.01)

            GPIO.output(TRIG,True)

            time.sleep(0.00001)

            GPIO.output(TRIG,False)

            pulse_start = time.time()
            timeout = pulse_start + maxTime
            while GPIO.input(ECHO) == 0 and pulse_start < timeout:
                pulse_start = time.time()

            pulse_end = time.time()
            timeout = pulse_end + maxTime
            while GPIO.input(ECHO) == 1 and pulse_end < timeout:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)
            u[n] = distance
            l = len(u)
            mw = sum(u)/50
            m= 0
            time.sleep(0.1)
            
        while l > m:      
            diff[m] = abs((mw-u[m])/mw)
            if (diff[m] > 0.1):
                del u[m]
                l = l-1

            m= m+1
            
              

                

        mw = sum(u)/len(u)
        #print("Mittelwert bereinigt", mw)
        #print("L:", l)
        cpu = CPUTemperature()
        cput = float(cpu.temperature)
       
        
#28-01143b9d88aa
        
        if z > 2:
            print("n=:", d)
            Datum = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu = CPUTemperature()
            fobj_out = open(logfile,"a")
            fobj_out.write(Datum + " n=: " + str(d) + " Mittelwert: " +  str(mw)+ "  CPU_temp: " + str(cpu.temperature) + " C " + '\n')
            fobj_out.close()
            #Ventilsteuerung:
            if mw > 10:        
                if R_on:
                    print("Ventil: OFF")
                    Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                    cpu = CPUTemperature()
                    fobj_out = open(filename,"a")
                    fobj_out.write(Datum + " n=: " + str(d) + ": Ventil OFF!!!  " + "Distanz: " + str(mw) + " CPU_temp: " + str(cpu.temperature) + "C"  + '\n')
                    fobj_out.close()
                    time.sleep(0.1)
                     
      
                    
                    R_on = False
                    R_off = True
                
                    
                    
            
               
            if mw < 10:
                if R_off:
                    print("Ventil_ON")
                    Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                    cpu = CPUTemperature()
                    fobj_out = open(filename,"a")
                    fobj_out.write(Datum + " n=: " + str(d) +  ": Ventil ON!!!  " + "Distanz: " +  str(mw) + "  CPU_temp: " + str(cpu.temperature) + "C"  + '\n')
                    fobj_out.close()
                    time.sleep(0.1)
                                       
                    
                    R_on = True
                    R_off = False
            
            z = 0
            Dg = 0
            Dm = 0
        else:
            z = z + 1


        


        

except KeyboardInterrupt:
    fobj_out = open("/home/pi/US-Sensor/logfile.txt","a")
    fobj_out.write(Datum + " keyboard.interrupt: " + " n: " + str(n) + " CPU_temp: " + str(cpu.temperature) + "C" +  '\n')
    fobj_out.close()
    print("process terminated")
  
    GPIO.cleanup()
    sys.exit()



