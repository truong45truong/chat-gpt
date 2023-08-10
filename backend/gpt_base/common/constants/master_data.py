from enum import unique, Enum


@unique
class TranslateTypesEnum(int, Enum):
    VIETNAMESE = 1
    ENGLISH = 2