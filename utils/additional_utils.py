import sys
from utils.additional_exceptions import *
import pandas as pd

def exit_with_print(code: int = 1, message: str = ""):
    sys.stderr.write(message + "\n")
    exit(code)

def exit_by_exception(exc: Exception, message: str = ""):
    if isinstance(exc, FilenameEmptyError):
        exit_with_print(2, "Filename turned out empty")
    if isinstance(exc, FileNotFoundError):
        exit_with_print(3, f"{message} not found")
    if isinstance(exc, PermissionError):
        exit_with_print(4, f"{message} not accessible")
    if isinstance(exc, ValueError):
        exit_with_print(5, f"Bad value")
    if isinstance(exc, DfNoneError):
        exit_with_print(6, "Dataframe is None")
    if isinstance(exc, pd.errors.ParserError):
        exit_with_print(7, "pandas' parser error happpened")
    if isinstance(exc, pd.errors.EmptyDataError):
        exit_with_print(8, "Data turned up empty according to pandas")
    if isinstance(exc, Exception):
        exit_with_print(9, "Some error occured: " + str(exc))

def ft_truncate(s, max_len):
    if (len(s) < max_len):
        return s
    return s[:max_len - 3] + "..."

def ft_pretty_table_print(tb, col_w: int = 12):
    for key in tb:
        print(f"{key:15}", end=" ")
        for item in tb[key]:
            if (key == "Names"):
                print(f"{ft_truncate(item, col_w):>{col_w}}", end=" ")
            elif (key == "Count"):
                print(f"{item:{col_w}}", end=" ")
            else:
                print(f"{item:{col_w}.4f}", end=" ")
        print()
