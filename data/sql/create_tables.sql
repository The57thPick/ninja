/**
 * Ninja represents an individual ANW competitor.
 *
 * Note that, unlike the other columns, `age` can be NULL. This is because we
 * aren't always given a competitor's age (especially in "partially shown"
 * cases).
 */
CREATE TABLE Ninja (
    ninja_id serial PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    sex char(1) NOT NULL,
    age integer
);

/**
 * Course represents an individual ANW course.
 *
 * `category` is one of "Qualifying", "Finals", or a stage number (1 - 4).
 */
CREATE TABLE Course (
    course_id serial PRIMARY KEY,
    city text NOT NULL,
    category text NOT NULL,
    num_obstacles integer NOT NULL,
    season integer NOT NULL
);

/**
 * Obstacle represents an individual ANW obstacle.
 */
CREATE TABLE Obstacle (
    obstacle_id serial PRIMARY KEY,
    title text NOT NULL,
    course_id integer references Course(course_id)
);


/**
 * ObstacleResult represents an individual ANW obstacle result.
 *
 * `transition` is the amount of time used (i.e., rest) prior to starting the
 * obstacle.
 */
CREATE TABLE ObstacleResult (
    result_id serial PRIMARY KEY,
    transition decimal NOT NULL,
    duration decimal,
    completed boolean NOT NULL,
    obstacle_id integer references Obstacle(obstacle_id),
    ninja_id integer references Ninja(ninja_id)
);

/**
 * CourseResult represents an individual ANW course result.
 */
CREATE TABLE CourseResult (
    result_id serial PRIMARY KEY,
    duration decimal,
    finish_point integer NOT NULL,
    completed boolean NOT NULL,
    course_id integer references Course(course_id),
    ninja_id integer references Ninja(ninja_id)
);
