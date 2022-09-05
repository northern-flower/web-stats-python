#for connection class
import mysql.connector

#to print datetime to console
from datetime import datetime

#to use ping response automatically
from ping3 import ping

#for logging
import logging

class WebsiteChecker:
	
	#
	# constuctor with arguments
	#
	# incoming parameters:
	# websites - list of lists (website, frequency (in ms), download_content (0 or 1))
	# for example - [['google.com', 300, 0], ['localhost', 600, 0]]
	# connection - database connection
	#
	# logger field will be created in the constructor
	# in this exercise for simplicity we would consider that class Connection already exists
	def _init_(self, websites_list = [][], connection):
		self.websites_list = websites_list.view()
		self.connection = connection
		self.cursor = self.connection.cursor()
		self.logger = logging.getLogger()
	
	#
	# check_url_spelling
	#
	# incoming parameters:
	# url - website url, string
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
	# incoming parameters:
	# url - website url, string
	# frequency - frequency of downloading, in ms, needed here for timeout configuring
	#
	# return 'http_response_time' if website is alive
	# otherwise return 'None' (timeout)
	# https://github.com/kyan001/ping3
	def check_ping(url, frequency):
		
		# we may assume that timeout can be equal to frequency
		# because if we can't obtain the response within frequency parameter
		# then we should not save it
		http_response_time = ping(url, unit='ms', timeout=frequency*1000)
		return http_response_time
	
	#
	# get_curl_results
	#
	# incoming parameters:
	# url - website url, string
	# frequency - frequency of downloading, in ms, needed here for timeout configuring
	# download_content - option to say if the content of the url should be downloaded or not (can be 0 or 1)
	#
	# return tuple (timestamp, status_code_returned, downloaded_content)
	def get_curl_results(url, frequency, download_content):
		
		timestamp = datetime.datetime.now().timestamp()
		
		# TODO: make timestamp, status_code_returned and download_content in one call
		status_code_returned = os.system("curl -I --connect-timeout "+ frequency + " --silent " + url + " | head -n 1 | awk -F' ' '{print $2}'")
		
		if download_content == 1:
			downloaded_content = os.system("curl " + url)
		
		return (timestamp, status_code_returned, downloaded_content)
	
	#
	# retrieve_url_id_in_websites_list
	#
	# incoming parameters:
	# url - website url, string
	#
	# return URL_ID if url exists in URL FRONTIER (i.e. website list)
	# if it doesn't exist - create it and return URL_ID
	def retrieve_url_id_in_websites_list(url):
		
		# find if url already exists in the database of urls
		# TODO: add exceptions
		sql_select = "SELECT website_id from websites where primary_url = %s"
		tuple = (url)
		self.cursor.execute(sql_select, tuple)
		records = self.cursor.fetchall()
		
		if self.cursor.rowcount == 0:
			# write new url_id into the database
			# TODO: add exceptions
			sql_insert = "INSERT INTO websites (primary_url) VALUES (%s)"
			tuple = (url)
			self.cursor.execute(sql_insert, tuple)
			self.connection.commit()
			
			url_id = self.connection.lastrowid
		elif self.cursor.rowcount != 1:
			logger.error("Problem while extracting id of url " + url + ": double insertion found")
		else:
			url_id = records[0]
			
		return url_id
		
	#
	# download_website_stats
	#
	# incoming parameters:
	# url - website url, string
	# frequency - frequency of downloading, in ms, needed here for timeout configuring
	# download_content - option to say if the content of the url should be downloaded or not (can be 0 or 1)
	#
	# return TRUE if it was succesful
	# otherwise return FALSE
	def download_website_stats(url, frequency, download_content):
		
		if check_url_spelling(url) == null:
			logger.warning(url + " does not pass the spelling check")
			return false
		
		http_response_time = check_ping(url, frequency)
		
		(timestamp, status_code_returned, downloaded_content) = get_curl_result(url)
		
		website_id = retrieve_url_id_in_websites_list(url)
		
		# write result into website_stats database
		# TODO: add exceptions
		sql_insert = "INSERT INTO website_stats (website_id, timestamp, http_response_time, status_code_returned) VALUES (%s, %s, %s, %s)"
		tuple = (website_id, timestamp, http_response_time, status_code_returned)
		self.cursor.execute(sql_insert, tuple)
		self.connection.commit()

		logger.info("Stats for "+ url + " have been inserted at " + datetime.fromtimestamp(timestamp))
		
		# write result into website_content database
		# TODO: add exceptions
		if download_content:
		
			sql_insert = "INSERT INTO website_content (website_id, timestamp, downloaded_content) VALUES (%s, %s, %s)"
			tuple = (website_id, timestamp, downloaded_content)
			self.cursor.execute(sql_insert, tuple)
			self.connection.commit()

			logger.info("Content for "+ url + " has been downloaded at " + datetime.fromtimestamp(timestamp))
			
		return true
	
	#
	# download_stats_for_multiple_websites
	#
	def download_stats_for_multiple_websites():
		
		for website in self.websites_list:
			download_website_stats(website[0], website[1], website[2])

	#
	# check website status periodically
	#
	def download_website_stats_periodically(url, frequency, download_content):
	
		while True:
			try:
				time.sleep(frequency)
				download_website_stats(url, frequency, download_content)
			except Exception as e:
				logger.error('*download_website_stats_periodically* failed %s ' % (str(e)))
			pass
	
	# def download_website_stats_periodically_start(url, frequency, download_content)
	# TODO: ADD corresponding crontab for this url based on frequency
	
	# def download_website_stats_periodically_update(url, frequency, download_content)
	# TODO: UPDATE corresponding crontab for this url based on frequency
	
	# def download_website_stats_periodically_stop(url, frequency, download_content)
	# TODO: REMOVE corresponding crontab for this url based on frequency

#
# other thoughts
# later i have found ideas about concurrent reading of the status of website
# i guess it would make sense for a high frequency reading
#


