# Tapping Test Software
For hardware build instructions, go to https://www.hackster.io/asun/tap-test-tt-41bdf2. Please note that the software is written for the PocketBeagle. Please go to https://beagleboard.org/pocket for more information. 

## Installation Instructions
### Cloning the Respository
Create a new directory for the program. To clone the repository: 
```
git clone https://github.com/AnSun03/ENGI301
git pull
```
### Installation
#### System Tools
General tools for python on the PocketBeagle. Skip if installed before. 
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-smbus -y
sudo apt-get install python-pip python3-pip -y
sudo apt-get install zip
```
#### Project Libraries 
```
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade Adafruit_BBIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-rgb-display
sudo apt-get install fonts-dejavu
sudo apt-get install python3-pil
pip3 install adafruit-circuitpython-tsc2007
```
### Automatic Boot
Setup for the program to run upon the PocketBeagle booting. In the command line: 
'''
sudo crontab -e
@reboot sleep 30 && bash /var/lib/cloud9/ENGI301/project_01/software/tap_test > /var/lib/cloud9/logs/chronlog 2>&1
'''

## Directories 
### tap_test - main program directory
configure_pins.sh - modify if pin connections are different 

run - check that filepaths are correct

tap_test.py - main program file 

### button - threaded button driver
Check that the default pin matches the hardware wiring or manually set the pin otherwise. Ensure that the button driver is set to the right configuration (active-low by default).

### buzzer - threaded buzzer driver
Ensure correct pin connections. 

### display - SPI display driver
Ensure correct pin connections. 

### timer - helper class for recording user inputs

### tsc2007 - touch screen controller driver
Ensure correct pin connections. Check that the size of the display matches the default (320 x 240). 

