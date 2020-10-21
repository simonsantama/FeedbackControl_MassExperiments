"""
PID function to calculate the IHF based on a set point and the current reading
"""
import time


def PID_IHF(Input, Setpoint, previous_time, lastErr, lastInput, errSum):
    """
    Uses a PID algorithm to calculate the IHF based on target and current nhf
    Output: IHF. Input: NHF: Setpoint: Target NHF.
    See: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/


	Parameters:
	----------


	Returns:
	-------



    """

    # Define the maximum and minimum voltages
    Output_max = 4
    Output_min = 0

    # Define the k constants (determined experimentally)
    kp = 0.0001
    ki = 0.000005
    kd = 0.0000005

    # How long since we last calculated
    now = time.time()
    # Calculates time difference between last scan and this one
    timeChange = now - previous_time

    # Compute all the working error variables
    error = Setpoint - Input
    errSum += error * timeChange
    # dERr ia according to the initial design, but later dInput is used
    dErr = (error - lastErr) / timeChange
    dInput = (Input - lastInput) / timeChange

    # Compute the Output
    Output = kp * error + ki * errSum - kd * dInput

    print(Output)

    # protects the FPA
    if Output > Output_max:
        Output = Output_max
    elif Output < Output_min:
        Output = Output_min

    print(Output)

    return Output, now, error, Input, errSum