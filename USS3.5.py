 #Bibliotheken einbinden 
import smbus
import smbus2
import bme280
import threading
import subprocess
from queue import Queue
import RPi.GPIO as GPIO
import time
import sys
import os
from gpiozero import CPUTemperature


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
GPIO.setwarnings(False)

import smbus2
import bme280

temperature,pressure,humidity = bme280.readBME280All()


#GPIO Pins zuweisen

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)
GPIO.setup(27, GPIO.OUT)


    

TRIG = 18
ECHO = 24
maxTime = 0.04

GPIO_TRIGGER = 18   
GPIO_ECHO = 24  
    
#Richtung der GPIO-Pins festlegen (IN / OUT)    
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  
GPIO.setup(GPIO_ECHO, GPIO.IN)



#Variablen auf default setzen, konfigiurieren
filename = ("/home/pi/US-Sensor/Entfernung.txt")
logfile = ("/home/pi/US-Sensor/logfile.txt")

d = 0              # Anzahl der US-Messungen
i = 0
n = 0
h = 0
k = 0.              #Zähler für t_mail
z = 0
Dg = 0
Tg = 0
Pg = 0
Hg = 0
diff = [0]*10
L = 0
E = 2               #Bedingung für Ventil ON erfüllt
D = [0]*(999)       #Array von D0-D999
VT_diff = 0


R_on = True
R_off = True
mail = True

print("USS3.5.py started")
print()
Datum = time.strftime("%Y-%m-%d %H:%M:%S")

fobj_out = open(logfile,"a")
fobj_out.write('\n' + "Reboot " +  Datum + " USS3.5.py started" + '\n' + '\n')
fobj_out.close()

print("Ventil ON")
GPIO.output(22, GPIO.HIGH)
cpu = CPUTemperature()
fobj_out = open(filename,"a")
fobj_out.write(Datum + " started " + " n=: " + str(d) + ": Ventil ON!!!  "  + " CPU_temp: " + str(round(cpu.temperature,1)) + "C"  + '\n' + '\n')
fobj_out.close()
time.sleep(5)
subprocess.call("/home/pi/US-Sensor/mail_on.sh")
Vt_start = time.time()
tm_start = time.time()

try:
    
    while True:

        #Lueftersteuerung cpu:
        GPIO.output(27, GPIO.HIGH) #Luefter

        u = [0]*10
        for n in range (10):
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
            mw = sum(u)/10
            m= 0
            
            time.sleep(1)
            
            d = d + 1
            
        while l > m:                   #Check Mittelwertabweichung >10% > Wert eliminieren, am Ende neue Mittelwertbildung
            diff[m] = abs((mw-u[m])/mw)
            if (diff[m] > 0.1):
                del u[m]
                l = l-1
            m= m+1


        mw = sum(u)/len(u)
        print()
        print()
        print("l: ", l)
        if l  < 5:
            print()
            print()
            print("l: ", l)
           
            fobj_out = open(filename,"a")
            fobj_out.write('\n' + Datum + " n=: " + str(d) + ": l > 5!!!  " + '\n' + '\n')
            fobj_out.close()
            subprocess.call("/home/pi/US-Sensor/Statusmail.sh") 
            print()
            print()

        cpu = CPUTemperature()
        cput = float(cpu.temperature)
        temperature,pressure,humidity = bme280.readBME280All()


        T = [0]*(z+1)
        P = [0]*(z+1)
        H = [0]*(z+1)

        D[z] = mw
        T[z] = temperature
        P[z] = pressure
        H[z] = humidity

        Dg = Dg + D[z]
        Tg = Tg + T[z]
        Pg = Pg + P[z]
        Hg = Hg + H[z]



        Dm = Dg/(z+1)
        Tm = Tg/(z+1) + 0.3
        Pm = Pg/(z+1) + 21
        Hm = Hg/(z+1) - 3

        print(("D: "), round(D[z], 1))
        print("T:", round((temperature + 0.3), 2))
        print("P:", round((pressure + 21), 2))
        print("H", round((humidity - 3), 2))
        print(("z: "),  z)

        if z > 116: # bereinigter Mittelwert aus 10*50 US-Messungen wird gespeichert
            print()
            print()
            print("----------------------------------------- n: ", d, "Mittelwert: ", round(Dm, 1))
            Vt_end = time.time()
            Vt_diff = (Vt_end - Vt_start)
            E = D[116]-D[0]
            F = (0.0000000001+E)/Vt_diff*10*60
            print("F:", F, " mm/min")

            if F < 1 and mail:
                  print("Email IBC leer!")
                  Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                  fobj_out = open(filename,"a")
                  fobj_out.write('\n' + Datum + " n=: " + str(d) + ": IBC leer!!!  " + '\n' + '\n')
                  fobj_out.close()                
                  subprocess.call("/home/pi/US-Sensor/mail_ibc.sh")
                  print()
                  print()
                  mail = False
                  print("Ventil OFF")
                  GPIO.output(22, GPIO.LOW)
                  Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                  cpu = CPUTemperature()
                  fobj_out = open(filename,"a")
                  fobj_out.write(Datum + " n=: " + str(d) +  ": Ventil OFF!!!  " + "Distanz: " +  str(round(mw,1)) + "  CPU_temp: " + str(cpu.temperature) + "C"  + '\n')
                  fobj_out.close()
                  subprocess.call("/home/pi/US-Sensor/mail_off.sh")

                 
                  

            if R_on and Dm > 10 and mail: #wenn Dm > 10cm und R_on (also vorher auf OFF) dann Ventil ON
                print("Ventil ON")
                GPIO.output(22, GPIO.HIGH)
                Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                cpu = CPUTemperature()
                fobj_out = open(filename,"a")
                fobj_out.write(Datum + " n=: " + str(d) + ": Ventil ON!!!  " + "Distanz: " + str(round(mw,1)) + " CPU_temp: " + str(round(cpu.temperature, 1)) + "C"  + '\n')
                fobj_out.close()
                subprocess.call("/home/pi/US-Sensor/mail_on.sh")
                R_on = False
                R_off = True
              
                   

            elif R_off and Dm < 8 and mail:  #wenn DM < 8cm und R_off (also vorher auf ON) dann Ventil OFF
                print("Ventil OFF")
                GPIO.output(22, GPIO.LOW)
                Datum = time.strftime("%Y-%m-%d %H:%M:%S")
                cpu = CPUTemperature()
                fobj_out = open(filename,"a")
                fobj_out.write(Datum + " n=: " + str(d) +  ": Ventil OFF!!!  " + "Distanz: " +  str(round(mw,1)) + "  CPU_temp: " + str(round(cpu.temperature, 1)) + "C"  + '\n')
                fobj_out.close()
                subprocess.call("/home/pi/US-Sensor/mail_off.sh")
                R_on = True
                R_off = False

            Datum = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu = CPUTemperature()
            fobj_out = open(logfile,"a")
            fobj_out.write(Datum + " n=: " + str(d) + " Mittelwert: " +  str(round(Dm, 1))+ "  CPU_temp: " + str(round(cpu.temperature, 1)) + " C " + " T: " + str(round(Tm, 2)) + " P: " + str(round(Pm, 1)) + " Hm: " + str(round(Hm,1)) + '\n')
            fobj_out.close()
            #subprocess.call("/home/pi/US-Sensor/mail_write.sh")
            #subprocess.call("/home/pi/US-Sensor/mail_on.sh")
            
            z = 0
            Dg = 0
            Tg = 0
            Pg = 0
            Hg = 0
            Dm = 0
            Tm = 0
            Pm = 0
            Vt_start = time.time()


        else:
            z = z + 1
        tm_end = time.time()
        t_mail = tm_start + 3600    

        if tm_end > t_mail:
            subprocess.call("/home/pi/US-Sensor/USmail.sh")
            tm_start = t_mail
       

except KeyboardInterrupt:
    fobj_out = open("/home/pi/US-Sensor/logfile.txt","a")
    fobj_out.write(Datum + " keyboard.interrupt: " + " n: " + str(n) + " CPU_temp: " + str(cpu.temperature) + "C" + " Mw: " + str(mw) + '\n')
    fobj_out.close()
    print("process terminated")
    GPIO.cleanup()
    sys.exit()

