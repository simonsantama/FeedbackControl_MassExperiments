"""
This is a trial script to communicate with the FPA's load cell
"""

# import libraries
import socket
import csv
import msvcrt
import os
import time
import numpy as np
import pickle

# -- establish the desired logging period (1/f)
logging_frequency = 0.1
# IP address and port (scale) - STATIC
IP_scale = "192.168.127.254"
PORT_scale = 4001
# boolean used for zeroing mass
first_reading = True


# # -- request and store name of the file (friendly user, no parsing)
# filename = input("Insert test name: ")
# filename = f"{filename}.csv"
# # check that the file doesn't exists in this folder
# while os.path.isfile(filename):
#     print("File already exists")
#     filename = input("Insert test name: ")
#     filename = f"{filename}.csv"

# # data storage to save as pickle for quiker reading by plotting algorithm
# all_data = {"time": [], "ACM": [], "ACMtray": [], "Insulationtray": [], "Insulation": []}


def send_recv(s, command):
    """
    Sends command to IND780 unit and receives response string
    """
    command = bytes(f"{command} \r\n", "utf-8")
    s.sendall(command)
    return(s.recv(1024).decode())


# # -- open csv file to store results
# with open(filename, mode="w", newline="") as f:
#     filewriter = csv.writer(f, delimiter=',')
#     filewriter.writerow(["Time", "LC1_ACM", "LC2_ACM_tray", "LC3_insulation_tray",
#                          "LC4_insulation"])

# -- open the TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # connect to the terminal
    s.connect((IP_scale, PORT_scale))
    print("que paso")
    # print(s.recv(1024).decode())

#         # set time out time for connections (seconds)
#         s.settimeout(3)

#         # log on (find out why no user name is required, but so far, this is the only way it works)
#         send_recv(s, "user")

#         # timer to ensure logging frequency of 10 Hz
#         start = time.time()
#         beginning = start

#         # -- scan mass until stopped
#         while True:
#             try:

#                 # verify condition that forces the logging frequency
#                 if time.time() - start < logging_frequency:
#                     continue

#                 # read the list of masss from the load cell
#                 response = send_recv(s, "read wt0101 wt0201 wt0301 wt0401")

#                 # separate the string into independent readings
#                 mass_0 = float(response.split("~")[1:-1][0]) * 1000
#                 mass_1 = float(response.split("~")[1:-1][1]) * 1000
#                 mass_2 = float(response.split("~")[1:-1][2]) * 1000
#                 mass_3 = float(response.split("~")[1:-1][3]) * 1000
#                 all_masses = [mass_0, mass_1, mass_2, mass_3]

#                 # write data into the .csv ile
#                 filewriter.writerow([time.time() - beginning, all_masses[0], all_masses[1], all_masses[2], all_masses[3]])
#                 print("Writing to .csv file ...")
#                 print(np.round(time.time() - beginning, 1), np.round(mass_0, 1), np.round(mass_1, 1), np.round(mass_2, 1),
#                       np.round(mass_3, 1))

#                 all_data["time"].append(time.time() - beginning)
#                 all_data["ACM"].append(all_masses[0])
#                 all_data["ACMtray"].append(all_masses[1])
#                 all_data["Insulationtray"].append(all_masses[2])
#                 all_data["Insulation"].append(all_masses[3])

#                 with open(f"{filename.split('.')[0]}.pickle", 'wb') as handle:
#                     pickle.dump(all_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

#                 # end if ESC is pressed
#                 if msvcrt.kbhit():
#                     if ord(msvcrt.getch()) == 27:
#                         break

#                 # re-establish start for the next reading
#                 start = time.time()

#             # deal with instantaneous errors in the communication
#             except:
#                 print("Instantaneous communication error, logging continues")
#                 pass