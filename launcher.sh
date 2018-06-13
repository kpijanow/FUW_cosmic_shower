#!/bin/sh
# launcher.sh

cd /
cd /home/pi/Desktop/FUW_cosmic_shower/
sleep 10
sudo shutdown -r 1:00
sudo python3 main.py &>> logDesktop.txt
