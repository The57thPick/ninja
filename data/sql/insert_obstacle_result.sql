/**
 * Inserts a row into the ObstacleResult table.
 */
INSERT INTO ObstacleResult(obstacle_id, ninja_id, duration, transition, completed)
VALUES (:obsid, :nid, :dur, :trans, :comp)
RETURNING obstacle_id;
