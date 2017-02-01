"""
Check the status of each URL in a CSV file.
"""
import argparse
import csv
from os.path import join

import requests


def check_links(urls):
    status_codes = []
    for url in urls:
        # Check each url's validity
        try:
            req = requests.head(url)
            code = req.status_code
        except requests.HTTPError as e:
            code = e.code
        except requests.ConnectionError as e:
            code = 'no such site'
        status_codes.append((url, code))
    return sorted(status_codes, key=lambda x: x[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                 description='Check CSV for broken links')
    parser.add_argument('--target_folder', metavar='FOLDER')
    parser.add_argument('--urls_path', metavar='PATH', required=True,
                        help='file containing list of URLs')
    args = parser.parse_args()
    with open(args.urls_path) as f:
        urls = [line.strip() for line in f.readlines()]
    status_codes = check_links(urls)
    target_path = join(args.target_folder, 'links.csv')
    with open(target_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["url", "status_code"])
        writer.writerows(status_codes)
    # Required print statement for crosscompute
    print('url_table_path = ' + target_path)
