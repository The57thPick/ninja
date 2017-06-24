"""split_mt.py

This script is designed to aid in the process of collecting splits from Mount
Midoriyama stages. Notably, unlike all previous courses, Midoriyama stages have
a clock that counts down: competitors are given a fixed amount of time (we
assume 2:30.00) to complete a given course. So, instead of inputing actual
splits, we need to input the clock time at each checkpoint on the course.

Example:
    This script is designed to called from the command line as follows ::

        $ python split_mt.py
        split: 2:24.78
        ...
"""
import datetime

# We assume that we're given 2:30.00.
tdt = datetime.datetime.strptime('2:30.00', '%M:%S.%f')
total = 60 * tdt.minute + (tdt.second + (tdt.microsecond / 1000000.0))

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
    # Calculate the actual split and update the total.
    splits.append(round(total - split, 2))
    total = split

# The last split (the total) is the summation of all previous splits.
splits.append(round(sum(splits), 2))
# print the CSV-formatted row.
print(str(splits).strip('[]').replace(' ', '') + ',')
