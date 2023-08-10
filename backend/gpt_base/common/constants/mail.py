from enum import Enum


class MailFields(str, Enum):
    IS_SEND_ONLY_USER = 'is_send_only_user'
    FROM_EMAIL = 'from_email'
    TO = 'to'
    BCC = 'bcc'
    CC = 'cc'
    REPLY_TO = 'reply_to'
    SUBJECT = 'subject'
    HTML_TEMPLATE_NAME = 'html_template_name'
    TXT_TEMPLATE_NAME = 'plain_template_name'
    CONTEXT = 'context'


class MailTemplateEnum(Enum):

    @property
    def id(self):
        return self.value[0]

    @property
    def template_html(self):
        return f'{self.value[1]}.html'

    @property
    def template_txt(self):
        return f'{self.value[1]}.txt'

    @property
    def subject_mail(self):
        return self.value[2]
