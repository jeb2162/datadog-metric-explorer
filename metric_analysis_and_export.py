# File that contains class for analyzing custom metric usage
import pandas as pd

class analyze_metrics:
	def __init__(self, custom_metric_pd, dd_account_object):
		self.custom_metric_pd = custom_metric_pd
		self.custom_metric_list = self.custom_metric_pd['metric_name'].tolist()
		self.dd_account_object = dd_account_object
		# Initialize a blank dataframe which we can use to export data to.
		self.report_df = pd.DataFrame()
		# Run metric analaysis
		self.run_metrics_analysis_loop()

		print('\n\ncustom_metric_pd:\n{}\n\n'.format(custom_metric_pd))

		export_csv =custom_metric_pd.to_csv (r'/Users/josh.brown/Desktop/test_export.csv', index = None, header=True)
		

	# Method to run through all metrics in custom metric object and get 
	def run_metrics_analysis_loop(self):
		row_index = 0
		for metric in self.custom_metric_list:
			monitors_that_use_metric, count_of_monitors_that_use_metric = self.get_metric_use_in_monitors(metric)
			dashboards_that_use_metric, count_of_dashboards_taht_use_metric = self.get_metric_use_in_dashboards(metric)
			# Add values for metric into dataframe
			self.custom_metric_pd.loc[row_index, 'count_of_monitors_that_use_metric'] = count_of_monitors_that_use_metric
			self.custom_metric_pd.loc[row_index, 'monitors_that_use_metric'] = monitors_that_use_metric
			self.custom_metric_pd.loc[row_index, 'dashboards_that_use_metric'] = dashboards_that_use_metric
			self.custom_metric_pd.loc[row_index, 'count_of_dashboards_taht_use_metric'] = count_of_dashboards_taht_use_metric

			row_index += 1



	# Method to get metric use in monitors
	def get_metric_use_in_monitors(self, metric):
		number_of_monitors_used_in = 0
		monitor_list = ''
		# Loop through each monitor to determin where the metric is used
		for monitor in self.dd_account_object.monitors:
			monitor_query = monitor['query']
			# Check if metric is used in monitor query
			if metric in monitor_query:
				monitor_name = monitor['name']
				monitor_id = monitor['id']
				monitor_creator_email = monitor['creator']['email']
				monitor_creator_name = monitor['creator']['name']
			
				number_of_monitors_used_in += 1
				monitor_info_to_add = "{{monitor_name: {}, monitor_id: {}, monitor_creator: {}, creator_email: {}}}".format(monitor_name, monitor_id, monitor_creator_name, monitor_creator_email)
				# Check if there is a value in the monitor list, if so include a comma and space before new text
				if monitor_list != '':
					monitor_list += ', '
				monitor_list += monitor_info_to_add

		print('\n{} dashboard list:\n{}'.format(metric, monitor_list))
		return monitor_list, number_of_monitors_used_in

	# Method to get metric use in dashboards
	def get_metric_use_in_dashboards(self, metric):
		number_of_dashboards_used_in = 0
		dashboard_list = ''
		# Loop through each monitor to determin where the metric is used
		for dashboard in self.dd_account_object.dashboards['dashboards']:
			try:
				dashboard_widgets = dashboard['dashboard_json']['widgets']
				# Loop through each request to see if the metric is in the request query
				for widget in dashboard_widgets:
					requests = widget['definition']['requests']
					for request in requests:
						if metric in request['q']:
							dashboard_name = dashboard['title']
							dashboard_id = dashboard['id']
							dashboard_creator_handle = dashboard['author_handle']
							dashboard_creator_name = dashboard['dashboard_json']['author_name']
					
							number_of_dashboards_used_in += 1
							dashboard_info_to_add = "{{ dashboard_name: {}, dashboard_id: {}, dashboard_creator: {}, creator_handle: {}}}".format(dashboard_name, dashboard_id, dashboard_creator_handle, dashboard_creator_name)
							# Check if there is a value in the dashboard list, if so include a comma and space before new text
							if dashboard_list != '':
								dashboard_list += ', '
							dashboard_list += dashboard_info_to_add

			except Exception as e:
				pass
		print('{} dashboard list:\n{}\n\n'.format(metric, dashboard_list))
		return dashboard_list, number_of_dashboards_used_in