from django.views.generic.list import ListView


from currency.models import Rate


class RateListView(ListView):
    model = Rate
    template_name = 'rates_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Rate.objects.all().order_by('-id')[:20]
        context['rates'] = queryset
        return context
