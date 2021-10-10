The Gemini Platform team values everyone’s ability to solve problems programmatically through code, with an understanding of how to deliver work to a defined specification. This is a short programming challenge to assess your technical ability to implement the sort of tooling you might be asked to create here at Gemini. This task can be done by yourself on your own time, or in an interview setting working through your thinking in-house, either directly in code, or in pseudo-code. If you would like to work through this in an interview please reach out to your recruiter. This is not used as a gate, but as an assessment of technical ability, and to shape further conversations.

Writing in a language of your choice (python is recommended, but not required), and in an expected 2-4 hours, implement a series of monitoring alerts using our public API - https://docs.gemini.com/rest-api. Do not go beyond 4 hours. If you hit the 4 hour mark, just note down what you have left to do, and how you would accomplish it. The 4 hour limit is to protect your own personal time, which I don't want to take too much of.

Imagine that your script will be run periodically by a monitoring tool, being called directly, generating alerts as output that will feed into an alerting mechanism (eg. Slack, PagerDuty, etc). You do not need to implement this alert mechanism - just log the alert (written to stdout) and its details per the spec below. Implementing the alert inputs as CLI args is nice to have, but not required. Values can be hardcoded to meet the time limit.

For each of the symbols (ie. currency pairs) that Gemini trades you must generate an alert for one (or more) of the following conditions -

Price Deviation - Generate an alert if the current price is more than one standard deviation from the 24hr average

Price Change - Generate an alert if the current price has changed in the past 24 hours by more than X% from the price at the start of the period

Volume Deviation - Generate an alert if the quantity of the most recent trade is more than X% of the total 24hr volume in the symbol

You only need to implement one of the above, but doing all three is fine, given time.

Delivering a more correct, but less complete answer is preferable - I'd rather you do a great job implementing one check and show off your skills and ability, than struggle to do all three.

The alert should be a log line that highlights -

Log level - (ie. INFO for regular output. ERROR if the alert condition is met)

timestamp

symbol

type of alert (ie. price deviation, high volume, etc)

Submission

Submit your code as a link to your git repo (eg. github, gitlab, etc with appropriate permissions shared to us), and a README text file in the repo containing:

Any necessary instructions for running your script

Any dependencies that need to be met

What you would do next to further improve it

Other interesting checks you might implement to alert on market behaviour

Your approach to solving the task, and any issues you faced with implementation

The time it took you to write it

Scoring

Your submission will be assessed by:

Running the code, and verifying it executes as expected

Scoring the code with pylint, shellcheck or an equivalent linter

Reviewed for code style

Reviewing your attached documentation

Thank you, and please reach out through your Gemini recruiter if you have any questions.

Appendix:

A sample run of the alert script might look something like:


$ ./apiAlerts.py -h
2019-08-05 16:10:51,143 - AlertingTool - INFO - Parsing args
usage: apiAlerts.py [-h] [-c CURRENCY] [-t {pricedev,pricechange,voldev,ALL}]
                    [-d DEVIATION]
 
Runs checks on API
 
optional arguments:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
                        The currency trading pair, or ALL
  -t {pricedev,pricechange,voldev,ALL}, --type {pricedev,pricechange,voldev,ALL}
                        The type of check to run, or ALL
  -d DEVIATION, --deviation DEVIATION
                        percentage threshold for deviation ch
$ ./apiAlerts.py -c zecbch -t pricedev
2019-08-05 16:09:49,788 - AlertingTool - INFO - Parsing args
2019-08-05 16:09:49,789 - AlertingTool - INFO - Running check: pricedev
2019-08-05 16:09:49,789 - AlertingTool - INFO - Using deviation threshold: 5
2019-08-05 16:09:49,789 - AlertingTool - INFO - Running checks on currency pair: zecbch
2019-08-05 16:09:49,789 - AlertingTool - INFO - Getting symbols API Data
2019-08-05 16:09:49,843 - AlertingTool - INFO - Running checks
2019-08-05 16:09:49,843 - AlertingTool - INFO - *** Running priceDev check on: zecbch
2019-08-05 16:09:49,843 - AlertingTool - INFO - Getting Price API Data for: zecbch
2019-08-05 16:09:49,858 - AlertingTool - INFO - Last Price: 0.1312
2019-08-05 16:09:49,858 - AlertingTool - INFO - Standard Deviation: 0.0220285943126
2019-08-05 16:09:49,858 - AlertingTool - INFO - Average: 0.1732375
2019-08-05 16:09:49,858 - AlertingTool - INFO - Price diff: 0.0420375
2019-08-05 16:09:49,859 - AlertingTool - ERROR - ******   Price Deviation