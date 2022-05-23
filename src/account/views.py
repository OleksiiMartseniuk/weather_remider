from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from src.account import serializers


class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_object(self):
        return self.request.user
