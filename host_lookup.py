#!/usr/bin/env python

import sys
import csv
import urlparse

""" An adapter that takes CSV as input, performs a lookup to map URLS
    to service names, then returns the CSV results

    Bidrectional mapping is always required when using an external lookup as an
    'automatic' lookup: one configured to be used without explicit reference in
    a search.
"""


# Given a url, find a service name
def lookup(url):
    try:
        hostname = mapHostnameUrl(url)
        return hostname
    except:
        return url

# Given an filetype, return it's own value
def rlookup(service):
    return service

def mapHostnameUrl(url):
    result = url
    urlparts = urlparse.urlparse(url)
    if urlparts is not None:
        result = urlparts.netloc
        hparts = urlparts.netloc.split('.')
        if hparts is not None:
            result = ".".join(len(hparts[-2]) < 4 and hparts[-3:] or hparts[-2:])
            # At this point, if we want to combine hostnames (eg. box.com, box12.com) we can do so
            if result == 'force.com':
                result = 'salesforce.com'
            if result == 'box.net':
                result = 'box.com'
    return result

def main():
    if len(sys.argv) != 3:
        print "Usage: python host_lookup.py [url field] [hostname field]"
        sys.exit(1)

    hostfield = sys.argv[1]
    urlfield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        # Perform the lookup or reverse lookup if necessary
        if result[hostfield] and result[urlfield]:
            # both fields were provided, just pass it along
            w.writerow(result)

        elif result[hostfield]:
            # only mimetype was provided, add filetype
            result[urlfield] = lookup(result[hostfield])
            if result[urlfield]:
                w.writerow(result)

        elif result[urlfield]:
            # only filetype was provided, add mimetype
            result[hostfield] = rlookup(result[urlfield])
            if result[hostfield]:
                w.writerow(result)

main()
