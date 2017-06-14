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
    course_id = ForeignKeyField(Course, to_field='course_id')


class ObstacleResult(BaseModel):
    """ObstacleResult represents an individual ANW obstacle result.
    """
    result_id = PrimaryKeyField()
    transition = DecimalField()
    duration = DecimalField()
    completed = BooleanField()
    obstacle_id = ForeignKeyField(Obstacle, to_field='obstacle_id')
    ninja_id = ForeignKeyField(Ninja, to_field='ninja_id')


class CourseResult(BaseModel):
    """CourseResult represents an individual ANW course result.
    """
    result_id = PrimaryKeyField()
    duration = DecimalField()
    finish_point = IntegerField()
    completed = BooleanField()
    course_id = ForeignKeyField(Course, to_field='course_id')
    ninja_id = ForeignKeyField(Ninja, to_field='ninja_id')
