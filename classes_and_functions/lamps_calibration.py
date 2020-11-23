"""
Algorithm used to calibrate the lamps every morning.

"""

#####
# IMPORT LIBRARIES, CLASSES AND FUNCTIONS
#####

# libraries
import numpy as np
import sys
import time
import msvcrt
import csv
import os
import pickle

# add path to import functions and classes (absolute path on the FPA's computer)
sys.path.insert(1, r"C:\\Users\\FireLab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\classes_and_functions")
from datalogger import DataLogger

# create folder to store the calibration results of this particular day



#####
# CONNECT TO LOAD CELL AND DATA LOGGER AND INSTANTIATE CLASSES
#####

# create instance of the data logger and check connection
print("\nConnection to data logger")
rm, logger = DataLogger().new_instrument()


#####
# CALIBRATE THE LAMPS. FOLLOW JUAN'S METHOD. USE STEPS OF 0.2 VOLTS
#####

# for voltage_output_lamps in np.arange(0,5.2,0.2):
# 	print(voltage_output_lamps)


	# # write IHF to the lamps
	# logger.write(':SOURce:VOLTage %G,(%s)' % (voltage_output, '@304'))