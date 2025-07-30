import logging

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"→ Incoming request: {request.method} {request.path}")
        response = self.get_response(request)
        logger.debug(f"← Response status: {response.status_code} for {request.path}")
        return response
