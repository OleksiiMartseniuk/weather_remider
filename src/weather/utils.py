from .models import SubscriptionCity
from .serializers import SubscriptionSerializer


class SubscriptionMixin:
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        # TODO проверить запрос silk
        # TODO  к city добавить id
        return SubscriptionCity.objects. \
            filter(owner=self.request.user). \
            only('id', 'periodicity_send_email', 'city')