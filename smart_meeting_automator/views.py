from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Smart Meeting Automator Backend Running",
        "version": "1.0"
    })
