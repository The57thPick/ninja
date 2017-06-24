/**
 * Get a list of all competitors who, for the given course and obstacle,
 */
SELECT ninja_id FROM ObstacleResult
WHERE completed=true AND transition<30.0 AND ObstacleResult.obstacle_id=:obs_id
ORDER BY duration + transition ASC
