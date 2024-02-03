from functools import wraps
from rest_framework import status
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger()


def api_response(api_function):
    @wraps(api_function)
    def wrapper(request, *args, **kwargs):
        msg_header = request.msg_header
        method_type = api_function.__name__.upper()
        try:
            status_code, status, message, extra = api_function(request, *args, **kwargs)
            return Utils().get_api_response(status_code, status, msg_header, message, extra)
        except Exception as e:
            logger.error(f"{method_type} API | Error: {e}", exc_info=True)
            return Utils().get_api_response(500, msg_header, str(e), 'error', None)

    return wrapper



class Utils:

    def __init__(self):
        super().__init__()

    def get_user_ip_address(self, request):
        try:
            if request and request.META.get('HTTP_X_FORWARDED_FOR'):
                return request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
            return request.META.get('REMOTE_ADDR')

        except Exception as e:
            logger.error(f'Utils | Error in getting user IP address: {e}', exc_info=True)

    def get_user_agent(self, request):
        try:
            user_agent = request.META['HTTP_USER_AGENT']
            return user_agent if user_agent else ''
        except Exception as e:
            logger.error(f'Utils | Error in getting user agent: {e}', exc_info=True)


    def get_api_response(self, status_code, status, message_header, message, data=None):
        response = {
            "status_code": status_code,
            "status": status,
            "message_header": message_header,
            "message": message,
        }
        if data is not None:
            response["data"] = data

        return JsonResponse(response)