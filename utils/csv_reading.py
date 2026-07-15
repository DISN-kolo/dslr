import pandas as pd
from .additional_exceptions import FilenameEmptyError, DfNoneError

def read_or_raise(filename: str = ""):
    df = None
    if (filename == ""):
        raise FilenameEmptyError
    df = pd.read_csv(filename)
    if (df is None):
        raise DfNoneError
    return (df)

def read_subjects_or_raise(filename: str = ""):
    if (filename == ""):
        raise FilenameEmptyError
    with open(filename) as f:
        subjects = [line.strip() for line in f if line.strip() != ""]
    return subjects
