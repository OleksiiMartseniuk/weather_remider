from rest_framework.permissions import IsAuthenticated


class UserMixin:

    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Получения текущего пользователя"""
        return self.request.user
