"""
FPA experiments
This algorithm uses a PID to control the IHF from the FPA's lamps so that samples pyrolyse at a constant mlr

Experimental procedure:
1. Lamps follow a linear heating ramp, with lambda (irradiation rate) = 0.5 kW/m^2 until the 
mlr is within 25% of the desired value
2. Once the mlr is within the desired value, the control of the lamps is passed to the PID controller,
until the test is ended.

Use command: 'prompt $g' to shorten command prompt
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
from loadcell import MettlerToledoDevice
from datalogger import DataLogger
from PID import PID_IHF as PID


#####
# CONNECT TO LOAD CELL AND DATA LOGGER AND INSTANTIATE CLASSES
#####

# create instance of the load cell class and check connection
print("\nConnection to load cell")
load_cell = MettlerToledoDevice()

# create instance of the data logger and check connection
print("\nConnection to data logger")
rm, logger = DataLogger().new_instrument()


# #####
# # REQUEST FROM THE USER THE DESIRED MLR (CONSTANT) AND THE NAME OF THE EXPERIMENT
# #####
# while True:
# 	try:
# 		mlr_desired = int(input("\nInput mlr to be kept contant throughout the test: "))
# 		number_of_test = input("Input number of test in format XXX": )
# 		material = input("Input material: ").lower()

# 		name_of_file = f"N2_{number_of_test}_{material}_{mlr_desired}gm-2s-1.csv"

# 		# confirm the values entered by user
# 		confirmation = input(f"\nDesired mlr = {mlr_desired} g/m2s. \nName of file: {name_of_file}.\nProceed?")
# 		if not confirmation.lower() in ["yes", "y"]:
# 			continue
# 		else:
# 			break

# 	except Exception as e:
# 		print("Invalid file name or mlr")

# 		# turn off the lamps and close the instrument
# 		logger.write(':SOURce:VOLTage %G,(%s)' % (0.0, '@304'))
# 		logger.close()
# 		rm.close()
# 		sys.exit()

# name_of_folder = name_of_file.split(".")[0]
# full_name_of_file = os.path.join(name_of_folder, name_of_file)
# # create folder with the name of the file
# if not os.path.exists(name_of_folder):
# 	os.mkdir(name_of_folder)
# # do not overwrite the file
# else:
# 	sys.exit()



# #####
# # INITIALIZE USEFUL PARAMETERS AND START TEST
# #####

# print("Starting test")
# time.sleep(2)

# # experiment parameters
# time_pretesting_period = 20
# time_logging_period = 0.05
# surface_area = 0.1*0.1
# averaging_window = 30
# irradiation_rate = 0.5

# # epsilon is percentage of mlr_desired used to forcefully reduce oscillations
# epsilon = 0.15

# # FPA lamps
# max_lamp_voltage = 4.75
# min_lamp_voltage = 0.25

# # convert irradiation rate using the calibration coefficients (from kW/m-2s to volts/s)
# irradiation_rate = irradiation_rate/50

# # create arrays large enough to accomodate one hour of data at the pre-set maximum logging frequency
# t_array = np.zeros(int(3600/time_logging_period))
# IHF = np.zeros_like(t_array)
# mass = np.zeros_like(t_array)
# mlr = np.zeros_like(t_array)
# mlr_moving_average_array = np.zeros_like(t_array)

# # PID
# PID_state = "not_active"
# PID_kp = 0.40
# PID_ki = 0.06
# PID_kd = 0.1
# PID_integral_term_array = np.zeros_like(t_array)
# PID_proportional_term_array = np.zeros_like(t_array)
# PID_derivative_term_array = np.zeros_like(t_array)

# # open csv file to write data
# with open(full_name_of_file, "w", newline = "") as handle:
# 	writer = csv.writer(handle)
# 	writer.writerows([['time_seconds', "mass_g", "IHF_volts", "mlr_g/m-2s-1", 
# 		"mlr_movingaverage_gm-2s-1", "Observations", "PID_state"]])

# 	# record the number of readings
# 	time_step = 0

# 	# ------
# 	# record mass for a period of 60 seconds before starting
# 	# ------
# 	print("\nGathering data for 60 seconds before testing")
# 	time.sleep(2)

# 	time_start_logging = time.time()
# 	previous_log = time.time()
# 	while time.time() - time_start_logging < time_pretesting_period:

# 		# enforce a maximum logging frequency of 20 Hz
# 		if time.time() - previous_log < time_logging_period:
# 			pass
# 		else:

# 			t_array[time_step] = time.time() - time_start_logging
# 			mass[time_step] = load_cell.query_weight()

# 			if time_step == 0:
# 				mlr[time_step] = 0
# 			else:
# 				# calculate mlr and force all negative readings to zero
# 				mlr[time_step] = - np.round((mass[time_step] - mass[time_step-1]) / (t_array[time_step] - t_array[time_step-1])/surface_area,1)
# 				mlr[mlr<0]=0

# 				# while I haven't done the necessary number of readings, averaging window needs to be smaller
# 				averaging_window_pretest = np.min([averaging_window, time_step])
# 				mlr_moving_average = mlr[time_step - averaging_window_pretest:time_step].mean()
# 				mlr_moving_average_array[time_step] = mlr_moving_average			

# 			# write data to the csv file
# 			if time_step == 0:
# 				writer.writerows([[t_array[time_step], mass[time_step], IHF[time_step], mlr[time_step], 
# 					mlr_moving_average_array[time_step], "start_logging", PID_state]])
# 			else:
# 				writer.writerows([[t_array[time_step], mass[time_step], IHF[time_step], mlr[time_step],
# 					mlr_moving_average_array[time_step],"", PID_state]])


# 			previous_log = time.time()
# 			time_step += 1

# 		# end if ESC is pressed
# 		if msvcrt.kbhit():
# 			if ord(msvcrt.getch()) == 27:
# 				break

# 	# ------
# 	# define additional parameters for start of test
# 	# ------

# 	bool_start_test = True
# 	bool_PID_active = False
# 	time_start_test = time.time()
# 	previous_log = time_start_test

# 	while True:
# 		try:

# 			# enforce a maximum logging frequency of 20 Hz
# 			if time.time() - previous_log < time_logging_period:
# 				pass
# 			else:

# 				# record time for this reading
# 				t_array[time_step] = time.time() - time_start_logging

# 				# query mass and update array
# 				mass[time_step] = load_cell.query_weight()
				
# 				# calculate the instantaneous mlr
# 				mlr[time_step] = - np.round((
# 					mass[time_step] - mass[time_step-1]) / (t_array[time_step] - t_array[time_step-1])/0.1/0.1,1)

# 				# calculate mlr and force all negative readings to zero
# 				mlr[time_step] = - np.round((mass[time_step] - mass[time_step-1]) / (t_array[time_step] - t_array[time_step-1])/surface_area,1)
# 				mlr_moving_average = mlr[time_step - averaging_window:time_step].mean()
# 				mlr_moving_average_array[time_step] = mlr_moving_average

# 				input_mlr = mlr_moving_average

# 				# forcefully remove the error if we are epsilon percent from the desired value
# 				current_error = mlr_desired - mlr_moving_average
# 				if np.abs(mlr_moving_average - mlr_desired) < epsilon * mlr_desired:
# 					input_mlr = mlr_desired
# 					# print(f"\n ------- David's idea at play! mlr:{mlr_moving_average, input_mlr}")

# 				# start with a ramped IHF, and once mlr reaches 0.9*mlr_desired, activate PID
# 				if PID_state == "not_active":
# 					IHF[time_step+1] = (t_array[time_step] - t_array[0]) * irradiation_rate
# 					voltage_output = IHF[time_step+1]

# 					if voltage_output > max_lamp_voltage:
# 						voltage_output = max_lamp_voltage
# 						IHF[time_step+1] = max_lamp_voltage

# 					if mlr_moving_average > 0.9*mlr_desired:
# 						PID_state = "active"
# 						print("\n-----")
# 						print("PID ACTIVE")
# 						print("-----\n")

# 						# set pid parameters
# 						previous_pid_time = time.time()
# 						last_error = mlr_desired - mlr_moving_average
# 						last_input = mlr_moving_average
# 						pid_integral_term = voltage_output
# 						pid_proportional_term = 0
# 						pid_derivative_term = 0


# 				# call PID
# 				elif PID_state == "active":

# 					voltage_output, previous_pid_time, last_error, pid_proportional_term, \
# 					pid_integral_term, pid_derivative_term = \
# 											PID(
# 											input_mlr, mlr_desired, previous_pid_time, 
# 											last_error, last_input, pid_integral_term, PID_kp, PID_ki, PID_kd,
# 											max_lamp_voltage, min_lamp_voltage)
# 					IHF[time_step+1] = voltage_output
# 					last_input = mlr_moving_average

# 					PID_proportional_term_array[time_step] = pid_proportional_term
# 					PID_integral_term_array[time_step] = pid_integral_term
# 					PID_derivative_term_array[time_step] = pid_derivative_term

# 				# write IHF to the lamps
# 				logger.write(':SOURce:VOLTage %G,(%s)' % (voltage_output, '@304'))

# 				# write data to the csv file
# 				if bool_start_test:
# 					writer.writerows([[t_array[time_step], mass[time_step], voltage_output, 
# 						mlr[time_step], mlr_moving_average, "start_test", PID_state]])
# 					bool_start_test = False
# 				else:
# 					writer.writerows([[t_array[time_step], mass[time_step], voltage_output, 
# 						mlr[time_step], mlr_moving_average, "", PID_state]])

# 				# save data as a a dict in a pickle to be read and plotted by another algorithm
# 				data_for_pickle = {"t":t_array,
# 									"IHF": IHF,
# 									"mlr": mlr_moving_average_array,
# 									"time_step": time_step,
# 									}
# 				with open(f"{full_name_of_file.split('.')[0]}.pkl", "wb") as handle:
# 					pickle.dump(data_for_pickle, handle)

# 				# print the result of this iteration to the terminal window
# 				print(f"time:{np.round(t_array[time_step],2)} - IHF:{np.round(IHF[time_step+1],2)} - mass: {mass[time_step]} - mlr:{np.round(mlr_moving_average,2)}\n")

# 				previous_log = time.time()

# 				time_step += 1
 
# 			# end if ESC is pressed
# 			if msvcrt.kbhit():
# 				if ord(msvcrt.getch()) == 27:
# 					writer.writerows([["", "", "", "", "end_test"]])
# 					break

# 		## ---- handle an exception during testing and continue logging the data
# 		except Exception as e:
# 			print(f"\nInstantaneous error at {np.round(time.time() - time_start_logging, 2)} seconds")
# 			print(f"Error:{e}")
# 			print("\nLogging continues")


# 			# end if ESC is pressed
# 			if msvcrt.kbhit():
# 				if ord(msvcrt.getch()) == 27:
# 					writer.writerows([["", "", "", "", "","end_test"]])
# 					break


# #####
# # CLOSE CONNECTION TO THE LOGGER, TURN OFF LAMPS AND FINISH THE EXPERIMENT
# #####

# # turn off the lamps and close the instrument
# logger.write(':SOURce:VOLTage %G,(%s)' % (0.0, '@304'))
# logger.close()
# rm.close()

# # finish the experiment
# print("\n\nExperiment finished")
# print(f"Total duration = {np.round((time.time() - time_start_logging)/60,1)} minutes")
