import sys
from utils.additional_exceptions import *

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
        exit_with_print(5, f"Bad value in read_csv")
    if isinstance(exc, DfNoneError):
        exit_with_print(6, "Dataframe is None")
    if isinstance(exc, pd.errors.ParserError):
        exit_with_print(7, "pandas' parser error happpened")
    if isinstance(exc, pd.errors.EmptyDataError):
        exit_with_print(8, "Data turned up empty according to pandas")
    if isinstance(exc, Exception):
        exit_with_print(9, "Some error occured")
