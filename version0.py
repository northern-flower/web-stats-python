class WebsiteChecker:

	#public $frequency;
	#public $websites;
	#public $download_content;
	
	#may be create array of tuples (website, download_content)
	
	def _init_(self, frequency = 300, websites = [], download_content = []):
		self.frequency = frequency #in seconds, let's say every 5 minutes by default
		self.websites = websites.view()
		self.download_content = download_content.view()
	
	#
	# check_url_spelling
	#
	# return URL if it is well formatted
	# return NULL if not
	# https://uibakery.io/regex-library/url-regex-python - for url regex
	def check_url_spelling(url):
		url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
		return re.match(url_pattern, url)
	
	#
	# check_ping
	#
	# return 0 if website is alive
	# otherwise return something else
	# TODO: control Exception here, limit the time for it
	# https://stackoverflow.com/questions/26468640/python-function-to-test-ping
	def check_ping(url):
		response = os.system("ping -c 1 " + url)
		# TODO: check if there are Exceptions to raise about it, for example if ping takes forever
		return response
	
	#
	# retrieve_url_id_in_websites_list
	#
	# return URL_ID if url exists in URL FRONTIER (i.e. website list)
	# if it doesn't exist - create it and return URL_ID
	def retrieve_url_id_in_websites_list(url):
		...
		...
		...
		return url_id
		
	#
	# download_website_stats
	#
	# return true if it was succeful
	# otherwise return false
	def download_website_stats():
		...
		...
		
		...
		return true
	
	#
	# download_website_stats_start
	#
	def download_website_stats_start(url, when, database, download_content) {
		
		# control the quality of website_url
		# if it is well formatted etc
		# also solve the ambiguity like 'google.com', 'https://google.com' etc
		if check_url_spelling(url):
			url_id = retrieve_url_id_in_websites_list(url)
		
		#if write to database - check ping first ...
		
		// optionally write the content
		if ($download_content && $ping == 'ok') {
		
			// write content to 'website_content' database
		}
	
	}
	
	function download_website_stats_stop(url, ):
		# TODO: retrieve the process and kill it
	
	function download_website_stats_durint_time(url, frequency, duration):
	
	
	function getWebsiteStatsOfMultiple(string[] $websites):
	
	//////////////////////
	// write tests here //
	//////////////////////
	
	...
	...
	...

}



