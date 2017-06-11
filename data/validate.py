import doctest
import difflib
import re
import sys

from typing import Tuple, List

def name_and_status(entry: str) -> Tuple[str, str]:
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


def check_spelling(name: str, seen: List[str]) -> List[str]:
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

def is_valid(rows: List[Tuple[str]], headings: List[str]) -> bool:
    """Validate the CSV file with the given `rows` and `headings`

    Returns:
        bool: `True` if no errors were found and `False` otherwise.
    """
    past_names = []
    expected_length = len(headings)
    for i, row in enumerate(rows):
        idx = i + 2
        # Check for missing columns
        if len(row) != expected_length:
            print('Length mismatch ({0} vs. expected {1}) at row = {2}'.format(
                len(row), expected_length, idx))
            return False

        # Check for transitions listed as failure points
        for j, value in enumerate(row):
            if value == 'F' and headings[j].startswith('Transition'):
                print('Invalid failure point at row = {0}'.format(idx))
                return False

        # Warn about potential typos
        name, shown = name_and_status(row[0])
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
