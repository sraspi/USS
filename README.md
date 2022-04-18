2021_12_13: USS 4GB-SD-Karte defekt, wiederholte Ausfaelle des Pi wegen Schreib/Lesefehlern.
- 32GB-Karte mit rpi-imager erstellt(inkl ssh und WLAN Fritzbox Keller)
- git installiert, ssh installiert und ueber git clone.... alles von USS aus github geclont
- erster Schritt war dann git add --all, git commit -am "text", git push --all
- noip installiert, crontab EintrÃ¤ge aus cron.uss uebernommen
- Ordner NAS und data erstellt
- pip3 istalliert
- smbus und smbus2 via pip3
- pip install RPi.bme280
- für Email: NICHT!!!(pip3 install numpy, pip3 uninstall numpy) sondern:sudo apt-get install python3-numpy
- NAS:sudo apt install samba cifs-utils
      mkdir ~/NAS
      /home/pi/NAS/                   nano ~/.smbcredentials
                                              username=sraspi
                                              password=StJ19raspbian
- etc/fstab ergänzen: 
  //192.168.178.1/FRITZ.NAS/ /home/pi/NAS cifs credentials=/home/pi/.smbcredentials,vers=3.0,noserverino,uid=1000,gid=1000,x-systemd.automount,x-systemd.requires=network-online.target 0 0
- crontab ergänzen:
- @reboot sleep 120 && mount -a

Power saving OFF:
sudo nano /etc/network/interfaces
allow-hotplug wlan0
iface wlan0 inet manual
post-up iw dev wlan0 set power_save off


- laeuft ab 13.12.2021
-USS nach Spannungsunterbrechung(wifi-Adapter Nano zu LC) neuer, kostenloser Ersatz-Pizero_W defekt, wifi(USS), erster Zero_W war doch nicht defekt(wifi).
18.04.22 neu aufgesetzt mit neuem Nano s.o.

