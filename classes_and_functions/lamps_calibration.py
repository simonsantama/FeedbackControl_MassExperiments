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
# CALIBRATE THE LAMPS.
#####

# define constants


# define arrays used for polynomial fitting
hf_gauge_factor = 0.1017          # mv/kW/m2
nmbr_readings_pervoltage = 20
nmbr_voltages = np.linspace(0,4.75,20)
all_output_voltages = np.zeros(nmbr_readings_pervoltage*len(nmbr_voltages))
all_input_voltages = np.zeros_like(all_output_voltages)
all_input_kWm2 = np.zeros_like(all_output_voltages)

t = 0

# increasing the heat flux in steps
for v, output_voltage in enumerate(nmbr_voltages):

	# protect the lamps
	if output_voltage > 4.75:
		output_voltage = 4.75

	# send voltage to lamps
	logger.write(':SOURce:VOLTage %G,(%s)' % (0.0, '@304'))

	# wait 5 seconds for the lamps to estabilise
	time.sleep(5)
	print(f"\n\n ---- Voltage output to the lamps: {output_voltage} V\n")

	for nmr_readings in range(nmbr_readings_pervoltage):

		print(t)

		# read voltage from the  hf gauge
		input_voltage = float(logger.query(':MEASure:VOLTage:DC? (%s)' % ('@110')))
		print(f"Voltage readings from the hf gauge: {np.round(input_voltage*1000,6)} mV")
		print(f"Corresponding heat flux: {np.round(input_voltage/hf_gauge_factor,2)} kW/m2\n")

		# save the data
		all_output_voltages[t] = output_voltage
		all_input_voltages[t] = input_voltage
		all_input_kWm2 = input_voltage/hf_gauge_factor

		# update the counter
		t += 1

# decreasing the heat flux in steps


# save all the data into an excel file




# run a couple of test heat flux curves to evaluate performance of the lamps
bool_extra_linear = input("\nComplete test of lamps with  linear HF?").lower()
if bool_extra_linear