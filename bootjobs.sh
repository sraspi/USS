#!/bin/sh
#bootjobs.sh
cd
cd /home/pi/noip-2.1.9-1
sudo noip2
cd
cd /home/pi/US-Sensor
sh filecopy.sh
rm logfile.txt
sh US-launcher.sh


