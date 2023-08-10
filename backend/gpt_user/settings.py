from gpt_base.settings import *

ROOT_URLCONF = 'gpt_user.urls'

WSGI_APPLICATION = 'gpt_user.wsgi.application'

# ---------------------------------------------------------------------------- #
#                                 SWAGGER                                      #
# ---------------------------------------------------------------------------- #
SPECTACULAR_SETTINGS['TITLE'] = 'PSCD-GPT User Api'
