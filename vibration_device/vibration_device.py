"""Virtual IOTile device to stream vibration data
"""

from iotile.core.hw.virtual.virtualdevice import VirtualIOTileDevice, rpc
import random

class VibrationDevice(VirtualIOTileDevice):
    """A  virtual IOTile device that can stream fake vibration data

    Args:
        args (dict): Any arguments that you want to pass to create this device.
    """

    def __init__(self, args) :
        super(VibrationDevice, self).__init__(1, 'Vibr01')
        self.min_value = 0
        self.max_value = 0
        #set the vibration interval to 1.0s
        self.create_worker(self._stream_vibrations, 1.0)

    @rpc(8, 0x0004, "", "H6sBBBB")
    def controller_status(self) :
        """Return the name of the controller as a 6 byte string
        """

        status = (1 << 1) | (1 << 0)  # Report configured and running
        return [0xFFFF, self.name, 1, 0, 0, status]

    @rpc(8, 0x9000, "LL")
    def set_min_and_max(self, min_value, max_value):
        """Set the values between which the device can vibrate
        """
        self.min_value = min_value
        self.max_value = max_value
        return []

    @rpc(8, 0x9001, "", "LL")
    def get_min_and_max(self) :
        """Send the current min and max values

        Returns :
            list  a list with two values containing the actual min and max
        """
        return [self.min_value, self.max_value]

    @rpc(8, 0x8000, "", "L")
    def get_vibration(self) :
        """Send the current vibration state
        I supposed it was an amplitude so its value can be negative

        Returns:
            list  a list with a single value containing the vibration state
        """
        return [random.randint(self.min_value, self.max_value)]

    def _stream_vibrations(self):
        """Stream vibration values
        """
        self.stream_realtime(0x1001, random.randint(self.min_value, self.max_value))