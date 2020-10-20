"""
This is a trial script to communicate with the FPA's load cell
Creates a Mettler toledo class based on the code by:
https://github.com/janelia-pypi and outputs the serial number
and 10 weight measurements

"""

import socket
import time
import numpy as np

class MettlerToledoDevice(object):
    """
    Creates a MettlerToledoDevice class which can be used to query the weight from the
    load cell.
    Designed for connection with the FPA load cell (TCP/IP) so the IP address and PORT number
    are hard-coded into the class.
    """

    IP_scale = "192.168.127.254"
    PORT_scale = 4001 

    def __init__(self):
        """
        Initializes the class by checking that connection is possible and then
        running the cancel command to erase any previous commands.
        """

        # open socket connection (TCP/IP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # set time out time for connections (seconds)
            s.settimeout(1)

            # connect to the terminal
            try:
                s.connect((self.IP_scale, self.PORT_scale))
            except Exception as e:
                print("\nCouldn't connect to the load cell when initiating the MettlerToledoDevice")
                print(f"Exception: {e}\n")


            # cancel (same as disconnecting and reconnecting)
            request = self._fomat_request("@")
            s.sendall(request)
            response = s.recv(1024).decode()
            print(f"\nSucessful connection with {response.split()}")


    def _fomat_request(self, request):
        """
        Formats the command according to MT-SICS requirements
        """
        request = bytes(f"{request} \r\n", "ascii")
        return request


    def query_weight(self):
        """
        Queries the weight.
        Prefers a stable readings but if time out is reached, it reads a dynamic weight

        """
        # open socket connection (TCP/IP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # set time out time for connections (seconds)
            s.settimeout(1)

            # connect to the terminal
            try:
                s.connect((self.IP_scale, self.PORT_scale))
            except Exception as e:
                print("Couldn't connect to the load cell when quering weight")
                print(f"Exception: {e}")


            # send stable weight or, if timeout (in ms), then send dynamic weight
            request = self._fomat_request("SC 420")
            s.sendall(request)
            response = s.recv(1024).decode()
            return response.split()


load_cell = MettlerToledoDevice()

start = time.time()
for i in range(10):
    print(f"{i} ------- {np.round(time.time() - start,2)} seconds")
    print(f"{load_cell.query_weight()}\n")