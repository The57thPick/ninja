#!/usr/bin/env python3
import hug
import records

from data.globals import (
    SEASONS,
    TYPE_2_INT,
    INT_2_TYPE,
    FINISH_2_NAME
)

# Connect to the PostgreSQL database given by $DATABASE_URL.
DB = records.Database()


@hug.get(examples='ninja_id=19')
def rating(ninja_id: hug.types.number):
    """Returns the given competitor's Ninja Rating.

    Ninja Rating (NR) attempts to provide a single number by which competitors
    can be compared. It's comprised of three components -- speed, consistency,
    and success -- which each represent core component of being a top American
    Ninja Warrior competitor.

    NOTE: Performance-wise, it would make more sense to do these calculations
    during the database creation phase (rather than on each request) and store
    them in their own table (Rating, perhaps). However, since we're currently
    limited to 10,000 rows, we try to store the bare minimum amount of data in
    the actual database.

    Args:
        ninja_id (int): A competitor's ID number.

    Returns:
        dict: A dictionary containing values of speed (float), success (int),
              and consistency (int).
    """
    # Get all course results for ninja_id.
    results = DB.query(
        """
        SELECT
            CourseResult.finish_point,
            CourseResult.completed,
            Course.season,
            Course.category,
            Course.course_id,
            Course.size
        FROM CourseResult, Course
        WHERE CourseResult.course_id = Course.course_id AND
              CourseResult.ninja_id = :nid;
        """, nid=ninja_id).all()

    n = len(TYPE_2_INT)
    completes = [0] * n
    finishes = [0] * n
    finish_scores = [0] * n
    seasons = set()
    trend = []
    places = []

    # Walk through their career history and record course finishes.
    for result in results:
        int_type = TYPE_2_INT[result.category]
        type_idx = int(int_type / 2) - 1
        seasons.add(result.season)
        if result.completed:
            # The course was completed, so there's no fail point.
            completes[type_idx] += 1
            point = result.size
        else:
            # The course wasn't completed, so there's a fail point.
            point = result.finish_point - 1
        finishes[type_idx] += int_type + 0.1 * point
        finish_scores[type_idx] += int_type + point
        trend.append(point)

        leaders = [l.ninja_id for l in DB.query(
            """
            SELECT ninja_id FROM ObstacleResult, Obstacle
            WHERE course_id=:id AND completed=true AND transition<30.0 AND
                  ObstacleResult.obstacle_id = Obstacle.obstacle_id
            ORDER BY duration + transition ASC
            """, id=result.course_id).all()]

        if ninja_id in leaders:
            places.append(leaders.index(ninja_id) + 1)
        else:
            places.append(0)

    total = sum(trend) if trend else 0
    speed = 3 * sum(x > 0 for x in places) - (sum(places) / len(places))
    return {'speed': speed,
            'consistency': total * len(seasons),
            'success': 4 * max(finish_scores)}
