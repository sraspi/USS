#!/bin/sh
#bootjobs.sh
cd
cd /home/pi/noip-2.1.9-1
sudo noip2
cd
sleep 30
sudo mount -a
echo "NAS mounted"
cd /home/pi/US-Sensor/
sh filecopy.sh
rm logfile.txt
sh US-launcher.sh 


