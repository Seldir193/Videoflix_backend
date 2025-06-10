from django.http import JsonResponse

def health_check(request):
    """Einfacher Health-Check Endpunkt"""
    return JsonResponse({"status": "ok"})