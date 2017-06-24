#!/usr/bin/env python3
import csv
import pathlib
import sys

from util import is_valid

CSV_DATA = pathlib.Path('data/csv')
for f in CSV_DATA.glob('**/*.csv'):
    base = f.parts[-1]
    course_info = base.strip('.csv').split('-')
    print('Reading {} ...'.format(base))
    with f.open('rU') as csv_file:
        reader = csv.reader(csv_file)
        headings = next(reader)  # Skip the headings
        rows = list(reader)
        # Validate the CSV file
        if not is_valid(rows, headings):
            sys.exit(1)
sys.exit(0)
