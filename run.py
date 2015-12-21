'''This program checks a csv file that contains
a list of urls and checks if each url is active'''
import csv
from pandas import DataFrame, read_csv
from os.path import join
from os import mkdir
from invisibleroads_macros.disk import make_folder
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

def check_links(links_table, url_col, target_folder):
    target_path = join(target_folder,'check_urls.csv')
    
    data = []
    for url in links_table[url_col]:
        req = urllib2.Request(url)
        try: 
            urllib2.urlopen(req)
            data.append("")
        except urllib2.HTTPError as e:
            data.append(str(e.code) + "-" + error_codes.get(e.code)[0])
    links_table['problems'] = data

    try:
        links_table.to_csv(target_path, index=False)
    except IOError:
        mkdir('./results')
        links_table.to_csv(target_path, index=False)
    print 'check_urls_table_path = ' + target_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check csv file for broken links')
    parser.add_argument('--urls_table_path', metavar='N', required=True,
            type=str, help='files to check')
    parser.add_argument('--url_column', type=str,required=True,
            metavar='COLUMNS', help='column name in csv sheet')
    parser.add_argument('--target_folder', metavar='FOLDER', type=make_folder)
    args = parser.parse_args()
    print(args.urls_table_path)
    urls_table = read_csv(args.urls_table_path)
    check_links(urls_table, args.url_column, args.target_folder)
    
