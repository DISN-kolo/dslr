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
