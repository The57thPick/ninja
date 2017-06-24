"""split.py

This script is designed to aid in the process of collecting splits from ANW
courses (excluding Mount Midoriyama stages; see ``split_mt.py``). The idea is
simple: at each checkpoint, you enter the time shown on the run clock and the
script calculates the split for that obstacle or transition.

Example:
    This script is designed to called from the command line as follows ::

        $ python split.py
        split: 2.78
        ...
"""
import datetime

done = False
count = 0
times = []
splits = []

# An empty split indicates that we're done.
while not done:
    split = input('split: ')
    if split == '':
        done = True
        continue

    try:
        dt = datetime.datetime.strptime(split, '%M:%S.%f')
    except:
        # Let the user try again if we're given a malformed split.
        print('Bad split - try again!')
        continue

    split = 60 * dt.minute + (dt.second + (dt.microsecond / 1000000.0))
    times.append(split)

    if count != 0:
        # We any split other than the first, the true split if the difference
        # between the clock time and the last split (count - 1).
        split = split - times[count - 1]

    splits.append(round(split, 2))
    count += 1

# The last split (the total) is the summation of all previous splits.
splits.append(round(sum(splits), 2))
# print the CSV-formatted row.
print(str(splits).strip('[]').replace(' ', '') + ',')
