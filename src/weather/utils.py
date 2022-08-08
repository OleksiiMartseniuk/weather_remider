from .models import SubscriptionCity
from .serializers import SubscriptionSerializer


class SubscriptionMixin:
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return SubscriptionCity.objects.select_related('city').\
            filter(owner=self.request.user).\
            only('id', 'periodicity_send_email', 'city__id', 'city__name')
