"""
Class use to connect to the FPA's data logger

"""

import visa
import sys

class DataLogger(object):
    """
    Creates a DataLogger class which connects to the FPA's data logger.
    """

    VISA_ADDRESS = "GPIB0::9::INSTR"

    def __init__(self):
        """
        Initializes the class by checking that connection is possible 
        and sending query for the ID number of the logger
        """

        rm = visa.ResourceManager()
        my_instrument = rm.open_resource(self.VISA_ADDRESS)
        idn = my_instrument.query("*IDN?")
        print(f"Connected to: {idn}")

 