from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

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
    lst = Paginator(qs, 2)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'

    def get_success_message(self, cleaned_data):
        return f'Город {cleaned_data["name"]} успешно создан.'


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    # success_message = f'Город успешно отредактирован.'

    def get_success_message(self, cleaned_data):
        return f'Город {self.object.name} успешно отредактирован.'


class CityDeleteView(DeleteView):
    model = City
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, f'Город {City.objects.get(pk=kwargs["pk"])} успешно удалён.')
        return self.post(request, *args, **kwargs)

    template_name = 'cities/detail.html'


class CityListView(ListView):
    model = City
    paginate_by = 2
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context
