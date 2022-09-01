# web-stats-python

TASK:

The website checker should perform the checks periodically and collect the HTTP
response time, status code returned, as well as optionally checking the returned
page contents for a regexp pattern that is expected to be found on the page.


Things to consider:


Q: is page content established for all the websites or can be 0 for 1 website and 1 for another (actually i considered that there could be different 'frequency' and 'downloaded_content' options for every website)
- how many websites to store (if many - consider distributed system and hash)
- for how long the stats should be kept (if for too long - consider distributed system as well, automatic archiving, etc)
- at which frequency to check whether the website is up or down (and not be blacklisted) - may be put it as a parameter

- how to test your code - if the website is down or not (the testing website can also be unexpectedly down or up)
- you may not have a right to access the websiite ..

Simple algorithm to use:
- ping to check if that website is alive (ideally 2 sources minimum should confirm that i would say)
Ping is fast operation. Optionally we would like to get the content of the website too but it would take more time.
- curl the stats and (optionally) the content



Database structure:

websites:
- website_id - integer, autoincrement
- primary_url - varchar(256) - limit url length to avoid crawler trap

website_stats:
- website_id - integer
- timestamp - timestamp
- http_response_time (ms) - integer
- status_code_returned - integer, probably with constraints (404, 423, ... <1000?)

website_content:
- website_id - integer
- timestamp - timestamp
- downloaded_content - BLOB


