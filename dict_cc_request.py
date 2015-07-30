import sys
import urllib2
import re
from prettytable import PrettyTable

def _printUsage():
    print "usage: dict_cc_request.py <input_language> <output_language> <search_keyword>"
    print "       NOTE: The <search_keyword> can be more than one word. In this case you "
    print "             MUST use quotes to get it used as you want"

# Help text requested
if str(sys.argv[0]) == 'help' or str(sys.argv[0]) == '--help':
        _printUsage()
        exit(0)

# Check if enough arguments available
if len(sys.argv) < 3:
    print "Wrong usage."
    _printUsage()
    exit(0)

# Assign input arguments
arg_input_language = sys.argv[1]
arg_output_language = sys.argv[2]
arg_search_keyword = sys.argv[3]

# Create subdomain from in+out language
req_subdomain = arg_input_language + arg_output_language

req = urllib2.Request(
    "http://" + req_subdomain + ".dict.cc/?s=" + arg_search_keyword,
    None, 
    {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'}
)

response_body = urllib2.urlopen(req).read()

input_list = []
output_list = []

javascript_list_pattern = "\"[^,]+\""

for line in response_body.split("\n"):
    if "var c1Arr" in line:
        input_list = re.findall(javascript_list_pattern, line)

    elif "var c2Arr" in line:
        output_list = re.findall(javascript_list_pattern, line)

if len(input_list) == 0:
    print
    print "Sorry. Nothing found."
    print
    exit(0)

table_result = PrettyTable()
table_result.header = False
table_result.border = False
table_result.align = "l"
for i in range(0, len(input_list)):
    table_result.add_row([input_list[i], output_list[i]])

print "Result: "
print table_result
