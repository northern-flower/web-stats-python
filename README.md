# web-stats-python

TASK:

The website checker should perform the checks periodically and collect the HTTP
response time, status code returned, as well as optionally checking the returned
page contents for a regexp pattern that is expected to be found on the page.


Things to consider:

- is page content established for all the websites or can be 0 for 1 website and 1 for another (actually i considered that there could be different 'frequency' and 'downloaded_content' options for every website)
- how many websites to store (if many - consider distributed system and hash)
- for how long the stats should be kept (if for too long - consider distributed system as well, automatic archiving, etc)
- at which frequency to check whether the website is up or down (and not be blacklisted) - may be put it as a parameter

- how to test your code - if the website is down or not (the testing website can also be unexpectedly down or up)
- you may not have a right to access the website ..

Simple algorithm to use that comes immediately to my mind:
- ping to check if that website is alive (ideally 2 sources minimum should confirm that)
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
- status_code_returned - integer, probably with constraints (100-600)

website_content:
- website_id - integer
- timestamp - timestamp
- downloaded_content - BLOB


Ideas for tests:

- ping localhost
- ping google.com (but it can be down ...)
- ping non existing website/ url address for example - https://console.aiven.io/signup.html
- ping wrongly formatted website (....,com for example) - should return false or exception, 'your url is not well formatted'

Additional tests:

- that the values obtained are not abberant (for example <1mln seconds, or may be even not insert them if they are TOO big)
- how many pings are obtained in the timeframe
- test how database saving is working (i.e. for example how many records have been inserted during some time)
- test exceptions during database saving

