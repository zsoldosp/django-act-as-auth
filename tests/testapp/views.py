from django.http import HttpResponse


def whoami(request):
    return HttpResponse(request.user.username)
