class UserMixin:

    def get_object(self):
        """Получения текущего пользователя"""
        return self.request.user
