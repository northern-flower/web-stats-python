#for connection class
import mysql.connector

#to print datetime to console
from datetime import datetime

#for unittesting
import unittest

class WebsiteChecker:
	
	#
	# constuctor with arguments
	#
	# websites - list of lists (website, frequency (in s), download_content (0 or 1))
	# [['google.com', 300, 0], ['localhost', 600, 0]]
	# connection - database connection
	
	def _init_(self, websites_list = [], connection):
		self.websites_list = websites_list.view()
		self.connection = connection
		self.cursor = self.connection.cursor()
		
	#TODO: create a separate class for SQL connection
	#mydb = mysql.connector.connect(
	#  host="localhost",
	#  user="yourusername",
	#  password="yourpassword",
	#  database="mydatabase"
	#)	
	
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
		return response
	
	#
	# get_curl_results
	#
	# return tuple (timestamp, http_response_time, status_code_returned, downloaded_content)
	# otherwise return something else
	# TODO: control Exception here, limit the time for it
	# TODO: refine curl (with options)
	def get_curl_results(url, download_content):
		if download_content == 1:
			response = os.system("curl " + url)
		else
			response = os.system("curl " + url)
		
		return (timestamp, http_response_time, status_code_returned, downloaded_content)
	
	#
	# retrieve_url_id_in_websites_list
	#
	# return URL_ID if url exists in URL FRONTIER (i.e. website list)
	# if it doesn't exist - create it and return URL_ID
	def retrieve_url_id_in_websites_list(url):
		
		# TODO: add exceptions
		sql_select = "SELECT website_id from websites where primary_url = %s"
		tuple = (url)
		self.cursor.execute(sql_select, tuple)
		records = self.cursor.fetchall()
		
		if self.cursor.rowcount == 0:
			# TODO: add exceptions
			# write new url_id into the database
			sql_insert = "INSERT INTO websites (primary_url) VALUES (%s)"
			tuple = (url)
			self.cursor.execute(sql_insert, tuple)
			self.connection.commit()
			
			url_id = self.connection.lastrowid
		elif self.cursor.rowcount != 1:
			print ("Problem while extracting id of url " + url + ": double insertion found")
		else:
			url_id = records[0]
			
		return url_id
		
	#
	# download_website_stats
	#
	# return true if it was succeful
	# otherwise return false
	def download_website_stats(url, download_content):
		
		if check_url_spelling(url) == null:
			print url + " does not pass the spelling check"
			return
		
		(timestamp, http_response_time, status_code_returned, downloaded_content) = get_curl_result(url)
		
		website_id = retrieve_url_id_in_websites_list(url)
		
		# TODO: add exceptions
		# write result into website_stats database
		
		sql_insert = "INSERT INTO website_stats (website_id, timestamp, http_response_time, status_code_returned) VALUES (%s, %s, %s, %s)"
		tuple = (website_id, timestamp, http_response_time, status_code_returned)
		self.cursor.execute(sql_insert, tuple)
		self.connection.commit()

		print("Stats for "+ url + " have been inserted at " + datetime.fromtimestamp(timestamp))
		
		# TODO: add exceptions
		# write result into website_content database
		if download_content:
		
			sql_insert = "INSERT INTO website_content (website_id, timestamp, downloaded_content) VALUES (%s, %s, %s)"
			tuple = (website_id, timestamp, downloaded_content)
			self.cursor.execute(sql_insert, tuple)
			self.connection.commit()

			print("Content for "+ url + " has been downloaded at " + datetime.fromtimestamp(timestamp))
			
		return true
	
	#
	# download_stats_for_multiple_websites
	#
	def download_stats_for_multiple_websites() {
		
		for website in websites_list:
			download_website_stats(website[0], website[2])
		

class TestWebChecker(unittest.TestCase):
	
	#
	# write tests here
	#
	
	def test_download_website_stats_google(self):
		websitechecker = WebsiteChecker(["google.com", 500, 0])
		self.assertEqual(websitechecker.download_website_stats(), true)
	
	def test_download_website_stats_localhost(self):
		websitechecker = WebsiteChecker(["localhost", 300, 1])
		self.assertEqual(websitechecker.download_website_stats(), true)
	
	# TODO: or may be this one should return exception
	def test_download_website_stats_broken_url_format(self):
		websitechecker = WebsiteChecker(["localhost.", 30, 0])
		self.assertEqual(websitechecker.download_website_stats(), false)
	
	def test_download_website_stats_broken_url(self):
		websitechecker = WebsiteChecker(["https://console.aiven.io/signup.html", 60, 1])
		self.assertEqual(websitechecker.download_website_stats(), true)
	
	#
	# verify that the entry has been inserted in the database
	#
	
	



