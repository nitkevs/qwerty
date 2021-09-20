from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

from trains.forms import TrainForm
from trains.models import Train


def home(request, pk=None):
    # if request.method == 'POST':
    #     form = TrainForm(request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         form.save()
    # else:
    #     form = TrainForm()
    qs = Train.objects.all()
    lst = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj,}
    return render(request, 'trains/home.html', context)


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'

    def get_success_message(self, cleaned_data):
        return f'Поезд {cleaned_data["name"]} успешно создан.'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    # success_message = f'Поезд успешно отредактирован.'

    def get_success_message(self, cleaned_data):
        return f'Поезд {self.object.name} успешно отредактирован.'


class TrainDeleteView(DeleteView):
    model = Train
    # template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, f'Поезд {Train.objects.get(pk=kwargs["pk"])} успешно удалён.')
        return self.post(request, *args, **kwargs)

    template_name = 'trains/detail.html'


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'
