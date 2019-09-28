# Main file for the Datadog Metric Explore Script.
import sys
from custom_metric_data import custom_metric_usage
from datadog_account_object import datadog_account

def main(run_time_parameters):
	custom_metric_object = custom_metric_usage(run_time_parameters)
	dd_account_object = datadog_account(run_time_parameters)

# Function to get input paramters from command line
def get_run_time_parameters():
	# Default run_time_parameters to use if no user inputs
	run_time_parameters = {'api_key':{'value':None,'discription':'Api key for Datadog Org you whish to explore metrics for. Here is infor on DD api keys: https://docs.datadoghq.com/account_management/api-app-keys/'},
							'app_key':{'value':None,'discription':'App key for Datadog Org you whish to explore metrics for. Here is infor on DD app keys: https://docs.datadoghq.com/account_management/api-app-keys/#application-keys'},
							'file_path':{'value':None,'discription':'File path to custom metric csv file.'}}
	# Check to see if user asked for help                    
	help(run_time_parameters)
	# Loop through each key in the run_time_parameters to get the command line input for it
	for key in run_time_parameters:
		# Look at all items in sys.argv, all of the variables passed into script when run using: python3 load_test.py <number_of_logs_per_second> <length_of_log>
		for item in sys.argv:
			index_of_key = item.find(key)
			# If key is in item, attempt to get inputed value and update the run_time_parameters
			if index_of_key != -1:
				try:
					index_of_colon = item.find(':') + 1
					run_time_parameters[key]['value'] = item[index_of_colon:]
				except:
					raise Exception('\n\nInvalid Entry for {} input\n\n'.format(key))
		# Check if the key's value is None, if so raise exception as it is a required item
		if run_time_parameters[key]['value'] == None:
			raise Exception('\n\n{} is a required input\n\n'.format(key))
	# Return the run_time_parameters 
	return run_time_parameters

# Help function 
def help(run_time_parameters):
	for item in sys.argv:
		# Check if help was submitted in command line
		index_of_key  = item.find('help')
		if index_of_key != -1:
			# Help was submited. So now print out helpful information on running this script
			print('\n\n\n*** Help for load_test.py ***\n')
			print('This script requires runs on python 3.7 or later\n')
			run_script_text = "Run script via: python3 dd_metric_explorer.py "
			for key in run_time_parameters:
				run_script_text = run_script_text + key + ':<' + key + '> '
			print(run_script_text + '\n')
			# Loop through each key in run_time_parameters and print out its description
			for key in run_time_parameters:
				print('\n' + key + ': ' + run_time_parameters[key]['discription'])
				print('Default Value: ' + str(run_time_parameters[key]['value']))
			print('\n\n\n')
			# After printing out help info, exit the script and return to command line
			sys.exit(0)

# Initialization function
if __name__ == '__main__':
	# Get runtime parameters
	run_time_parameters = get_run_time_parameters()
	# Call into the main funciton
	main(run_time_parameters)