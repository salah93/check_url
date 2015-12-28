"""
Check the status of each URL in a CSV file.
"""
import argparse
import urllib2
from invisibleroads_macros.disk import make_folder
from invisibleroads_macros.log import format_path
from os.path import join
from pandas import read_csv


def check_links(target_folder, table_path, url_column):
    target_path = join(target_folder, 'links.csv')
    links_table = read_csv(table_path)

    status_codes = []
    # Check each url's validity
    for url in links_table[url_column]:
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)
            status_codes.append(res.code)
        except urllib2.HTTPError as e:
            status_codes.append(e.code)
    links_table['Status Codes'] = status_codes

    # TODO: Fix this, add try/except, implement make_folder
    links_table.to_csv(target_path, index=False)

    # Required print statement for crosscompute
    print('url_table_path = ' + format_path(target_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check CSV for broken links')
    parser.add_argument(
        '--target_folder', metavar='FOLDER', type=make_folder)
    parser.add_argument(
        '--url_table_path', metavar='PATH', required=True,
        help='CSV containing URLs')
    parser.add_argument(
        '--url_column', metavar='COLUMN', required=True,
        help='column in CSV containing URLs')
    args = parser.parse_args()
    check_links(args.target_folder, args.url_table_path, args.url_column)
