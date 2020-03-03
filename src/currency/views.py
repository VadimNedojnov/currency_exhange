from django.shortcuts import render


from currency.models import Rate


def rates_list(request):
    queryset = Rate.objects.all()
    return render(request, 'rates_list.html', context={'rates': queryset})
