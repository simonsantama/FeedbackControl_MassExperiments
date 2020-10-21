"""
FPA experiments
This algorithm uses a PID to control the IHF from the FPA's lamps so that samples pyrolyse at a constant mlr

Uses the PID algorithm developed by 
"""

# libraries
import numpy as np
import sys
import time
import msvcrt
import csv

# add path to import functions and classes
sys.path.insert(1, r"C:\\Users\\FireLab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\classes_and_functions")
from loadcell import MettlerToledoDevice
from datalogger import DataLogger
from PID import PID_IHF as PID

# create instance of the load cell class and check connection
print("\nConnection to load cell")
load_cell = MettlerToledoDevice()

# create instance of the data logger and check connection
print("\nConnection to data logger")
rm, logger = DataLogger().new_instrument()

##### ---- constant mlr ----- ####
mlr_desired = 2

# start test
print("Starting test")
time.sleep(2)
start_time = time.time()
previous_log = start_time
pretesting_period = 30

# create arrays large enough to accomodate one hour of data at 10 Hz for each experiment
IHF = np.zeros(3600*10)
t_array = np.zeros_like(IHF)
mass = np.zeros_like(IHF)
mlr = np.zeros_like(IHF)

logging_period = 0.1

# open file to dump all the data
with open("test_output.csv", "w", newline = "") as handle:
	writer = csv.writer(handle)
	writer.writerows([['time_seconds', "mass_g", "IHF_volts", "mlr_g/m-2s-1", "mlr_linearfit_gm-2s-1", "Observations"]])

	# record the number of readings
	step = 0

	# record mass for a period of 60 seconds before starting the test
	print("\nGathering of data for 60 seconds before testing")
	time.sleep(2)

	start_pretesting_period = time.time()
	while time.time() - start_pretesting_period < pretesting_period:

		# force a logging frequency of approx. 10 Hz (dno't want anything more than that)
		if time.time() - previous_log < 0.1:
			pass
		else:

			t_array[step] = time.time() - start_time
			mass[step] = load_cell.query_weight()

			if step == 0:
				writer.writerows([[t_array[step], mass[step], IHF[step], 0, 0, "start_logging"]])
			else:
				writer.writerows([[t_array[step], mass[step], IHF[step], 0, 0,""]])

			step += 1

			previous_log = time.time()

		# end if ESC is pressed
		if msvcrt.kbhit():
			if ord(msvcrt.getch()) == 27:
				break

	# additional parameters
	bool_starttest = True
	time_starttest = t_array[step]
	previous_log = time_starttest

	pid_input = 0
	pid_setpoint = mlr_desired
	previous_time = 0
	lastErr = 0
	lastInput = 0
	errSum = 0


	while True:
		try:

			# force a logging frequency of approx. 10 Hz (don't want anything more than that)
			if time.time() - previous_log < 0.1:
				pass
			else:

				# record time for this reading
				t_array[step] = time.time() - start_time

				# query mass and update array
				mass[step] = load_cell.query_weight()
				
				# calculate the instantaneous mlr
				mlr[step] = - np.round((mass[step] - mass[step-1]) / (t_array[step] - t_array[step-1])/0.1/0.1,1)


				# evaluate the mlr average and send new IHF to lamps
				mlr[mlr<0]=0
				mlr_moving_average = mlr[step-25:step].mean()

				## call the PID ##
				IHF[step+1], previous_time, lastErr, lastInput, errSum = PID(
					mlr_moving_average, pid_setpoint, previous_time, lastErr, lastInput, errSum)
				print("----")
				print(IHF[step+1])

				# write IHF to the lamps
				logger.write(':SOURce:VOLTage %G,(%s)' % (IHF[step+1], '@304'))

				# annotate the start of the test
				if bool_starttest:
					writer.writerows([[t_array[step], mass[step], IHF[step], mlr[step], mlr_moving_average, "start_test"]])
					bool_starttest = False
				else:
					writer.writerows([[t_array[step], mass[step], IHF[step], mlr[step], mlr_moving_average, ""]])

				# print the result of this iteration to the terminal window
				print(f"\ntime:{np.round(t_array[step],2)} - IHF:{IHF[step+1]} - mass: {mass[step]} - mlr:{np.round(mlr_moving_average,2)}")

				previous_log = time.time()

				step += 1
 
			# end if ESC is pressed
			if msvcrt.kbhit():
				if ord(msvcrt.getch()) == 27:
					writer.writerows([["", "", "", "", "end_test"]])
					break

		except Exception as e:
			print(f"\nInstantaneous error at {np.round(time.time() - start_time, 2)} seconds")
			print(f"Error:{e}")
			print("\nLogging continues")


			# end if ESC is pressed
			if msvcrt.kbhit():
				if ord(msvcrt.getch()) == 27:
					writer.writerows([["", "", "", "", "end_test"]])
					break


# volt = 1
# for i in range(10):
# 	logger.write(':SOURce:VOLTage %G,(%s)' % (volt, '@304'))
# 	if volt:
# 		volt = 0
# 	else:
# 		volt = 1
# 	print(volt)

# 	time.sleep(2)

# turn off the lamps and close the instrument
logger.write(':SOURce:VOLTage %G,(%s)' % (0.0, '@304'))
logger.close()
rm.close()



# finish the experiment
print("\n\nExperiment finished")
print(f"Total duration = {np.round((time.time() - start_time)/60,1)} minutes")

# # ask from the user the mlr that is to be kept constant
# while True:
# 	constant_mlr = input("\nInput mlr to be kept constant throughout the test: ")
# 	confirmation = input(f"MLR is: {constant_mlr}. Proceed? ")
# 	if not confirmation.lower() in ["yes", "y"]:
# 		continue
# 	else:
# 		break

