/**
 * Inserts a row into the Course table.
 */
INSERT INTO Course(city, category, season)
VALUES (:city, :cat, :s)
RETURNING course_id;
