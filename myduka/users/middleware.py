# =======================================================================
# FILE: myduka/users/middleware.py (NEW)
# =======================================================================
class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("--- REQUEST DEBUG ---")
        print(f"Host: {request.get_host()}")
        print(f"Path: {request.path}")
        print(f"Method: {request.method}")
        print("--- END REQUEST DEBUG ---")
        
        response = self.get_response(request)
        
        return response
