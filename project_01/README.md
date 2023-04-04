# Tapping Test Software
For hardware build instructions, go to https://www.hackster.io/asun/tap-test-tt-41bdf2. Please note that the software is written for the PocketBeagle. Please go to https://beagleboard.org/pocket for more information. 

## Installation Instructions
### Cloning the Respository
Create a new directory for the program. To clone the repository: 
```
git clone https://github.com/AnSun03/ENGI301/tree/main/project_01/software
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

