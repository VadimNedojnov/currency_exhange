import csv


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView, View
from django.http import HttpResponse
from django_filters.views import FilterView


from currency.filters import RateFilter
from currency.models import Rate


class RateListView(LoginRequiredMixin, FilterView):
    filterset_class = RateFilter
    queryset = Rate.objects.all().order_by('-id')
    template_name = 'rates_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        from urllib.parse import urlencode
        context = super().get_context_data(*args, **kwargs)

        query_params = dict(self.request.GET.items())
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = urlencode(query_params)

        return context

    # @property
    # def template_name(self):

    # @property
    # def paginate_by(self):
    #     paginate = int(self.request.GET.get('paginate-by'))
    #     return paginate


class RateCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)
        headers = [
            'id',
            'created',
            'currency',
            'buy',
            'sale',
            'source',
        ]
        writer.writerow(headers)
        for rate in Rate.objects.all().iterator():
            writer.writerow(map(str, [
                rate.id,
                rate.created,
                rate.get_currency_display(),
                rate.buy,
                rate.sale,
                rate.get_source_display(),
            ]))
        return response
