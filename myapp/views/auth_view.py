from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.auth_serializers import AuthSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from ..permissions import IsNotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.exceptions import ValidationError


@api_view(['POST'])
@permission_classes([IsNotAuthenticated])
def regis(request):
    try:
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Regitration succes!',
                'data' : {
                    'username'  : user.username,
                    'email'     : user.email
                }
            }, status=status.HTTP_201_CREATED)
        
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)

@api_view(['POST'])
@permission_classes([IsNotAuthenticated])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email    = request.data.get('email')

        user = User.objects.get(username=username, email=email)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'success' : True,
                'message' : 'Login succes!',
                'data' : {
                    'refresh'   : str(refresh),
                    'access'    : str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        else:
            raise NotAuthenticated('Email, username or password is incorrect!')
    except User.DoesNotExist :
        raise NotAuthenticated('Email, username or password is incorrect!')

@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            raise ValidationError('Refresh token is required.')
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'success' : True,
            'message' : 'Logout succes!'
        }, status=status.HTTP_205_RESET_CONTENT)
    except TokenError as e:
        raise ValidationError(f'Invalid token: {str(e)}')