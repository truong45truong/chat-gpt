from enum import Enum

class DateTimeFields(str, Enum):
    YEAR = '%Y'
    MONTH = '%m'
    DAY = '%d'
    DATETIME = '%m/%d/%Y, %H:%M:%S'
    SEPARATOR = ' '


class FormatDateTime(str, Enum):
    DATE_TIME_HMS_FZ: str = '%Y-%m-%d %H:%M:%S.%f%z'
    DATE_TIME = '%Y/%m/%d'
    DATE_TIME_HMS = '%Y-%m-%d %H:%M:%S'

