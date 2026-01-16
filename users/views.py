from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from .serializers import RegisterSerializer, LoginSerializer

import logging

logger = logging.getLogger(__name__)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(
            "User fetched profile",
            extra={"user_id": request.user.id},
        )
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
        })


# class RegisterView(CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(
            "New user registered",
            extra={"user_id": user.id, "email": user.email},
        )


# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]

# 🔐 NEVER log passwords or tokens.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # ⚠️ this won't log failed logins properly
    # because the exception is raised before returning response.
    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)

    #     if response.status_code == 200:
    #         logger.info(
    #             "User login successful",
    #             extra={"email": request.data.get("email")},
    #         )
    #     else:
    #         logger.warning(
    #             "User login failed",
    #             extra={"email": request.data.get("email")},
    #         )

    #     return response
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            logger.warning(
                "User login failed",
                extra={"email": request.data.get("email")},
            )
            raise
        else:
            logger.info(
                "User login successful",
                extra={"email": request.data.get("email")},
            )
            return response
