from trudge import csv_util
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "data.csv")

def test_csv_reader():
    assert os.path.isfile(DATA_PATH)
    res = csv_util.parse_file(DATA_PATH)

    assert res[0][2] == 5
    