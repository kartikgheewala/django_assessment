import requests
import json
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *


# Authentication
class UserCreateView(APIView):
    """
    :param: username, email, password, confirm_password
    :return: object
    function : Register user data.
    """
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            qry_message = {
                "status": True,
                "message": "User registered successfully.",
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_201_CREATED)

        else:
            if 'username' in serializer.errors:
                if serializer.errors['username'] == ["This field is required."]:
                    message = "username field is required!"
                else:
                    message = "ensure username field has no more than 50 characters!"
            elif 'email' in serializer.errors:
                message = "email field is required!"
            elif 'password' in serializer.errors:
                message = "password field is required!"
            elif 'confirm_password' in serializer.errors:
                message = "confirm password field is required!"
            else:
                message = "Some unknown error is occur!"

            qry_message = {
                "status": False,
                "message": message,
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    :param: username, password
    :return: user object
    function : Login user and sending jwt_token.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=request.data['username'],
                password=request.data['password']
            )

            if user is not None:
                login(request, user)

                url = "http://localhost:8000/api/token/"

                payload = {
                    'username': serializer.data['username'],
                    'password': serializer.validated_data['password'],
                }
                files = []
                headers = {}

                response = requests.request("POST", url, headers=headers, data=payload, files=files)

                user = User.objects.get(
                    id=user.pk
                )
                user.auth_token = json.loads(response.text)['access']
                user.save()

                qry_message = {
                    "status": True,
                    "message": "Logged in successful.",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "auth_token": user.auth_token,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    }
                }
                return Response(qry_message, status=status.HTTP_200_OK)
            else:
                qry_message = {
                    "status": False,
                    "message": "Invalid credentials.",
                    "data": {}
                }
                return Response(qry_message, status=status.HTTP_401_UNAUTHORIZED)

        else:
            if 'username' in serializer.errors:
                if serializer.errors['username'] == ["This field is required."]:
                    message = "username field is required!"
                else:
                    message = "ensure username field has no more than 50 characters!"
            elif 'password' in serializer.errors:
                message = "password field is required!"
            else:
                message = "Some unknown error is occur!"

            qry_message = {
                "status": False,
                "message": message,
                "data": {}
            }
            return Response(qry_message, status=status.HTTP_400_BAD_REQUEST)
