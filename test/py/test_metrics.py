import trudge.csv_util
import trudge.metrics
import unittest
import os


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CSV_PATH = os.path.join(DATA_DIR, "1.csv")


class TestOrmSeries(unittest.TestCase):
    def test_does_not_except(self):
        df = trudge.csv_util.load_csv(CSV_PATH)
        orm = trudge.metrics.orm_series(df)
