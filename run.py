"""
Check the status of each URL in a CSV file.
"""
import argparse
import csv
import requests


def check_links(urls):
    if len(urls) <= 0:
        return []
    # Check each url's validity
    url = urls[0]
    tail = urls[1:]
    try:
        req = requests.head(url)
        code = req.status_code
    except requests.HTTPError as e:
        code = e.code
    except requests.ConnectionError as e:
        code = 'connection error'
    return [(url, code)] + check_links(tail)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check CSV for broken links')
    parser.add_argument(
        'urls', metavar='URLS', nargs='+',
        help='CSV containing URLs')
    args = parser.parse_args()
    status_codes = check_links(args.urls)
    target_path = 'links.csv'
    with open(target_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["url", "status_code"])
        writer.writerows(status_codes)
    # Required print statement for crosscompute
    print('url_table_path = ' + target_path)
