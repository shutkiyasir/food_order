from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
