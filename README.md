## aht20

AHT20 small python library and companion meaurement example script.
Reduces traffic on the i2c bus to the least amount required to get a fully working device.

# Dependencies

Only smbus2 library is required

# Usage

Simplest usage:

```python
from smbus2 import SMBus
from aht20 import Aht20

bus_id = 1

i2c = SMBus(bus_id)
aht20 = Aht20(i2c)

aht20.do_measure()

print(aht20.get_temperature())
print(aht20.get_humidity())
```
