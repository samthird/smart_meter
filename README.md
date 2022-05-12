# Smart energy meter using a PZEM-004T module, Raspberry Pi, Node Red and MQTT

CAUTION: This project involves working with MAINS AC POWER and IT CAN KILL YOU if you don't take the necessary precautions. 
I take no responsibility for any injury (or worse) to people who fail to do the necessary 
research before embarking on such a project, and it is beyond the scope of this repository to provide that here.

Note: I am based in the UK where we have single phase, 230v (216v - 253v) AC power. The live and neutral are effectively interchangeable. Other countries may differ (especially the USA) so do your research before blindly following this guide.

This project uses a PZEM-004T module to read AC voltage, current, power, energy etc, and sends the data over MQTT to a Node Red dashboard.

You can get a PZEM-004T on Amazon for about £25 (Make sure you get the version 3 as this includes the plastic case which protects the electronics). If you plan to monitor a large load (such as an entire house), get one with a 100A CT clamp. If you just want to monitor a single outlet or device, a 13A CT clamp would be sufficient.

You will also need a Raspberry Pi with the associated accessories (SD card + power supply)

This project is based on code from this repository: ```https://gist.github.com/bandaangosta/134c9d84ae9bd317297e96dcc0b9c860```

## Installation

ISOLATE THE MAINS SUPPLY BEFORE CONTINUING! I used a standard 13A 3 pin plug connected to a length of 1.5mm 3 core cable on one end and connected to the PZEM-004T at the other. Connect the Live and Neutral supply to the PZEM-004T. There is a diagram on the back of the case which shows the correct terminals.

Connect the CT clamp to the screw terminals (diagram also shows this)

Connect the UART-USB cable to the PZEM-004T and plug the USB into the Raspberry Pi.

Clamp the CT clamp around either the live or neutral. DO NOT clamp it around both or they will cancel each other out and you will read 0A.

## Clone this repository

```cd ~/```

```git clone https://github.com/samthird/smart_meter.git```

```cd smart_meter```

## Install packages

```pip install modbus-tk```

```pip install pyserial```

```pip install paho-mqtt```

## Install Node red and Mosquitto

```sudo apt update```

Install node red using this command:

```bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)```

(https://nodered.org/docs/getting-started/raspberrypi)

Start node red on boot:

```sudo systemctl enable nodered.service```

Start node red:

```sudo systemctl start nodered.service```

Install mosquitto broker:

```sudo apt install -y mosquitto mosquitto-clients```

Start mosquitto broker on boot:

```sudo systemctl enable mosquitto.service```

### Import the flow

You can either copy flows.json to the ```.node-red``` folder in the home directory, 

```cd ~/smart_meter/```

```cp flows.json ~/.node-red/```

or import the flow directly in the node red web interface

## Check the USB port

Run ```dmesg | grep tty``` to check which USB port the USB adapter is connected to. Change this in the python code if necessary.

## Set up the service to run the python script on boot

Note: The following assumes you have cloned this repository into the home directory of a user called ```pi```. If that is not the case then you will need to modify pzem004t.sh and pzem004t.service accordingly.

```sudo cp pzem004t.service /lib/systemd/system/```

Enable the service:

```sudo systemctl enable pzem004t.service```

Start the service:

```sudo systemctl start pzem004t.service```

Check if everything is working:

```sudo systemctl status pzem004t.service```
