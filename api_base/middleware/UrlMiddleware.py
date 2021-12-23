from django.http import HttpResponsePermanentRedirect
from django.core.handlers.base import BaseHandler
from django.middleware.common import CommonMiddleware
from django.conf import settings


class CommonMiddlewareAppendSlashWithoutRedirect(CommonMiddleware):
    def process_request(self, request):
        if not request.path.endswith('/'):
            request.path = request.path + '/'
            request.path_info = request.path_info + '/'

        return None
