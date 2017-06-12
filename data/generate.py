#!/usr/bin/env python3
import csv
import records
import sys

from enum import Enum
from pathlib import Path
from typing import Tuple

from util import (
    name_and_status,
    is_valid
)


CSV_DATA = Path('data/csv')
TABLES = [
    'Ninja',
    'Course',
    'Obstacle',
    'ObstacleResult',
    'CourseResult'
]


def insert_ninja(db, row):
    """Add a row to the Ninja table.

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
        ninja_id = db.query_file('data/sql/insert_ninja.sql',
            f=first, l=last, s=sex, a=age)

    return shown, ninja_id


def insert_course(db, headings, info):
    """Add a row to the Course table.

    Args:
        headings (List[str]): headings for the current CSV file.
        info (List[str]): [city, category, season].

    Returns:
        int: The ID of the current course.
    """
    obstacles = (len(headings) - 4) / 2
    course_id = db.query_file('data/sql/insert_course.sql',
            city=info[0], cat=info[1], s=info[2], n=obstacles).all()
    return course_id[0].course_id

def insert_obstacles(db, row, info, course_id):
    """Add a row to the Obstacle table.

    Args:
        info (list): [city, category, season]

    Returns:
        int: The ID of the current course.
    """
    for i in range(3, len(row) - 2):  # Skip The first 3 and last 2 columns.
        name = row[i]
        if name.startswith('Transition'):  # It's a transition column.
            continue
        db.query_file('data/sql/insert_obstacle.sql', title=name, id=course_id)


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
            rows = list(reader)

            # Validate the CSV file
            if not is_valid(rows, headings):
                sys.exit(1)

            # Insert course info
            course_id = insert_course(db, headings, course_info)
            insert_obstacles(db, headings, course_info, course_id)
            for i, row in enumerate(rows):
                shown, ninja_id = insert_ninja(db, row)
    tx.commit()
