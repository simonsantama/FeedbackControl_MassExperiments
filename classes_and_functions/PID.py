"""
PID function to calculate the IHF based on a set point and the current reading
"""
import time
import numpy as np

def PID_IHF(Input, Setpoint, previous_time, lastErr, lastInput, errSum, first_activation):
    """
    Uses a PID algorithm to calculate the IHF based on target and current nhf
    Output: IHF. Input: NHF: Setpoint: Target NHF.
    See: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/


	Parameters:
	----------


	Returns:
	-------



    """

    # define the maximum and minimum voltages
    Output_max = 4.5
    Output_min = 0

    # Define the k constants (determined experimentally)
    kp = 0.30
    ki = 0.04
    kd = 0.02

    # How long since we last calculated
    now = time.time()
    timeChange = now - previous_time

    # Compute all the working error variables
    error = Setpoint - Input
    errSum += error * timeChange

    # dERr ia according to the initial design, but later dInput is used
    dErr = (error - lastErr) / timeChange
    dInput = (Input - lastInput) / timeChange

    # Compute the Output
    Output = kp * error + ki * errSum - kd * dInput

    print("PID active")

    # protects the FPA
    if Output > Output_max:
        Output = Output_max
    elif Output < Output_min:
        Output = Output_min

    if first_activation and (Output < 1):
        Output = 1
        first_activation = False

    return Output, now, error, errSum, first_activation