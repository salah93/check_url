'''This program checks a csv file that contains
a list of urls and checks if each url is active'''
from pandas import read_csv
from os.path import join
from invisibleroads_macros.disk import make_folder
import urllib2
import argparse


def check_links(table_path, url_col, target_folder):
    target_path = join(target_folder, 'check_urls.csv')
    links_table = read_csv(table_path)
   
    data = []
    # check each url's validity
    for url in links_table[url_col]:
        req = urllib2.Request(url)
        try: 
            urllib2.urlopen(req)
            data.append("")
        except urllib2.HTTPError as e:
            data.append(e.code)
    links_table['problems'] = data

    # TODO: fix this, add try/except, implement make_folder
    links_table.to_csv(target_path, index=False)

    # Required print statement for crosscompute
    print('check_urls_table_path = ' + target_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check csv file for broken links')
    parser.add_argument('--urls_table_path', metavar='N', required=True,
            type=str, help='.csv file to check')
    parser.add_argument('--url_column', type=str,required=True,
            metavar='COLUMNS', help='column name in csv sheet where urls are stored')
    parser.add_argument('--target_folder', metavar='FOLDER', type=make_folder)
    args = parser.parse_args()
    print(args.urls_table_path)

    check_links(args.urls_table_path, args.url_column, args.target_folder)


