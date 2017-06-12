/**
 * Inserts a row into the Obstacle table.
 */
INSERT INTO Obstacle(title, course_id)
VALUES (:title, :id)
RETURNING obstacle_id;
