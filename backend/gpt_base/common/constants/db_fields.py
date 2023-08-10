from enum import Enum


class DBUserFields(str, Enum):
    ID = 'id'
    EMAIL = 'email'
    PASSWORD = 'password'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    IS_ACTIVE = 'is_active'
    IS_STAFF = 'is_staff'
    IS_SUPERUSER = 'is_superuser'
    DELETE_FLAG = 'delete_flag'
    LAST_LOGIN = 'last_login'
    DATE_JOINED = 'date_joined'
    CREATED_DATE = 'created_date'
    UPDATED_DATE = 'updated_date'
    IS_VERIFY_EMAIL = 'is_verified_mail'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'  

class DBFieldsCommon(str, Enum):
    EMAIL = 'email'
    TOKEN = 'token'
    PASSWORD = 'password'
    NEW_PASSWORD = 'new_password'
    OLD_PASSWORD = 'old_password'
    USER = 'user'
    DELETE_FLAG = 'delete_flag'
    IS_VERIFY_EMAIL = 'is_verified_mail'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
   
class DBMembersFields(str, Enum):
    ID = 'id'
    TOKEN_LIMIT = 'token_limit'
    QUANTITY_TOKEN_USED = 'quantity_token_used'
    USER_ID = 'user_id'
    USER = 'user'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'

class DBConversationsFields(str, Enum):
    ID = 'id'
    MEMBER = 'member'
    MEMBER_ID = 'member_id'
    NAME = 'name'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'

class DBChatsFields(str, Enum):
    ID = 'id'
    CONVERSATION = 'conversation'
    CONVERSATION_ID = 'conversation_id'
    PROMPT = 'prompt'
    CONTENT = 'content'
    CONTENT_TRANSLATE = 'content_translate'
    TRANSLATE_TYPE = 'translate_type'
    TRANSLATE_TYPE_ID = 'translate_type_id'
    ROLE = 'role'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    # other
    IS_INVERSE = 'is_inverse'
class DBPromptsFields(str,Enum):
    ID = 'id'
    MEMBER_ID = 'member_id'
    TITLE = 'title'
    DESCRIPTION = 'description'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
class DBTemplatesFields(str,Enum):
    ID = 'id'
    PARAMS = 'params'
    ICON = 'icon'
    CONTENT = 'content'
    TEXTFEATUREBUTTON = 'text_feature_button'
    NAME = 'name'
    HTML = 'html'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    QUESTION_ASKED  = 'question_asked'
class DBWorkBooksFields(str,Enum):
    ID = 'id'
    QUANTITY = 'quantity_document'
    MEMBER_ID = 'member_id'
    NAME = 'name'
    HTML = 'html'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    QUESTION_ASKED  = 'question_asked'
class DBDocumentsFields(str,Enum):
    ID = 'id'
    NAME = 'name'
    CONTENT = 'content'
    PARAMS_VALUE = 'params_value'
    WORKBOOK = 'workbook_id'
    MEMBER_ID = 'member_id'
    TEMPLATE = 'template_id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    LANGUAGE = 'language'