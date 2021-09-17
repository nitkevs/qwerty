from django.shortcuts import get_object_or_404, render

from cities.models import City

__all__ = (
    'home',
)

def home(request, pk=None):
    if pk:
        city = City.objects.filter(id=pk).first()
        if city:
            context = {'object': city}
        else:
            context = {'city_not_found_message': 'Город не найден. <a href="/cities/">Перейти к списку городов</a>.'}

        # city = get_object_or_404(City, pk=pk)

        return render(request, 'cities/detail.html', context)
    qs = City.objects.all()
    context = {'object_list': qs}
    return render(request, 'cities/home.html', context)

