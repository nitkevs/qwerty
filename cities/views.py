from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, CreateView

from cities.forms import HtmlForm, CityForm
from cities.models import City

# __all__ = (
#     'home',
#     'CityDetailView',
# )

def home(request, pk=None):
    # if pk:
    #     city = City.objects.filter(id=pk).first()
    #     if city:
    #         context = {'object': city}
    #     else:
    #         context = {'city_not_found_message': 'Город не найден. <a href="/cities/">Перейти к списку городов</a>.'}
    #     return render(request, 'cities/detail.html', context)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    else:
        form = CityForm()
    qs = City.objects.all()
    context = {'object_list': qs, 'form': form}
    return render(request, 'cities/home.html', context)

class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
