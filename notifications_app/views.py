from django.http import HttpResponse

def index(request):
    return HttpResponse("Notifications app working")
