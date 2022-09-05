#for unittesting
import unittest

#import class to test
import WebsiteChecker

#TODO: to merge TestWebsiteChecker and TestWebsiteCheckerDatabase

class TestWebsiteChecker(unittest.TestCase) {
	
	def _init_(self):
		#TODO: initialise connection
	
	def test_download_website_stats_google(self):
		websitechecker = WebsiteChecker(["google.com", 500, 0], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)
	
	def test_download_website_stats_localhost(self):
		websitechecker = WebsiteChecker(["localhost", 300, 1], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)
	
	# TODO: or may be this one should return exception
	def test_download_website_stats_broken_url_format(self):
		websitechecker = WebsiteChecker(["localhost.", 30, 0], connection)
		self.assertEqual(websitechecker.download_website_stats(), false)
	
	def test_download_website_stats_broken_url(self):
		websitechecker = WebsiteChecker(["https://console.aiven.io/signup.html", 60, 1], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)

}


#
# verify that the entry has been inserted in the database
#
#https://medium.com/swlh/python-testing-with-a-mock-database-sql-68f676562461


from mock_db import MockDB
from mock import patch
import utils

class TestWebsiteCheckerDatabase(MockDB):
	
    def test_db_websites_insert(self):
	with self.mock_db_config:
		self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                	('https://github.com/')"""), True)
	
    def test_db_websites_delete(self):
	with self.mock_db_config:
		self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                	('https://github.com/')"""), True)
	
    def test_db_websites_insert_and_delete(self):
        with self.mock_db_config:
		self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                	('https://github.com/')"""), True)
            
		self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                        ('https://github.com/')"""), False)
			
		self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                        ('https://github.com/')"""), True)
            
		self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                	('https://github.com/')"""), False)
			
			
	# TODO: there will be similar tests for 'website_stats' and 'website_content'
	# TODO: for 'website_content' it would make sense to verify timeout while writing to the database			
			
			
#
# other test ideas
#
# verify if there is an infinite loop
# how many insertions in the database have been made during a certain time
#
