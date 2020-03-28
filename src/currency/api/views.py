from rest_framework import generics


from currency.api.serializers import RateSerializer
from currency.models import Rate


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    # queryset = Rate.objects.all()[:20] WRONG
    serializer_class = RateSerializer


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    # queryset = Rate.objects.all()[:20] WRONG
    serializer_class = RateSerializer
