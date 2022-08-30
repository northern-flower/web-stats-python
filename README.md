# web-stats-python
//
// The website checker should perform the checks periodically and collect the HTTP
// response time, status code returned, as well as optionally checking the returned
// page contents for a regexp pattern that is expected to be found on the page.


Q: is page content established for all the websites or can be 0 for 1 website and 1 for another

//
//
// Things to consider:
//
// - how many websites to store (if many - consider distributed system and hash)
// - for how long the stats should be kept (if for too long - consider distributed system as well, automatic archiving, etc)
// - at which frequency to check whether the website is up or down (and not be blacklisted) - may be put it as a parameter
//
// - how to test your code - if the website is down or not (the testing website can also be unexpectedly down or up)
// - you may not have a right to access the websiite ..
//
// Simple algorithm to use:
// - ping to check if that website is alive (ideally 2 sources minimum should confirm that i would say)
// Ping is fast operation. Optionally we would like to get the content of the website too but it would take more time.
// - curl the stats and (optionally) the content
//

website:
- id - integer
- primary_url - varchar(256) - limit url length to avoid crawler trap

website_stats:
- website_id - integer
- timestamp - timestamp
- HTTP response time (ms) - integer
- status code returned - integer, probably with constraints (404, 423, ... <1000?)
- (optionally checking) the returned page contents for a regexp pattern that is expected to be found on the page - BLOB - this is huge (may be put in another database indeed)

website_content:
- website_id - integer
- timestamp - timestamp
- downloaded_page (content) - BLOB

//
//
// ping time/interval - may be do it as a variable, read what is reasonable
//
//
// https://phoenixnap.com/kb/linux-ping-command-examples
//
// How to Limit the Number of Pings:
// ping -c 2 google.com
//
// Time limit for ping:
// ping -w 25 google.com
//
// Add Timestamp Before Each Line in ping Output
// ping -D google.com
// 
//
// test:
// ping localhost
// ping google.com (but it can be down ...)
// ping non existing website
// ping wrongly formatted website (....,com for example) - should return exception, 'your url is not well formatted'
//
//
// additional tests:
// - that the values obtained are not abberant (for example <1mln msc, or may be even not insert them if they are TOO big)
// - how many pings are obtained in the timeframe
//
//




