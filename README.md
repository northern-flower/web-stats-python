# web-stats-python

DISCLAIMER:

Please note that this repository is for illustration purpose only and doesn not imply that the code compiles.

TASK:

The website checker should perform the checks periodically and collect the HTTP
response time, status code returned, as well as optionally checking the returned
page contents for a regexp pattern that is expected to be found on the page.


Limitations:

- too many websites to check would mean a distributed system would be needed, with hash table managing the keys for their access
- too frequent checks could black list the server from which we are performing them

Database structure:

websites:
- website_id - integer, autoincrement
- primary_url - varchar(256) - limit url length to avoid crawler trap

website_stats:
- id, integer, autoincrement
- website_id - integer, FK to websites->website_id
- timestamp - timestamp
- http_response_time (ms) - integer
- status_code_returned - integer, probably with constraints (100-600)

website_content:
- id, integer, autoincrement
- website_id - integer, FK to websites->website_id
- timestamp - timestamp
- downloaded_content - BLOB


Ideas for tests:

- ping localhost
- ping google.com (but it can be down ...)
- ping website with a known (not 200 status code), for example - https://console.aiven.io/signup.html (404)
- ping non existing website with correct url address for example - https://digg.com/2019/WHAT-earth-WOULD-look-like-if-all-the-oceans-were-drained-visualized (404)
- ping wrongly formatted website (....,com for example) - should return false or exception, 'your url is not well formatted'

Additional tests:

- that the values obtained are not abberant (for example <1mln seconds, or may be even not insert them if they are TOO big)
- how many pings are obtained in the timeframe
- test how database saving is working (i.e. for example how many records have been inserted during some time)
- test exceptions during database saving

