/**
 * Get all course results for the given competitor.
 */
SELECT
    CourseResult.finish_point,
    CourseResult.completed,
    Course.season,
    Course.category,
    Course.course_id,
    Course.size
FROM CourseResult, Course
WHERE CourseResult.course_id=Course.course_id AND CourseResult.ninja_id=:nid;
