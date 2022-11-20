#!/bin/sh
#recon.sh
sudo ifconfig wlan0 down
sleep 30
sudo ifconfig wlan0 up
echo "wifi reconnected" 
