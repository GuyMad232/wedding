from django.utils.deprecation import MiddlewareMixin

class CacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/serve_apng/':
            response['Cache-Control'] = 'public, max-age=31536000'
        return response
