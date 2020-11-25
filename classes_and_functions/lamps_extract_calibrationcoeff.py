"""
Algorithm that extracts the calibration coefficinets for the lamps from the
latest calibration performed.

"""

import os
import pandas as pd

def extract_calibrationcoeff():
	"""
	Determines the latest polynomial fit coefficients to 
	relate heat flux in kW/m2 to the voltage to the lamps
	in VDC
	
	Parameters:
	----------
	None

	Returns:
	-------
	fit_coefficients = np.array()
		array of coefficients to determine the voltage to the lamps in VDC from
		the incident heat flux in kW/m2

	"""
	
	# determine the newest file in the calibration_data folder
	path = "C:\\Users\\FireLab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\calibration_data"
	
	files = os.listdir(path)
	paths = [os.path.join(path, basename) for basename in files if ".xlsx" in basename]
	latest_file = max(paths, key=os.path.getctime)

	# read the coefficients from the latest file
	file_path = os.path.join(path, latest_file)
	fit_data = pd.read_excel(file_path, sheet_name = "polynomial_fit")
	fit_coefficients = fit_data.loc[:, "coefficients"].values

	return fit_coefficients