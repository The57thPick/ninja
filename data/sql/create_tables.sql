/**
 * Ninja represents an individual ANW competitor.
 */
CREATE TABLE Ninja (
    ninja_id serial PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    sex char(1) NOT NULL,
    age integer,
    occupation text,
    instagram text,
    twitter text
);

/**
 * Course represents an individual ANW course.
 *
 * `category` is one of "Qualifying", "Finals", or a stage number (1 - 4).
 *
 * `size` can be NULL because we don't know it until we've counted the number
 * of obstacles.
 */
CREATE TABLE Course (
    course_id serial PRIMARY KEY,
    city text NOT NULL,
    category text NOT NULL,
    season integer NOT NULL,
    size integer
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

/**
 * CareerSummary provides a high-level view of a competitor's career, including
 * the number of courses completed (qualifying, finals, and Mount Midoriyama
 * stages), the number of seasons competed, their best finish, and their Ninja
 * Rating.
 */
CREATE TABLE CareerSummary (
    summary_id serial PRIMARY KEY,
    best_finish text NOT NULL,
    speed decimal NOT NULL,
    success decimal NOT NULL,
    consistency decimal NOT NULL,
    rating decimal NOT NULL,
    seasons integer NOT NULL,
    qualifying integer NOT NULL,
    finals integer NOT NULL,
    stages integer NOT NULL,
    ninja_id integer references Ninja(ninja_id)
);
