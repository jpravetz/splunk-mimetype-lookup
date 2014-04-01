#!/usr/bin/env python

import sys
import re
import csv

""" An adapter that takes CSV as input, performs a lookup to map mime types
    to a more common file type (eg. 'MSWord'), then returns the CSV results

    Bidrectional mapping is always required when using an external lookup as an
    'automatic' lookup: one configured to be used without explicit reference in
    a search.
"""


# Given a mimetype, find a uniform file type descriptor
def lookup(mimetype):
    try:
        filetype = mapMimeType(mimetype)
        return filetype
    except:
        return mimetype

# Given an filetype, return it's own value
def rlookup(filetype):
    return filetype

def mapMimeType(mimetype):
    result = mimetype
    if re.match( '(?i).*pdf', mimetype ):
        result = 'PDF'
    elif re.match( '(?i).*ms\-?word.*', mimetype ):
        result = 'MSWord'
    elif re.match( '(?i).*ms\-?excel.*', mimetype ):
        result = 'Excel'
    elif re.match( '(?i).*ms\-?powerpoint.*', mimetype ):
        result = 'Powerpoint'
    elif re.match( '(?i).*officedocument.*wordprocessing', mimetype ):
        result = 'MSWord'
    elif re.match( '(?i).*officedocument.*spreadsheet.*', mimetype ):
        result = 'Excel'
    elif re.match( '(?i).*officedocument.*presentation.*', mimetype ):
        result = 'Powerpoint'
    elif re.match( '(?i)(text|application)/rtf', mimetype ):
        result = 'RTF'
    elif re.match( '(?i)(text|appication)/csv', mimetype ):
        result = 'CSV'
    elif re.match( '(?i)(text|appication)/html', mimetype ):
        result = 'HTML'
    elif re.match( '(?i)(text|appication)/(tab-separated-values|tsv)', mimetype ):
        result = 'TSV'
    elif re.match( '(?i)application/.*shockwave-flash', mimetype ):
        result = 'Shockwave-Flash'
    elif re.match( '(?i)application/.*opendocument.spreadsheet', mimetype ):
        result = 'ODF-Spreadsheet'
    elif re.match( '(?i)application/.*opendocument.presentation', mimetype ):
        result = 'ODF-Presentation'
    elif re.match( '(?i)application/.*opendocument.graphics', mimetype ):
        result = 'ODF-Graphics'
    elif re.match( '(?i)application/.*opendocument.text', mimetype ):
        result = 'ODF-Text'
    elif re.match( '(?i)^application/vnd\.', mimetype ):
        result = re.sub( '(?i)^application/vnd.', '', mimetype )
    return result

def main():
    if len(sys.argv) != 3:
        print "Usage: python mimetype_lookup.py [mimetype field] [filetype field]"
        sys.exit(1)

    mimetypefield = sys.argv[1]
    filetypefield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        # Perform the lookup or reverse lookup if necessary
        if result[mimetypefield] and result[filetypefield]:
            # both fields were provided, just pass it along
            w.writerow(result)

        elif result[mimetypefield]:
            # only mimetype was provided, add filetype
            result[filetypefield] = lookup(result[mimetypefield])
            if result[filetypefield]:
                w.writerow(result)

        elif result[filetypefield]:
            # only filetype was provided, add mimetype
            result[mimetypefield] = rlookup(result[filetypefield])
            if result[mimetypefield]:
                w.writerow(result)

main()
