#for unittesting
import unittest

#for initialisation of connection
import sqlite3

#contains both WebsiteChecker and WebsiteCheckerUtils
import WebsiteChecker

#constants
PING_PERFORMANCE = 1000

class TestWebChecker(unittest.TestCase) {
	
	def setUp(self):
        connection = sqlite3.connect("our-database.db")
        wbutils = WebsiteChecker(connection)
	
	#
    # url spelling true tests
    #
    
    #TOCONSIDER: consider using pytest instead of unittest (check the advantages)
    def test_url_spelling_true_simple_url():
        self.assertEqual(wbutils.check_url_spelling("google.com"), true, "google.com should be a valid url")
    
    def test_url_spelling_true_simple_url_with_www():
        self.assertEqual(wbutils.check_url_spelling("www.goOgle.de"), true, "www.goOgle.de should be a valid url")
    
    def test_url_spelling_true_simple_url_with_http():
        self.assertEqual(wbutils.check_url_spelling("http://1oogle.se"), true, "http://1oogle.se should be a valid url")
    
    def test_url_spelling_true_simple_url_with_https():
        self.assertEqual(wbutils.check_url_spelling("https://goog-e.fr"), true, "https://goog-e.fr should be a valid url")
    
    def test_url_spelling_true_simple_url_with_256_characters():
        self.assertEqual(wbutils.check_url_spelling("ulhxbtoarnqshozsuulpcztqstle.nl"), true, "ulhxbtoarnqshozsuulpcztqstle.nl should be a valid url")

    # url spelling false tests
    def test_url_spelling_false_simple_url_1():
        self.assertEqual(wbutils.check_url_spelling("www.goOgle."), false, "www.goOgle. should be invalid url")
    
    def test_url_spelling_false_simple_url_2():
        self.assertEqual(wbutils.check_url_spelling("goOgle-com"), false, "goOgle-com should be invalid url")
    
    def test_url_spelling_false_url_with_3_points_in_it():
        self.assertEqual(wbutils.check_url_spelling("goOgle.com.nl"), false, "goOgle.com.nl should be invalid url")
    
    def test_url_spelling_false_url_with_special_character():
        self.assertEqual(wbutils.check_url_spelling("goOgle#.com"), false, "goOgle#.com should be invalid url")
    
    def test_url_spelling_false_simple_url_with_more_than_256_characters():
        self.assertEqual(wbutils.check_url_spelling("xpuhcxryawkyuxxztskjkuupecblwxal.com"), false, "xpuhcxryawkyuxxztskjkuupecblwxal.com contains more than 256 characters and thus should be invalid url")
    
    #
    # Since we are using the library for ping check
    # there are already a lot of tests there - 
    # we could use them instead of writing our own
    #
    
    #TOIMPROVE:
    #get_curl_results
    #retrieve_url_id_in_websites_list(url)
    #test expected raises/exceptions - create constants for them
    
    #integration tests (or is it end to end)
    def test_download_website_stats_google(self):
		websitechecker = WebsiteChecker(["google.com", 500, 0], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)
        #check ping < 1000 for example
        #check the last line in the database
        #check that the content is not downloaded
        #check the log file
	
	def test_download_website_stats_localhost(self):
		websitechecker = WebsiteChecker(["localhost", 300, 1], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)
        #check ping < 1000 for example
        #check the last line in the database
        #check that the content is not downloaded
        #check the log file
	
	def test_download_website_stats_broken_url_format(self):
		websitechecker = WebsiteChecker(["localhost.", 30, 0], connection)
		self.assertEqual(websitechecker.download_website_stats(), false)
        #check ping < 1000 for example
        #check the last line in the database
        #check that the content is not downloaded
        #check the log file
	
	def test_download_website_stats_broken_url(self):
		websitechecker = WebsiteChecker(["https://console.aiven.io/signup.html", 60, 1], connection)
		self.assertEqual(websitechecker.download_website_stats(), true)
        #check ping < 1000 for example
        #check the last line in the database
        #check that the content is not downloaded
        #check the log file
    
    # verify that logger is producing something (no infinite loop)
    # verify that the number of entrance into the database is an expected number

if __name__ == '__main__':
    unittest.main()

#
#TOIMRPOVE: incorporate this into the previous tests
#

from mock_db import MockDB
from mock import patch
import utils
import time

#for initialisation of connection
import sqlite3

#constants
BLOB_INSERT_PERFORMANCE = 1000
BLOB_DELETE_PERFORMANCE = 1000

class TestWebCheckerDatabase(MockDB):
	
    def _init_(self):
		connection = sqlite3.connect("our-database.db")
    
    # test insert and delete for 'websites' table
    def test_db_websites_insert_and_delete(self):
        with self.mock_db_config:
			self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                            (`https://test.com/`)"""), True, """First time insert of https://test.com/ into `websites` table should work""")
            
            self.assertEqual(utils.db_write("""INSERT INTO `websites` (`primary_url`) VALUES
                            (`https://test.com/`)"""), False, """Second time insert of https://test.com/ into `websites` table should NOT work""")
			
			self.assertEqual(utils.db_write("""DELETE FROM `websites` where `primary_url` = `https://test.com/`"""), True, """First time delete of https://test.com/ from `websites` table should work""")
            
            self.assertEqual(utils.db_write("""DELETE FROM `websites` where `primary_url` = `https://test.com/`"""), False, """Second time delete of https://test.com/ from `websites` table should NOT work""")
	
    # test insert and delete for 'website_stats' table
    def test_db_website_stats_insert_and_delete(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_write("""INSERT INTO `website_stats` (`website_id`, `timestamp`, `http_response_time`, `status_code_returned`) VALUES
                            (1, 1594819641.9622827, 32, 0)"""), True, """First time insert of website_id = 1 (for timestamp in the past) into `website_stats` table should work""")
            
			self.assertEqual(utils.db_write("""INSERT INTO `website_stats` (`website_id`, `timestamp`, `http_response_time`, `status_code_returned`) VALUES
                            (1, 1594819641.9622827, 545, 23)"""), False, """Second insertion for `website_stats` table should not be possible for the same `website_id` and `timestamp`""")
			
			self.assertEqual(utils.db_write("""DELETE FROM `website_stats` where website_id = 1 and timestamp = 1594819641.9622827""", True, """First time delete of website_id = 1 (in the past) from `website_stats` table should work""")
            
			self.assertEqual(utils.db_write("""DELETE FROM `website_stats` where website_id = 1 and timestamp = 1594819641.9622827""", False, """Second time delete of website_id = 1 (in the past) from `website_stats` table should NOT work""")
    
    # test insert and delete for 'website_content' table
	# additional tests for insertion performace of the table (as it contains BLOB)
	def test_db_website_content_insert_and_delete(self):
        with self.mock_db_config:
			
            self.assertEqual(utils.db_write("""INSERT INTO `website_content` (`website_id`, `timestamp`, `downloaded_content`) VALUES
                            (1, 1662890978.4920807, '<html></html>')"""), True, """First time insert of website_id = 1 (for timestamp in the past) into `website_content` table should work""")
            
			self.assertEqual(utils.db_write("""INSERT INTO `website_content` (`website_id`, `timestamp`, `downloaded_content`) VALUES
                            (1, 1662890978.4920807, '')"""), False, """Second insertion for `website_content` table should not be possible for the same `website_id` and `timestamp`""")
			
			self.assertEqual(utils.db_write("""DELETE FROM `website_content` where website_id = 1 and timestamp = 1662890978.4920807""", True, """First time delete of website_id = 1 (in the past) from `website_content` table should work""")
            
			self.assertEqual(utils.db_write("""DELETE FROM `website_content` where website_id = 1 and timestamp = 1662890978.4920807""", False, """Second time delete of website_id = 1 (in the past) from `website_content` table should NOT work""")
            
            #read a very large html from a file
            f = open("very_large_html.html", "r")
            
            # BLOB insert performance
            start = time.time()
            
            self.assertEqual(utils.db_write("""INSERT INTO `website_content` (`website_id`, `timestamp`, `downloaded_content`) VALUES
                            (1, 1662890978.4920807, """ + f +""")"""), True, """(BLOB) First time insert of website_id = 1 (for timestamp in the past) into `website_content` table should work""" )
            
            end = time.time()
			
            self.assertEqual(end-start < BLOB_INSERT_PERFORMANCE, true, "Insert of BIG BLOB into `website_content` table should be possible under < " + BLOB_INSERT_PERFORMANCE + "ms")
            
            # BLOB delete performance
            start = time.time()
            
            self.assertEqual(utils.db_write("""DELETE FROM `website_content` where website_id = 1 and timestamp = 1662890978.4920807""", True, """(BLOB) First time delete of website_id = 1 (in the past) from `website_content` table should work""")
            
            end = time.time()
			
            self.assertEqual(end-start < BLOB_DELETE_PERFORMANCE, true, "")
            
