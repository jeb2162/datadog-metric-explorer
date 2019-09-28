# File contains class for getting datadog monitor and dashboard information for an account.
from datadog import initialize, api

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
		print('DASHBOARDS BELOW ************************\n\n')
		print(self.dashboards)


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

	