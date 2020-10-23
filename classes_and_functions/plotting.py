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

# find the most recently created folder


# filename = input("Insert test name: ")
# filename = f"{filename}.pickle"

# # -- create lists to store time and masses so that the plot can be updated
# plotting_time = []
# plotting_ACM = []
# plotting_ACMtray = []
# plotting_Insulation = []
# plotting_Insulationtray = []
# plotting_masses = [plotting_ACM, plotting_ACMtray, plotting_Insulationtray, plotting_Insulation]

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