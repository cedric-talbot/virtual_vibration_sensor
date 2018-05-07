from iotile.core.hw.proxy.proxy import TileBusProxyObject
from iotile.core.utilities.typedargs.annotate import return_type, context, param
from typedargs.exceptions import ArgumentError
import struct

@context("VibrationProxy")
class VibrationProxyObject(TileBusProxyObject):
    """A proxy object for the vibration device
    """

    @classmethod
    def ModuleName(cls):
        """The 6 byte name by which CoreTools matches the proxy object
        with an IOTile Device
        """
    	return 'Vibr01'


    @param("min_value", "integer")
    @param("max_value", "integer")
    def set_min_and_max(self, min_value, max_value):
        #min_value and max_value should be positive integers 
        if min_value < 0 or max_value < 0 :
            raise ArgumentError("Both values should be positive")

        #max_value should be greater than min_value
        if min_value > max_value :
            raise ArgumentError("max_value should be greater than min_value")

        args = struct.pack("<LL", min_value, max_value)
        self.rpc(0x90, 0x00, args)


    @return_type("list(integer)")
    def get_min_and_max(self):
        vibrs = self.rpc(0x90, 0x01, result_format="LL")
        return vibrs

        
    @return_type("integer")
    def get_vibration(self):
        vibr, = self.rpc(0x80, 0x00, result_format="L")
        return int(vibr)