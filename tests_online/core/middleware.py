class UTF8Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ct = response.get("Content-Type", "text/plain")
        if not 'charset' in ct:
            ct += (';' if not ct.endswith(';') else '') + " charset=utf-8"
            response["Content-Type"] = ct
        return response
