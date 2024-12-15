from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate
from .serilalizers import SignupSerializer
from django.contrib.auth import get_user_model

UserModel =get_user_model()



class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"Message": "User Created Successfully"}, status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, 
                        status= status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email = email,
                            password = password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message':"user logged in"
            }, status= status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status= status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshView(TokenRefreshView):
    pass


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Flush session data
            request.session.flush()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Failed to logout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)



class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "id": user.id,
            "email": user.email
        }, status=status.HTTP_200_OK)







