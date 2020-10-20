"""
FPA experiments
This algorithm uses a PID to control the IHF from the FPA's lamps so that samples pyrolyse at a constant mlr

Uses the PID algorithm developed by 
"""

# libraries
import numpy
import sys

# add path to import functions and classes
sys.path.insert(1, r"C:\\Users\\FireLab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\classes_and_functions")
from loadcell import MettlerToledoDevice
from datalogger import DataLogger

# create instance of the load cell class and check connection
print("\nConnection to load cell")
load_cell = MettlerToledoDevice()

# create instance of the data logger and check connection
print("\nConnection to data logger")
logger = DataLogger()


# ask from the user the mlr that is to be kept constant
while True:
	constant_mlr = input("\nInput mlr to be kept constant throughout the test: ")
	confirmation = input(f"MLR is: {constant_mlr}. Proceed? ")
	if not confirmation.lower() in ["yes", "y"]:
		continue
	else:
		break

