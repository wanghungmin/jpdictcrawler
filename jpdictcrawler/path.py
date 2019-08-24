import os.path
__all__ = [
    'FILE_PATH',
    'HTML_RESULT_PATH',
    'ICON_PATH',
    'DEBUG_PATH',
    'LOGFILE_PATH',
    'COOKIES_PATH',
]

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.join(os.path.join(FILE_PATH, ".."),"icons")
DEBUG_PATH = os.path.join(FILE_PATH, "debug")
HTML_RESULT_PATH = os.path.join(DEBUG_PATH, "result.html")
LOGFILE_PATH = os.path.join(DEBUG_PATH, "logfile.log")
COOKIES_PATH = os.path.join(FILE_PATH, "cookies.txt")