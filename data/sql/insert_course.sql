/**
 * Inserts a row into the Course table.
 */
INSERT INTO Course(city, category, season, num_obstacles)
VALUES (:city, :cat, :s, :n)
RETURNING course_id;
