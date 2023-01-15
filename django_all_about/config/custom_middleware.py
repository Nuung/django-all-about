from time import process_time_ns
from django.core.handlers.wsgi import WSGIRequest

# from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


def view_process_time_middleware(get_response):
    def middleware(request: WSGIRequest):
        view_process_start_time = process_time_ns()
        response: Response = get_response(request)

        ############ After response ############

        view_process_end_time = process_time_ns()
        if not response.has_header("process_time"):
            response["View-Process-Run-Time"] = (
                view_process_end_time - view_process_start_time
            )

        return response

    return middleware


class ViewProcessTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        self.view_process_start_time = process_time_ns()

    def process_response(self, request, response):
        response["View-Process-Run-Time"] = (
            process_time_ns() - self.view_process_start_time
        )
