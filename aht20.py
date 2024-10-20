from smbus2 import SMBus
import time

class Aht20(object):

    DEFAULT_ADDRESS = 0x38

    CMD_SOFTRESET = [0xBA]
    CMD_INITIALIZE = [0xBE, 0x08, 0x00]
    CMD_MEASURE = [0xAC, 0x33, 0x00]

    STATUSBIT_BUSY = 7  # The 7th bit is the Busy indication bit. 1 = Busy, 0 = not.
    STATUSBIT_CALIBRATED = 3  # The 3rd bit is the CAL (calibration) Enable bit. 1 = Calibrated, 0 = not

    DIVIDER = pow(2, 20)

    def __init__(self, bus: SMBus, address: int = DEFAULT_ADDRESS):

        # i2c/smbus instance
        self.bus = bus

        # chip address, by default = 0x38
        self.address = address

        # last readout temperature
        self.temperature: float = 0.0

        # last readout humidity
        self.humidity: float = 0.0

        # last readout time
        self.time: float = 0.0

        # Do soft restart of the
        self._initialize_chip()

    def _initialize_chip(self):
        """
            Does a softrestart of the chip and calibrate it
        :return:
        """

        # Softreset
        self.bus.write_i2c_block_data(self.address, self.CMD_SOFTRESET[0], [])
        time.sleep(0.04)

        # Calibrate
        self.bus.write_i2c_block_data(self.address, self.CMD_INITIALIZE[0], self.CMD_INITIALIZE[1:])
        time.sleep(0.01)

    def get_temperature(self) -> float:
        return self.temperature

    def get_humidity(self) -> float:
        return self.humidity

    def get_time(self) -> float:
        return self.time

    def do_measure(self):
        # Ask the chip to do a measurement, then wait 80ms as specs require
        self.bus.write_i2c_block_data(self.address, self.CMD_MEASURE[0], self.CMD_MEASURE[1:])

        busy = True
        while busy:
            # Read data (7 bytes) from chip, then check if bit 7 of status byte (i.e.: data[0])
            # is set. If so, repeat reading because the chip is busy
            time.sleep(0.08)
            data = self.bus.read_i2c_block_data(self.address, self.CMD_MEASURE[0], 7)
            busy = (data[0] & self.STATUSBIT_BUSY) == 1

        raw_humidity = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        raw_temperature = ((data[3] & 0xf) << 16) | (data[4] << 8) | (data[5])

        # Calculate humidity using the specs formula (Srh / 2^20) * 100
        self.humidity = (raw_humidity / self.DIVIDER) * 100

        # Calculate temperature using the specs formula (St / 2^20) * 200 - 50
        self.temperature = ((raw_temperature / self.DIVIDER) * 200) - 50

        # Record the time of the reading
        self.time = time.time()
