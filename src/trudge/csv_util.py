# pandas/numpy and other python deps that are distributed as binaries instead of python source
# can be packaged but it is difficult.
# use built in  CSV functionality instead of pandas.
# https://docs.beeware.org/en/latest/tutorial/tutorial-7.html
import csv
import pprint
import datetime


# def parse_effort(val):
#     i = int(val)
#     assert 1 <= val and val <= 5

COLUMNS = [
    "date",
    "name",
    "reps",
    "weight",
    "rest",
    "positive",
    "hold",
    "negative",
    "effort",
    "notes",
]
N_COLS = len(COLUMNS)
PARSERS = {
    "date": datetime.date.fromisoformat,
    "name": str,
    "reps": int,
    "weight": float,
    "rest": float,
    "positive": int,
    "hold": int,
    "negative": int,
    "effort": int,
    "notes": str,
}


def parse_row(row) -> list:
    ret = []
    if len(row) != len(COLUMNS):
        raise Exception("row has unexpected columns: {}".format(row))
    for idx in range(N_COLS):
        parser = PARSERS[COLUMNS[idx]]
        ret.append(parser(row[idx]))
    return ret

def parse_file(path) -> list[list]:
    found_columns = False
    data = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not found_columns:
                assert row == COLUMNS
                found_columns = True
            else:
                parsed_row = parse_row(row)
                data.append(parsed_row)     
    return data   

