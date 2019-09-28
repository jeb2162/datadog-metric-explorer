# File that contains class for reading in the csv doc that contains custom metric usage
import pandas as pd

class custom_metric_usage:
	def __init__(self, run_time_parameters):
		self.file_path = run_time_parameters['file_path']['value']
		self.custom_metric_pd = self.load_custom_metric_object()
		self.custom_metric_list = self.custom_metric_pd['Metric Name'].tolist()


	# Main function for loading custom metric file
	def load_custom_metric_object(self):
		custom_metric_pd = pd.read_csv(self.file_path)
		return custom_metric_pd

	

