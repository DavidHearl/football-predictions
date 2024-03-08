"""
This script cleans all the data and copies it from raw data.
"""

import time
from functools import wraps

from process_data.correct_data import DataCorrection


if __name__ == "__main__":
    data_correction = DataCorrection()
    data_correction.copy_data()
    data_correction.correct_unicode_data()
    data_correction.correct_key_values()