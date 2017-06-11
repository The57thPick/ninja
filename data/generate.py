#!/usr/bin/env python3
import csv
import records
import sys

from enum import Enum
from pathlib import Path
from typing import Tuple
from validate import name_and_status, is_valid


CSV_DATA = Path('data/csv')
TABLES = [
    'Ninja',
    'Course',
    'Obstacle',
    'ObstacleResult',
    'CourseResult'
]


def insert_ninja(db: records.Database, row: Tuple[str]) -> Tuple[str, int]:
    """Add a column to the Ninja table.

    `row` is CSV entry like

        Ian Waggoner,42,M,...,

    where the first 3 columns represent a competitor's name, age, and sex.

    Returns:
        (str, int): (shown status, ninja_id).
    """
    name, shown = name_and_status(row[0])
    age = row[1].strip() or None
    sex = row[2].strip()
    if not name or name == 'Name':
        return '', -1

    first, last = name.split(' ', 1)
    ninja_id = db.query(
        'SELECT ninja_id FROM Ninja WHERE first_name=:f AND last_name=:l',
        f=first, l=last).all()

    # TODO: What if two competitors have the same first + last name?
    if not ninja_id:
        ninja_id = db.query_file(
            'data/sql/insert_ninja.sql', f=first, l=last, s=sex, a=age)

    return shown, ninja_id

if __name__ == '__main__':
    # Reset the database and its tables.
    db = records.Database()  # Defaults to $DATABASE_URL.
    tx = db.transaction()
    for table in TABLES:
        db.query('DROP TABLE IF EXISTS {0} CASCADE;'.format(table))
    db.query_file('data/sql/create_tables.sql')

    # Insert data
    for f in CSV_DATA.glob('**/*.csv'):
        path = str(f)
        course_info = path.strip('.csv').split('-')
        print('Reading {} ...'.format(path.split('/')[-1]))
        with f.open('rU') as csv_file:
            reader = csv.reader(csv_file)
            headings = next(reader)  # Skip the headings
            if not is_valid(list(reader), list(headings)):
                sys.exit(1)
            for i, row in enumerate(reader):
                shown, ninja_id = insert_ninja(db, row)
    tx.commit()
