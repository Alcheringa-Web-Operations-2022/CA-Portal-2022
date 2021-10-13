from django.shortcuts import render


def error_404(request, exception, template_name="ca_portal/404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def error_500(request, *args, **argv):
    return render(request, 'ca_portal/404.html', status=500)
