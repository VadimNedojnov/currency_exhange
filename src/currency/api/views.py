from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget


from currency.api.serializers import RateSerializer, ContactSerializer
from currency.models import Rate
from account.models import Contact


class RateFilter(filters.FilterSet):
    class Meta:
        model = Rate
        created_range = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
        fields = {
            'created': ['exact', 'gt', 'lt', 'gte', 'lte', 'range'],
            'currency': ['exact', ],
            'source': ['exact', ],
        }


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    # queryset = Rate.objects.all()[:20] WRONG
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RateFilter


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class ContactView(generics.RetrieveUpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
