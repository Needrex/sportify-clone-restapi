from django.http import JsonResponse
from rest_framework import status

def custom_404(request, exception):
    context = {   
        "success": False,
        "status_code": status.HTTP_404_NOT_FOUND,
        "error": {
            "type": "Not Found",
            "message": "Endpoint not found."
        }
    }
    return JsonResponse(context, status=status.HTTP_404_NOT_FOUND)