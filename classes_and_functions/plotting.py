"""
This script plots the data while the main script is reading from the FPA data
loggers and the load cells. Not sure this is the best way to implement the
simultaneous plotting, but it does separate the two algorithms so that if there
is a problem with the plotting, the logging is not afected.

"""

# import libraries
import msvcrt
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import time
import sys

#####
# DETERMINE WHERE THE DATA FOR THE MOST RECENT EXPERIMENT IS
#####

# find the most recently created folder
path = "C:\\Users\\Firelab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\nitrogen_experiments"
all_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

folder_creation_time = 0
for folder in all_folders:
	ts = os.path.getmtime(os.path.join(path, folder))
	if ts > folder_creation_time:
		latest_folder = folder
		folder_creation_time = ts

#####
# CREATE AND FORMAT FIGURES
#####

# plotting parameters
fontsize_labels = 16
fontsize_legend = 14
linewidth_grid = 1
figure_size = (18,8)


# create figures 
plt.ion()
fig0, axes0 = plt.subplots(2,1, constrained_layout = True)
fig1, ax1 = plt.subplots(1,1, constrained_layout = True)


# format the plots
for a,ax in enumerate(axes0):
	ax.set_ylabel(["IHF [kW]", "MLR [g/m2s]"][a], fontsize = fontsize_labels)
	ax.set_xlabel("Time [s]", fontsize = fontsize_labels)
	ax.yaxis.grid(True, linewidth = linewidth_grid, linestyle = "--", color = "gainsboro")
ax1.set_ylabel("PID coefficients [-]", fontsize = fontsize_labels)
ax1.set_xlabel("Time [s]", fontsize = fontsize_labels)
ax1.yaxis.grid(True, linewidth = linewidth_grid, linestyle = "--", color = "gainsboro")


# add legend for mlr plot in figure 0
s = axes0[1].scatter([],[], color = "gray", alpha = 0.75, marker = "o", 
	label = "mlr")
l = axes0[1].plot([],[], color = "maroon", alpha = 0.75, linewidth = 1.5,
	label = "mlr_moving_average")
axes0[1].legend(fancybox = True, loc = "upper left", fontsize = fontsize_legend)

# add legend for PID coefficients plot in figure 1
list_plots = []
for i in range(3):
	l = ax1.plot([],[], color = ["maroon", "dodgerblue", "black"][i], linewidth = 1,
		linestyle = ["-", "--", ":"][i], 
		label = ["Proportional", "Integral", "Derivative"][i])
ax1.legend(fancybox = True, loc = "upper right", fontsize = fontsize_legend)



#####
# KEEP UPLOADING, READING AND PLOTTING THE DATA WHILE THE EXPERIMENT CONTINUES
#####

latest_folder_path = os.path.join(path, latest_folder)
for file in os.listdir(latest_folder_path):
	if ".pkl" in file:
		pickle_file = file

pickle_file_path = os.path.join(latest_folder_path, pickle_file)

# do an infinite loop where it reads the data and plots it to both figures
while True:

	try:
		with open(pickle_file_path, "rb") as handle:
			all_data = pickle.load(handle)
			
			# extract the data
			time_array = all_data["time"]
			IHF = all_data["IHF"]
			mlr = all_data["mlr"]
			mlr_moving_average = all_data["mlr_moving_average"]
			time_step = all_data["time_step"]

			time.sleep(1)
			plt.pause(0.001)
# # 			print(all_data.keys())
# # 			time.sleep(5)
# # 			time_array = all_data["t"]
# # 			IHF = all_data["IHF"]
# # 			mlr = IHF = all_data["mlr"]
# # 			time_step = all_data["time_step"]

# # 			plotting_list = [IHF, mlr, IHF, mlr]

# # 			for i,l in enumerate(list_plots):
# # 				l.set_data(time_array[:time_step], l[:time_step])
# # 				plt.pause(0.001)



	except Exception as e:
		print(f"\nError when loading pickle\n")
		print(e)

	if msvcrt.kbhit():
# 	    if ord(msvcrt.getch()) == 27:
# 	    	folder_path = os.path.join(path, latest_folder)
# 	    	figure0_name = f"{folder_path}/IHF_MLR.pdf"
# 	    	figure1_name = f"{folder_path}/PID_terms.pdf"
# 	    	fig0.savefig(f"{figure0_name}")
# 	    	fig1.savefig(f"{figure1_name}")
	    	sys.exit(0)


# while True:

#     try:
#         with open(filename, 'rb') as handle:
#             all_data = pickle.load(handle)

#             time_max = math.ceil(all_data["time"][-1] / 100) * 100
#             axes[0].set_xlim([0, time_max])

#             # parse data from the pickle
#             plotting_time = all_data["time"]
#             for i, key in enumerate(all_data.keys()):
#                 if key == "time":
#                     continue
#                 else:
#                     plotting_masses[i - 1] = np.array(all_data[key])

#             # update mass plots
#             for i, data in enumerate(plotting_masses):
#                 list_plots[i].set_data(plotting_time, plotting_masses[i] - plotting_masses[i][0])
#                 plt.pause(0.0001)

#     except Exception as e:
#         print(f"Error when loading pickle: {e}")



plt.show()