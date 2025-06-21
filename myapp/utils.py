import os
from uuid import uuid4
from django.utils.timezone import now
from rest_framework.views import exception_handler
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken

def custom_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}.{ext}"
    return os.path.join('music/', filename)



def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        exc_class = exc.__class__.__name__
        message = str(exc.detail if hasattr(exc, 'detail') else exc)
        details = response.data if isinstance(response.data, dict) else {"non_field_errors": message}
        
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "error": {
                "type": exc_class,
                "message": message                
            }
        }

        if isinstance(exc, serializers.ValidationError):
            message = "Validation error"
        elif isinstance(exc, InvalidToken):
            message = "Invalid token"

        response.data = {
            "success": False,
            "status_code": response.status_code,
            "error": {
                "type": exc_class,
                "message": message,
                "details": details
                }
            }
        
        return response
