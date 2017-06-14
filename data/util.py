import doctest
import difflib
import re
import sys


def is_number(s):
    """Determine if the string `s` is a number.

    Examples:
        >>> is_number('5')
        True
        >>> is_number('5.5')
        True
        >>> is_number('foo')
        False
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def name_and_status(entry):
    """Get the athlete's name and shown status (S, PS, or NS) from a CSV entry.

    Args:
        entry: The athlete's name entry (e.g., "Max Grocki (NS)").

    Returns:
        (str, str): (name, shown status).

    Examples:
        >>> name_and_status("Micheal Burkett-Crist (NS)")
        ('Micheal Burkett-Crist', 'NS')
        >>> name_and_status("P.J. Granger")
        ('P.J. Granger', 'S')
        >>> name_and_status("Alex Dell'Aquila (NS)")
        ("Alex Dell'Aquila", 'NS')
        >>> name_and_status('Luciano Acuna Jr. (PS)')
        ('Luciano Acuna Jr.', 'PS')
        >>> name_and_status('Luciano Acuna Jr.')
        ('Luciano Acuna Jr.', 'S')
    """
    m = re.compile('([^\(]+)(?:\((PS|NS)\))?').match(entry)
    return m.group(1).strip(" ").strip(), m.group(2) if m.group(2) else 'S'


def check_spelling(name, seen):
    """Look for names that could be mispellings of `name`.

    Examples:
        >>> check_spelling('Jon Hoton', ['Jon Horton', 'Jon Hoton'])
        ['Jon Horton']
        >>> check_spelling('Jon Alexis Jr.', ['Jon Alexis Sr.'])
        ['Jon Alexis Sr.']
    """
    matches = difflib.get_close_matches(name, seen, cutoff=0.9)
    if matches and name in matches:
        matches.remove(name)
    return matches


def finish_point(row, shown, results, obstacles, completed):
    """Extract a failure point (i.e., which obstacle) from a given row.

    Args:
        shown (str): "S", "PS" or "NS".
        results (int): The number of completed obstacles.
        completed (bool): True if the course was completed and False otherwise.

    Returns:
        int: An integer representing the failure point (e.g., 3 for the third
             obstacle).
    """
    if results or completed:
        # If completed is True, the course was completed and thus there is no
        # fail point. If completed is False, then the fail point is 1 +
        # <# of completed obstacles>.
        finish_point = obstacles if completed else results + 1
    else:
        # Ignore the first 3 columns (Name, Age and Sex) and the last 2 (Total
        # and Completed).
        data = row[3:-2][0::2]
        if shown == "NS" and "F" in data:
            # The position of "F" indicates the failure point. E.g.,
            # [0, 1, 2, 'F', None, None] => 4th obstacle.
            finish_point = data.index("F") + 1
        elif shown == "S":
            # In this case, there are no results but shown == "S". Thus, the
            # fail point is the first obstacle.
            finish_point = 1
        elif shown == "PS":
            # In this case, there will be N blank columns before we start
            # recording data - e.g., [None, None, 1, 3, None]. Here, the fail
            # point is the 4th obstacle (index 3).
            offset = -1
            for element in reversed(data):
                if not element:
                    offset += 1
                else:
                    break
            finish_point = len(data) - offset
        else:
            finish_point = -1

    return finish_point


def is_valid(rows, headings):
    """Validate the CSV file with the given `rows` and `headings`

    Returns:
        bool: `True` if no errors were found and `False` otherwise.
    """
    past_names = []
    expected_length = len(headings)
    for i, row in enumerate(rows):
        idx = i + 2
        name, shown = name_and_status(row[0])

        # Check for missing columns.
        if len(row) != expected_length:
            print('Length mismatch ({0} vs. expected {1}) at row = {2}'.format(
                len(row), expected_length, idx))
            return False

        # Check for transitions listed as failure points.
        for j, value in enumerate(row):
            if value == 'F' and headings[j].startswith('Transition'):
                print('Invalid failure point at row = {0}'.format(idx))
                return False

        c = 3
        t = 0
        while row[c] not in  ('', 'F') and c < expected_length - 2:
            t += float(row[c])
            c += 1

        # If a competitor failed the course, their last attempted obstacle
        # should not have an associated duraton.
        if row[-1] == 'Failed':
            if (c - 1 > 2) and not headings[c - 1].startswith('Transition'):
                print('Time for failed obstacle at row = {0}'.format(idx))
                print(row[c - 1])
                return False

        # A competitor's splits should sum to their total time.
        try:
            if row[-2] and shown not in ('PS', 'NS'):
                observed = round(float(row[-2]), 2)
                expected = round(t, 2)
                if observed != expected:
                    print('{0} != {1} at row = {2}'.format(t, observed, idx))
                    return False
        except ValueError:
            print('Bad finish time ({0}) at row = {1}'.format(row[-2], idx))
            return False

        # Warn about potential typos.
        matches = check_spelling(name, past_names)
        if matches:
            print("{} - {}, misspelled?".format(name, matches))
        past_names.append(name)

    return True

if __name__ == '__main__':
    # Run tests
    failed, _ = doctest.testmod()
    if failed:
        sys.exit(1)
