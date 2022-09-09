#for unittesting
import unittest

#for initialisation of connection
import sqlite3

#contains both WebsiteChecker and WebsiteCheckerUtils
import WebsiteChecker

class TestWebChecker(unittest.TestCase) {
	
	def _init_(self):
        connection = sqlite3.connect("our-database.db")
	
    #
    # url spelling true tests
    #
    #TODO: create a method to test those with parameters
    #TODO: create one object to test on different methods
    def check_url_spelling_true_simple_url():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("google.com"), true)
    
    def check_url_spelling_true_simple_url_with_www):
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("www.goOgle.com"), true)
    
    def check_url_spelling_true_simple_url_with_http():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("http://1oogle.com"), true)
    
    def check_url_spelling_true_simple_url_with_https():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("https://goog-e.com"), true)
    
    def check_url_spelling_true_simple_url_with_256_characters():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("ulhxbtoarnqshozsuulpcztqstl.com"), true)

    # url spelling false tests
    def check_url_spelling_false_simple_url_1():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("www.goOgle."), false)
    
    def check_url_spelling_false_simple_url_2():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("goOgle-com"), false)
    
    def check_url_spelling_false_url_with_3_points_in_it():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("goOgle.com.nl"), false)
    
    def check_url_spelling_false_url_with_special_character():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("goOgle#.com"), false)
    
    def check_url_spelling_false_simple_url_with_more_than_256_characters():
        wbutils = WebsiteChecker(connection)
        self.assertEqual(wbutils.check_url_spelling("xpuhcxryawkyuxxztskjkuupecblwxal.com"), false)
    
    #
    # check that ping is taking less time than the frequency ???
    # ...
    #
    
    #
    # TODO: think about if i really need to test curl results ...
    #
    
    # TODO: check the following tests:
    
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

    
    #TODO: agggregation tests
    # ...


#
# other test ideas
#
# verify if there is an infinite loop
# how many insertions in the database have been made during a certain time
#

    
    
    
    
    
}


#
#TODO: incorporate this
#


from mock_db import MockDB
from mock import patch

#TODO: may be handle exceptions ???
#TODO: probably need to be initialised to know in which database to write
import utils

#for initialisation of connection
import sqlite3

class TestWebCheckerDatabase(MockDB):
	
    def _init_(self):
		connection = sqlite3.connect("our-database.db")
    
    def test_db_websites_insert(self):
		with self.mock_db_config:
			self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), True)
	
	def test_db_websites_delete(self):
		with self.mock_db_config:
			self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), True)
	
    def test_db_websites_insert_and_delete(self):
        with self.mock_db_config:
			self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), True)
            
			self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), False)
			
			self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), True)
            
			self.assertEqual(utils.db_write("""DELETE FROM `websites` (`primary_url`) VALUES
                            ('https://test.com/')"""), False)
			
			
	# TODO: there will be similar tests for 'website_stats' and 'website_content'
	# TODO: for 'website_content' it would make sense to verify timeout while writing to the database			
			
			
