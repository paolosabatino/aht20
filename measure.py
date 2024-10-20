from smbus2 import SMBus
from aht20 import Aht20
from datetime import datetime
import time

bus_id = 1

i2c = SMBus(bus_id)
aht20 = Aht20(i2c)

try:
    while True:
        aht20.do_measure()
        date = datetime.fromtimestamp(aht20.get_time())
        print("%s - Temperature: %.2f °C, Relative Humidity: %.2f%%" %
              (date.strftime("%Y-%M-%d %H:%I:%S"), aht20.get_temperature(), aht20.get_humidity()))
        time.sleep(5)
except KeyboardInterrupt:
    pass
