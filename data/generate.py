#!/usr/bin/env python3
import csv
import records
import sys

from enum import Enum
from pathlib import Path

from util import (
    name_and_status,
    is_valid,
    is_number,
    finish_point
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
    out = db.query(
        'SELECT ninja_id FROM Ninja WHERE first_name=:f AND last_name=:l',
        f=first, l=last).all()

    # TODO: What if two competitors have the same first + last name?
    if not out:
        ninja_id = db.query_file('data/sql/insert_ninja.sql',
            f=first, l=last, s=sex, a=age).all()[0].ninja_id
    else:
        ninja_id = out[0].ninja_id

    return shown, ninja_id


def insert_course(db, headings, info):
    """Add a row to the Course table.

    Args:
        headings (List[str]): headings for the current CSV file.
        info (List[str]): [city, category, season].

    Returns:
        int: The ID of the current course.
    """
    city = info[0] if info[0] != 'Stage' else 'Las Vegas'
    cat = info[1] if not is_number(info[1]) else 'Stage ' + info[1]
    course_id = db.query_file('data/sql/insert_course.sql',
            city=city, cat=cat, s=info[2]).all()
    return course_id[0].course_id


def insert_obstacles(db, row, info, cid):
    """Add a row to the Obstacle table.

    Args:
        info (list): [city, category, season]

    Returns:
        int: The ID of the current course.
    """
    size = 0
    for i in range(3, len(row) - 2):  # Skip The first 3 and last 2 columns.
        name = row[i]
        if name.startswith('Transition'):  # It's a transition column.
            continue
        db.query_file('data/sql/insert_obstacle.sql', title=name, id=cid)
        size += 1
    db.query(
        'UPDATE Course SET size = :s WHERE course_id = :id;', s=size, id=cid)


def insert_obstacle_results(db, row, nid, cid, shown, headings):
    """Add rows to the ObstacleResult table.

    Args:
        nid (int): An ID of a column in the Ninja table.
        cid (int) An ID of a column in the Course table.
        shown (str): "S", "PS" or "NS".
        headers (list): The CSV headers.
    """
    if shown == 'NS':  # There are no results.
        return
    elif shown == 'PS':  # There are partial results.
        print('Skipping PS ...')
        # TODO: Handle PS (alter FAILED_IDS?)
        return
    i = 0
    while i < len(headings) and nid not in FAILED_IDS:
        header = headings[i]
        if header == 'Gender' or header.startswith('Transition'):
            # If the current column is either 'Gender' or 'Transition', we know
            # that the next column's header (i + 1) will be the obstacle label.
            name = headings[i + 1]
            out = db.query(
                """
                SELECT obstacle_id FROM Obstacle
                WHERE (title=:title AND course_id=:id)
                """, title=name, id=cid).all()
            # Given that the current header is 'Gender' or 'Transition', we
            # know that the value at the next column will be the time.
            time = row[i + 1]
            completed = is_number(time)
            if not completed:
                FAILED_IDS.append(nid)
                time = 0
            if header == 'Gender':
                # This is the first obstacle and therefore is the only one
                # without a transition.
                transition = 0
                i += 1
            else:
                transition = row[i]
                i += 2
            db.query_file('data/sql/insert_obstacle_result.sql', nid=nid,
                dur=time, trans=transition, comp=completed,
                obsid=out[0].obstacle_id)
        else:
            i += 1


def insert_course_result(db, row, cid, nid, shown, obstacles):
    """Add columns to the CourseResult table.

    Args:
        nid (int): An ID of a column in the Ninja table.
        cid (int) An ID of a column in the Course table.
        shown (str): "S", "PS" or "NS".
    """
    # time is the second-to-last column.
    time = row[-2] or None
    # completed is the last column.
    completed = row[-1] == 'Completed'

    results = db.query_file('data/sql/obstacles_by_ninja.sql',
        nid=nid, comp=completed, crid=cid).all()[0].count

    # Calculate the finish point.
    finish = finish_point(row, shown, results, obstacles, completed)

    db.query_file('data/sql/insert_course_result.sql',
        crid=cid, nid=nid, dur=time, fp=finish, comp=completed).all()


if __name__ == '__main__':
    # Reset the database and its tables.
    db = records.Database()  # Defaults to $DATABASE_URL.
    tx = db.transaction()
    for table in TABLES:
        db.query('DROP TABLE IF EXISTS {0} CASCADE;'.format(table))
    db.query_file('data/sql/create_tables.sql')

    for f in CSV_DATA.glob('**/*.csv'):
        base = f.parts[-1]
        course_info = base.strip('.csv').split('-')
        print('Reading {} ...'.format(base))
        with f.open('rU') as csv_file:
            FAILED_IDS = []
            reader = csv.reader(csv_file)
            headings = next(reader)  # Skip the headings
            rows = list(reader)

            # Validate the CSV file
            if not is_valid(rows, headings):
                tx.rollback()
                sys.exit(1)

            # Insert data
            obstacles = (len(headings) - 4) / 2
            course_id = insert_course(db, headings, course_info)
            insert_obstacles(db, headings, course_info, course_id)
            for i, row in enumerate(rows):
                shown, ninja_id = insert_ninja(db, row)
                insert_obstacle_results(
                    db, row, ninja_id, course_id, shown, headings)
                insert_course_result(
                    db, row, course_id, ninja_id, shown, obstacles)
    tx.commit()
