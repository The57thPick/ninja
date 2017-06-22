#!/usr/bin/env python3
import os
import urllib.parse as urlparse

from peewee import *

urlparse.uses_netloc.append('postgres')
URL = urlparse.urlparse(os.environ['DATABASE_URL'])

# Create our peewee database instance using $DATABASE_URL.
DATABASE = PostgresqlDatabase(
    database=URL.path[1:],
    user=URL.username,
    password=URL.password,
    host=URL.hostname,
    port=URL.port
)

SEASONS = [1, 2, 3, 4, 5, 6, 7, 8]
TYPE_2_INT = {
    "N/A": 0,
    "Qualifying": 2,
    "Finals": 4,
    "1": 6,
    "2": 8,
    "3": 10,
    "4": 12
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


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Ninja(BaseModel):
    """Ninja represents an individual ANW competitor.
    """
    ninja_id = PrimaryKeyField()
    first_name = TextField()
    last_name = TextField()
    sex = CharField()
    age = IntegerField()

    def rating(self):
        """Calculate a given competitor's Ninja Rating (NR).
        """
        completes = [0] * 6
        finishes = [0] * 6
        finish_scores = [0] * 6
        seasons = set()

        # ...
        ret = CourseResult.select().where(CourseResult.ninja_id==self.ninja_id)
        for result in ret.all():
            cid = result.course_id
            data = Course.select().where(Course.course_id==cid)
            int_type = TYPE_2_INT[data.category]
            type_idx = int(int_type / 2) - 1
            seasons.add(data.season)
            if not result.completed:
                # The course wasn't completed, so there's a fail point.
                point = result.finish_point - 1
                finishes[type_idx] += int_type + 0.1 * point
                finish_scores[type_idx] += int_type + point
            else:
                # The course was completed, so there's no fail point.
                completes[type_idx] += 1
                finishes[type_idx] += int_type + 0.1 * results[2]
                finish_scores[type_idx] += int_type + results[2]

        n_seasons = len(seasons)
        best = max(finish_scores)

        return ret[0].course_id


class Course(BaseModel):
    """Course represents an individual ANW course.
    """
    course_id = PrimaryKeyField()
    city = TextField()
    category = TextField()
    season = IntegerField()


class Obstacle(BaseModel):
    """Obstacle represents an individual ANW obstacle.
    """
    obstacle_id = PrimaryKeyField()
    title = TextField()
    course = ForeignKeyField(Course, to_field='course_id')


class ObstacleResult(BaseModel):
    """ObstacleResult represents an individual ANW obstacle result.
    """
    result_id = PrimaryKeyField()
    transition = DecimalField()
    duration = DecimalField()
    completed = BooleanField()
    obstacle = ForeignKeyField(Obstacle, to_field='obstacle_id')
    ninja = ForeignKeyField(Ninja, to_field='ninja_id')


class CourseResult(BaseModel):
    """CourseResult represents an individual ANW course result.
    """
    result_id = PrimaryKeyField()
    duration = DecimalField()
    finish_point = IntegerField()
    completed = BooleanField()
    course = ForeignKeyField(Course, to_field='course_id')
    ninja = ForeignKeyField(Ninja, to_field='ninja_id')


ninja = Ninja.select().where(Ninja.ninja_id==7).get()
print(ninja.rating())
