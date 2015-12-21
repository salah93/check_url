'''This program checks a csv file that contains
a list of urls and checks if each url is active'''
import csv
from os.path import join
from os import mkdir
import urllib2
import argparse


error_codes = {
    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

def check_links(links, url_col_no, problem_col_no): 
    target_path = join('./results/','check_urls.csv')
    
    data = []
    with open(links, 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            url = row[url_col_no]
            if 'http' in url:
                req = urllib2.Request(url)
                try: urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    row[problem_col_no] = str(e.code) + "-" + error_codes.get(e.code)[0]
            data.append(row)


    try:
        f = open(target_path, 'w+')

    except IOError:
        mkdir('./results')
        f = open(target_path, 'w+')

    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
    f.close()
    print{
            'check_urls_table_path': target_path
    }

if __name__ == "__main__":
    #file name
    links_file = 'links-list.csv'
    parser = argparse.ArgumentParser(description='Check csv file for broken links')
    parser.add_argument('--urls_table_path', metavar='N', required=True,
            type=str, help='files to check')
    parser.add_argument('--colno', metavar='c', type=int,nargs='?', default=0,
                            help='column number in csv sheet, starting from index 0')
    parser.add_argument('--colno_problem', metavar='r', type=int, nargs='?',default=1,
                            help='column number of where problems of links would be reported in csv sheet, starting from index 0')
    args = parser.parse_args()
    print(args.urls_table_path)
    check_links(args.urls_table_path,url_col_no=args.colno, problem_col_no=args.colno_problem)

