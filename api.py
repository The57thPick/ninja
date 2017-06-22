#!/usr/bin/env python3
import hug
import records

DB = records.Database()  # Defaults to $DATABASE_URL.

SEASONS = [1, 2, 3, 4, 5, 6, 7, 8]
TYPE_2_INT = {
    "N/A": 0,
    "Qualifying": 2,
    "Finals": 4,
    "Stage 1": 6,
    "Stage 2": 8,
    "Stage 3": 10,
    "Stage 4": 12
}
INT_2_TYPE = {v: k for k, v in TYPE_2_INT.items()}
FINISH_2_NAME = {
    2.0: "Qualifying (0 obstacles)",
    2.1: "Qualifying (1 obstacle)",
    2.2: "Qualifying (2 obstacles)",
    2.3: "Qualifying (3 obstacles)",
    2.4: "Qualifying (4 obstacles)",
    2.5: "Qualifying (5 obstacles)",
    2.6: "Qualifying (complete)",
    4.0: "City Finals (0 obstacles)",
    4.1: "City Finals (1 obstacle)",
    4.2: "City Finals (2 obstacles)",
    4.3: "City Finals (3 obstacles)",
    4.4: "City Finals (4 obstacles)",
    4.5: "City Finals (5 obstacles)",
    4.6: "City Finals (6 obstacles)",
    4.7: "City Finals (7 obstacles)",
    4.8: "City Finals (8 obstacles)",
    4.9: "City Finals (9 obstacles)",
    5.0: "City Finals (complete)",
    6.0: "Stage 1 (0 obstacles)",
    6.1: "Stage 1 (1 obstacle)",
    6.2: "Stage 1 (2 obstacles)",
    6.3: "Stage 1 (3 obstacles)",
    6.4: "Stage 1 (4 obstacles)",
    6.5: "Stage 1 (5 obstacles)",
    6.6: "Stage 1 (6 obstacles)",
    6.7: "Stage 1 (7 obstacles)",
    6.8: "Stage 1 (complete)",
    8.0: "Stage 2 (0 obstacles)",
    8.1: "Stage 2 (1 obstacle)",
    8.2: "Stage 2 (2 obstacles)",
    8.3: "Stage 2 (3 obstacles)",
    8.4: "Stage 2 (4 obstacles)",
    8.5: "Stage 2 (5 obstacles)",
    8.6: "Stage 2 (complete)",
    10.0: "Stage 3 (0 obstacles)",
    10.1: "Stage 3 (1 obstacle)",
    10.2: "Stage 3 (2 obstacles)",
    10.3: "Stage 3 (3 obstacles)",
    10.4: "Stage 3 (4 obstacles)",
    10.5: "Stage 3 (5 obstacles)",
    10.6: "Stage 3 (6 obstacles)",
    10.7: "Stage 3 (7 obstacles)",
    10.8: "Stage 3 (complete)",
    12.0: "Stage 4 (0 obstacles)",
    12.1: "Stage 4 (complete)",
}


@hug.get(examples='first=Brent&last=Steffensen')
def rating(first: hug.types.text, last: hug.types.text, hug_timer=3):
    """Returns the given competitor's Ninja Rating.
    """
    out = DB.query(
        "SELECT * FROM Ninja WHERE (first_name=:f AND last_name=:l)",
        f=first, l=last).all()[0]
    speed, consistency, success = 0, 0, 0
    return {'speed': speed, 'consistency': consistency, 'success': success, 'took': float(hug_timer)}
