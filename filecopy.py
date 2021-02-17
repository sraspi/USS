import time
from shutil import copyfile
Datum = time.strftime("%Y_%m_%d")
dateiname = ("/home/pi/data/" + Datum + ".txt")
copyfile("/home/pi/US-Sensor/logfile.txt", dateiname)
