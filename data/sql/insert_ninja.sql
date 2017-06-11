INSERT INTO Ninja (first_name, last_name, sex, age)
VALUES (:f, :l, :s, :a)
RETURNING ninja_id;
