from enum import Enum

class RegexPattern(str, Enum):
    PASS_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,255}$"
    SNAKE_CASE = "(?<!^)(?=[A-Z])"
    PHONE_NUMBER_REGEX = "^[0-9]{8,11}$"

class TokenObtainPairEnum(str, Enum):
    CREATED_AT_LABEL = "created_at"
    
class ProviderEnum(str, Enum):
    PROVIDER_LABEL = 'provider'
    USER = 'user'

class RoleEnum(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    