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
fig0, ax0 = plt.subplots(2,1, constrained_layout = True)
fig1, ax1 = plt.subplots(1,1, constrained_layout = True)

# # format the plots
# for a, ax in enumerate([ax0, ax1]):
# 	ax.set_xlabel("Time [s]", fontsize = fontsize_labels)
# 	ax.yaxis.grid(True, linewidth = linewidth_grid, linestyle = "--", color = "gainsboro")
# 	ax.set_title(["IHF and averaged MLR", "Contribution of PID coefficients"][a], fontsize = fontsize_labels + 1)
# 	ax.set_ylim([[-1,7],[0,2]][a])
# ax1.set_ylabel("PID_term/IHF", fontsize = fontsize_labels)	

# # add plots
# list_plots = []
# for i in range(2):
# 	l = ax0.plot([], [], color = ["maroon", "dodgerblue"][i], 
# 		linestyle = "", marker = ["o", "d"][i], markersize = 5, label = ["IHF [volts]", "MLR [g/m2s]"][i])
# 	list_plots.append(l)

# for i in range(3):
# 	l = ax1.plot([], [], color = ["maroon", "dodgerblue", "forestgreen"][i], 
# 		linestyle = "", marker = ["o", "d", "+"][i], markersize = 5, 
# 		label = ["Proportional term", "Integral term", "Derivative term"][i])
# 	list_plots.append(l)

# # add legends
# for ax in [ax0,ax1]:
# 	ax.legend(fancybox = True, loc = "upper left", fontsize = fontsize_legend)
# plt.pause(1)


# #####
# # DETERMINE WHERE THE DATA FOR THE MOST RECENT EXPERIMENT IS
# #####

# # find the most recently created folder
# path = "C:\\Users\\Firelab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\nitrogen_experiments\\constant_mlr"
# all_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

# folder_creation_time = 0
# for folder in all_folders:
# 	ts = os.path.getmtime(os.path.join(path, folder))
# 	if ts > folder_creation_time:
# 		latest_folder = folder
# 		folder_creation_time = ts

# #####
# # KEEP UPLOADING, READING AND PLOTTING THE DATA WHILE THE EXPERIMENT CONTINUES
# #####

# pickle_file_name = f"{latest_folder}.pkl"

# # do an infinite loop where it reads the data and plots it to both figures
# while True:

# 	try:
# 		with open(os.path.join(path, folder, pickle_file_name), "rb") as handle:
# 			all_data = pickle.load(handle)
# 			print(all_data.keys())
# 			time.sleep(5)
# 			time_array = all_data["t"]
# 			IHF = all_data["IHF"]
# 			mlr = IHF = all_data["mlr"]
# 			time_step = all_data["time_step"]

# 			plotting_list = [IHF, mlr, IHF, mlr]

# 			for i,l in enumerate(list_plots):
# 				l.set_data(time_array[:time_step], l[:time_step])
# 				plt.pause(0.001)



# 	except Exception as e:
# 		print(f"Error when loading pickle {e}")

# 	if msvcrt.kbhit():
# 	    if ord(msvcrt.getch()) == 27:
# 	    	folder_path = os.path.join(path, latest_folder)
# 	    	figure0_name = f"{folder_path}/IHF_MLR.pdf"
# 	    	figure1_name = f"{folder_path}/PID_terms.pdf"
# 	    	fig0.savefig(f"{figure0_name}")
# 	    	fig1.savefig(f"{figure1_name}")
# 	    	break


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





# # -- create plots and format them
# plt.ion()
# fig, axes = plt.subplots(1, 4, figsize=(12, 12), sharex=True, sharey=True)
# # fig.canvas.manager.full_screen_toggle()
# axes[0].set_ylabel("Mass [g]", fontsize=16)
# axes[0].set_xlim([0, 100])
# axes[0].set_ylim([-500, 500])
# axes[0].set_yticks([-500, -250, 0, 250, 500])
# for ax in axes:
#     ax.set_xlabel("Time [s]", fontsize=16)
# # column titles
# for a, ax in enumerate(axes):
#     ax.set_title(["ACM", "ACM tray", "Insulation tray", "Insulation"][a], fontsize=20)
# # empty plots with data that updates in time
# list_plots = []
# for a, ax in enumerate(axes):
#     l, = ax.plot(plotting_time, plotting_masses[a], linestyle=None, marker="o", markersize=3, markerfacecolor="None", markeredgecolor="r")
#     list_plots.append(l)
# # grid
# for ax in axes:
#     ax.grid(True, color="gainsboro", linestyle="--", linewidth=0.75)
# plt.pause(0.5)

# # read csv file and update the plot
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

#     if msvcrt.kbhit():
#         if ord(msvcrt.getch()) == 27:
#             plt.savefig(f"{filename.split('.')[0]}_testingplot.png")
#             break