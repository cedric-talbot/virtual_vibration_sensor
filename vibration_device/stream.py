from iotile.core.hw.hwmanager import HardwareManager
from iotile.core.hw.reports import IndividualReadingReport, IOTileReading

def stream_vibrations(min_value, max_value) :
    """ Stream vibration data every second, all between min_value and max_value.
    """
    with HardwareManager(port='virtual:./vibration_device.py') as hw:
        hw.connect('1')
        con = hw.controller()
        con.set_min_and_max(min_value,max_value)
        hw.enable_streaming()
        """
        hw.iter_reports() will run forever until we kill the program
        with a control-c.
        """
        try:
            for report in hw.iter_reports(blocking=True):

                # Verify that the device is sending realtime data as we expect.
                assert isinstance(report, IndividualReadingReport)
                assert len(report.visible_readings) == 1

                reading = report.visible_readings[0]
                assert isinstance(reading, IOTileReading)

                # We just need the value here, use reading.stream and 
                # reading.reading_time to respectively get the stream 
                # and reading time. Print reading to get them all.
                print(reading.value)
        except KeyboardInterrupt:
            pass

stream_vibrations(0,18)