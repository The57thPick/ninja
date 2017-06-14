/**
 *
 */
INSERT INTO CourseResult(course_id, ninja_id, duration, finish_point, completed)
VALUES (:crid, :nid, :dur, :fp, :comp)
RETURNING result_id;
