import logging
import uuid
from threading import local

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')
REQ_UUID_ATTR_NAME = getattr(settings, 'LOCAL_REQ_UUID_ATTR_NAME', '_req_uuid')

logger = logging.getLogger(__name__)

_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


def _do_del_current_user():
    delattr(_thread_locals, USER_ATTR_NAME)


def _do_set_req_uuid(request_uuid):
    setattr(_thread_locals, REQ_UUID_ATTR_NAME, request_uuid)


def _do_del_req_uuid():
    req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, None)

    if req_uuid is not None:
        delattr(_thread_locals, REQ_UUID_ATTR_NAME)


def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    if callable(current_user):
        return current_user()
    return current_user


def get_req_uuid():
    req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, None)
    return req_uuid


class CorrelationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        req_uuid = uuid.uuid4()
        _do_set_req_uuid(req_uuid)
        logger.info(f'START "{request.path} {request.method}"')
        _do_set_current_user(lambda self: getattr(request, 'user', None))

    def process_response(self, request, response):
        current_user = request.user
        # provider = getattr(current_user, 'provider', '')
        logger.info(f'END "{request.path} {response.status_code}" user_logged={current_user}, provider=member')
        _do_del_current_user()
        _do_del_req_uuid()
        return response


class RequestUuidFilter(logging.Filter):

    def filter(self, record):
        req_uuid = getattr(_thread_locals, REQ_UUID_ATTR_NAME, '')
        record.req_uuid = req_uuid
        return True
