/**
 * Inserts a row into the CareerSummary table.
 */
INSERT INTO CareerSummary(
    ninja_id,
    best_finish,
    speed,
    success,
    consistency,
    seasons,
    qualifying,
    finals,
    stages
)
VALUES (:nid, :best, :speed, :success, :consistency, :seasons, :q, :f, :s)
RETURNING summary_id;
