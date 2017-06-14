/**
 *
 */
SELECT COUNT(*) FROM ObstacleResult
JOIN Obstacle
    ON (ObstacleResult.obstacle_id=Obstacle.obstacle_id)
JOIN Course
    ON (Obstacle.course_id=Course.course_id)
WHERE (ninja_id=:nid AND completed=:comp AND Obstacle.course_id=:crid)
