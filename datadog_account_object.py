# File contains class for getting datadog monitor and dashboard information for an account.
from datadog import initialize, api
import requests
import datetime
import json
import pandas as pd

class datadog_account:
	def __init__(self, run_time_parameters):
		self.api_key = run_time_parameters['api_key']['value']
		self.app_key = run_time_parameters['app_key']['value']
		self.options = {
			'api_key': self.api_key,
			'app_key': self.app_key
		}
		initialize(**self.options)
		
		self.monitors = self.retrieve_all_monitors()
		self.dashboards = self.retreive_all_dashbaords()

	# Method for retrieving monitors
	def retrieve_all_monitors(self):
		monitors = api.Monitor.get_all()
		if 'errors' in monitors:
			raise Exception('\n\nError in calling Datadog API Key: {}\n\n'.format(monitors['errors']))
		return monitors

	# Method for retrieving dashboards
	def retreive_all_dashbaords(self):
		dashboard_list = api.Dashboard.get_all()
		# For each dashboard in list, call and get dashbaord info
		for dashboard in dashboard_list['dashboards']:
			dashboard_id = dashboard['id']
			dashboard_json = api.Dashboard.get(dashboard_id)
			# Add the dashboard json to the dashboard object
			dashboard['dashboard_json'] = dashboard_json
		# Return the dashboard_listh
		return dashboard_list

	# Method to get custom metrics usage over the last 90 days
	def get_custom_metrics_usage(self):
		# Get the datetime object for 90 days ago
		today = datetime.date.today()
		month_string = today.strftime("%Y-%m")
		datadog_usage_url = ('https://api.datadoghq.com/api/v1/usage/top_avg_metrics?api_key={}&application_key={}&month={}'.format(self.api_key, self.app_key, month_string))
		# Call datadog via the url to get usage
		response = requests.get(datadog_usage_url)
		# Convert response into JSON
		response_object = json.loads(response.text)
		custom_metric_pd = pd.DataFrame(response_object['usage'])

		return custom_metric_pd


	