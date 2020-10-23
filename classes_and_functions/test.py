import pickle
import os
import time

with open("C:\\Users\\FireLab\\Desktop\\Simon\\FeedbackControl_MassExperiments\\nitrogen_experiments\\constant_mlr\\test_output\\test_output.pkl", "rb") as handle:
	all_data = pickle.load(handle)
	print(all_data.keys())
	time.sleep(5)
	time_array = all_data["t"]
	IHF = all_data["IHF"]
	mlr = IHF = all_data["mlr"]
	time_step = all_data["time_step"]