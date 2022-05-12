import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import paho.mqtt.client as mqtt
import json
import time

client_name = "smart_meter"

client =mqtt.Client(client_name)

client.connect("localhost", port=1883)

try:
    # Connect to the sensor
    sensor = serial.Serial(
                           port='/dev/ttyUSB0',
                           baudrate=9600,
                           bytesize=8,
                           parity='N',
                           stopbits=1,
                           xonxoff=0
                          )

    master = modbus_rtu.RtuMaster(sensor)
    master.set_timeout(2.0)
    master.set_verbose(True)
    
    while True:
        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

        voltage = data[0] / 10.0 # [V]
        current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
        power = (data[3] + (data[4] << 16)) / 10.0 # [W]
        energy = data[5] + (data[6] << 16) # [Wh]
        frequency = data[7] / 10.0 # [Hz]
        powerFactor = data[8] / 100.0
        alarm = data[9] # 0 = no alarm

        json_data = {
            "voltage":voltage,
            "current":current,
            "power":power,
            "energy":energy,
            "frequency":frequency,
            "power_factor":powerFactor,
            "alarm":alarm
            }

        client.publish("home/energy", json.dumps(json_data))

        print('Voltage [V]: ', voltage)
        print('Current [A]: ', current)
        print('Power [W]: ', power) # active power (V * I * power factor)
        print('Energy [Wh]: ', energy)
        print('Frequency [Hz]: ', frequency)
        print('Power factor []: ', powerFactor)
        print('Alarm : ', alarm)

        # Change power alarm value to 100 W
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)
        time.sleep(5)

    try:
        master.close()
        if sensor.is_open:
            sensor.close()
    except KeyboardInterrupt:
        print('Interrupted')
    except:
        pass

except KeyboardInterrupt:
        print('Interrupted')
except:
    print("Error opening serial connection")
