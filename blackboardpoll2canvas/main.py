""" Import poll reports from BlackBoard Collaborate Ultra into Canvas gradebook format
"""

import re
import argparse
import pandas
import nameparser

pat = (
    r"PollReport_"
    r"(?P<poll_name>[\w ]+)_"
    r"(?P<poll_timestamp>\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})"
    r".csv"
)

POLL_COLUMNS = ["AttendeeName", "PollQuestion", "AttendeePollAnswer"]
GRADEBOOK_COLUMNS = ["Student", "ID", "SIS User ID", "SIS Login ID", "Section"]


def makeparser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gradebook_path",
                        help="path to the CSV file with Canvas gradebook",
                        metavar="gradebook")
    parser.add_argument("poll_path",
                        help="path to the CSV file with poll reports",
                        nargs="+",
                        metavar="poll")
    parser.add_argument("keys_path",
                        help="path to the CSV file with poll keys",
                        metavar="keys")
    parser.add_argument("output_path",
                        help="write the new CSV to this path",
                        metavar="output")
    return parser


def _normalize(name):
    STRING_FORMAT = "{last}, {first}"
    STRING_2_FORMAT = "{last} {suffix}, {first}"
    n = nameparser.HumanName(name)
    if n.suffix is not "":
        n.string_format = STRING_2_FORMAT
    else:
        n.string_format = STRING_FORMAT
    return str(n)


def _score1(correct, attendee):
    if pandas.isna(attendee):
        return 0
    if correct == '*':
        return 1
    return 1 if correct == attendee else 0


def _score(x):
    return _score1(x['CorrectAnswer'], x['AttendeePollAnswer'])


def main(args):
    roster = pandas.read_csv(args.gradebook_path,
                             usecols=GRADEBOOK_COLUMNS,
                             dtype="string")
    keys = pandas.read_csv(args.keys_path, dtype="string")
    keys['CorrectAnswer'] = keys['CorrectAnswer'].str.upper().astype("string")
    d = {}
    for path in args.poll_path:
        # Extract poll date from path name
        m = re.match(pat, path)
        poll_date = m["poll_timestamp"][:10]  # YYYY-MM-DD
        poll_name = "Poll " + poll_date
        # Select poll questions
        poll_keys = keys.set_index("PollDate").loc[poll_date]
        poll_keys = poll_keys.reset_index(drop=True)
        # When correct answer is NA all answers are correct
        poll_keys["CorrectAnswer"] = poll_keys["CorrectAnswer"].fillna("*")
        # Cross join roster with poll questions
        poll_keys["dummy"] = 1
        roster["dummy"] = 1
        df0 = pandas.merge(poll_keys, roster, on="dummy").drop("dummy", axis=1)
        df0.set_index(["Student", "PollQuestion"], inplace=True)
        # Read poll answers
        df = pandas.read_csv(path, encoding="utf-8-sig",
                             usecols=POLL_COLUMNS,
                             dtype="string")
        # Convert student name to Canvas format (last name, first name)
        df = df.groupby(["AttendeeName", "PollQuestion"]).tail(1)
        df["Student"] = df["AttendeeName"].map(_normalize).astype("string")
        df.set_index(["Student", "PollQuestion"], inplace=True)
        df['AttendeePollAnswer'] = df['AttendeePollAnswer'].str.upper()
        # df['IsCorrect'] = df['CorrectAnswer'] == df['AttendeePollAnswer']
        df0 = df0.join(df)
        scores = df0.apply(_score, axis=1).groupby('Student').sum()
        d[poll_name] = scores
    roster.set_index('Student', inplace=True)
    for poll_name in d:
        roster[poll_name] = d[poll_name]
    return roster.drop("dummy", axis=1)


if __name__ == '__main__':
    parser = makeparser()
    args = parser.parse_args()
    roster = main(args)
    roster.to_csv(args.output_path)
    print("Written: {}".format(args.output_path))
