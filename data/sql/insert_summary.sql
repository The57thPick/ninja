/**
 * Inserts a row into the CareerSummary table.
 */
INSERT INTO CareerSummary(
    ninja_id,
    best_finish,
    speed,
    success,
    consistency,
    rating,
    seasons,
    qualifying,
    finals,
    stages
)
VALUES (:nid, :best, :speed, :success, :consistency, :rating, :seasons, :q, :f, :s)
RETURNING summary_id;
