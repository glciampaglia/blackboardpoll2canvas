# Blackboard polls to Canvas

Command-line utility to convert poll reports from BlackBoard Collaborate Ultra
into Canvas gradebook format.

Requires [Pandas](//pandas.pydata.org) and the excellent
[Nameparser](https://github.com/derek73/python-nameparser) to parse human
names. The code was written using Python 3.

# Installation

```
python setup.py install
```

# Running

To run the program, first print the help message. It will describe the format
and inputs of the program. The program expects in input at least four files:

1. gradebook - this is a CSV export of the Canvas gradebook;
2. poll - this is a poll report exported from Blackboard Collaborate Ultra;
3. keys - this is CSV file with the poll keys (see _Keys_ below);
4. output - this is the path to the output CSV.

The command can process multiple poll report files. It will extract the date of
the poll from the name of the report file, so make sure NOT to rename the
exported polls.

Here is the full help message:
```
> blackboardpoll2canvas -h

usage: blackboardpoll2canvas [-h] gradebook poll [poll ...] keys output

Import poll reports from BlackBoard Collaborate Ultra into Canvas gradebook
format

positional arguments:
  gradebook   path to the CSV file with Canvas gradebook
  poll        path to the CSV file with poll reports
  keys        path to the CSV file with poll keys
  output      write the new CSV to this path

optional arguments:
  -h, --help  show this help message and exit
```

# Keys

You need to prepare a CSV file with the poll keys. There should be three columns in this file:

1. `PollQuestion` - this should match the `PollQuestion` column in the poll file.
2. `CorrectAnswer` - this should match the `AttendeePollAnswer` column in the poll file.
3. `PollDate` - a date (`YYYY-MM-DD` format) matching the date in the report file name.

You can combine the keys from multiple polls in the same file. The program will
look for the `PollDate` of each key and match it to its report. 

When all answers are correct, enter NA under `CorrectAnswer` (or leave it blank).

## Example Keys

```
PollQuestion,CorrectAnswer,PollDate
Carbon dioxide in the atmosphere,D,2020-09-09
Globally temperatures are increasing because…,C,2020-09-09
Sea surface temperature has,D,2020-09-09
Which of the following phenomena is most closely linked with the salinity of the northwest Atlantic?,NA,2020-09-09
"ocean pH is ______ and the aragonite saturation state, Ω,  is ______.",D,2020-09-09
Which of the following change in fish distribution would you also expect to see with continued warming?,B,2020-09-09
```

# Limitations / Notes

* Multiple answers questions are not supported;
* To compute points for a student, only the last answer is considered;
* Students are matched by `Last Name, First Name`, so students with the same name will be merged together.
