from django.shortcuts import redirect, render


def index(request):
    return redirect('/map/')


def page_not_found_view(request):
    response = render(request, 'webapp/404.html', {})
    response.status_code = 404
    return response


def error_view(request):
    response = render(request, 'webapp/500.html', {})
    response.status_code = 500
    return response


def permission_denied_view(request):
    response = render(request, 'webapp/403.html', {})
    response.status_code = 403
    return response


def bad_request_view(request):
    response = render(request, 'webapp/400.html', {})
    response.status_code = 400
    return response
