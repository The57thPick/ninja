/**
 * Inserts a row into the Ninja table.
 */
INSERT INTO Ninja (first_name, last_name, sex, age, occupation, instagram, twitter)
VALUES (:f, :l, :s, :a, :o, :i, :t)
RETURNING ninja_id;
