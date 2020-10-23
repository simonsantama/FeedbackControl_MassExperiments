"""
Class use to connect to the FPA's data logger

"""

import visa
import sys

class DataLogger():
    """
    Creates a DataLogger class which connects to the FPA's data logger.
    """

    VISA_ADDRESS = "GPIB0::9::INSTR"
    time_out = 1000

    def __init__(self):
        """
        Initializes the class by checking that the connection is possible 
        and sending query for the ID number of the logger

        Additionally, it prints to the command window that the connection
        has been successful
        """

        rm = visa.ResourceManager()
        my_instrument = rm.open_resource(self.VISA_ADDRESS)
        idn = my_instrument.query("*IDN?")
        print(f"Successful connection to {idn}")


    def new_instrument(self):
        """
        Connects to the data logger and returns the instrument as well
        as the visa Resource Manager (used to close the connection)

        Returns:
        -------
        rm: visa.ResourceManager
            visa resource manager created by the visa library

        my_instrument: rm.open_resource()
            logger instrument from which it is possible to write commands 
            and query states.
        """

        rm = visa.ResourceManager()
        my_instrument = rm.open_resource(self.VISA_ADDRESS)

        # initial configuration
        my_instrument.write(":ABORt")
        my_instrument.write("*RST")
        my_instrument.write("*CLS")
        my_instrument.time_out = self.time_out

        # make sure the lamps are off before starting
        my_instrument.write(':SOURce:VOLTage %G,(%s)' % (0, '@304'))
        
        return (rm, my_instrument)