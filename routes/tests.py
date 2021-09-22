from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from routes.forms import RouteForm
from trains.models import Train
import routes.views as routes_view
from routes.utils import dfs_paths, get_graph
import cities.views as cities_view


class AllTestsCase(TestCase):
    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        lst = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5),
            Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4),
        ]
        Train.objects.bulk_create(lst)

    def test_model_city_duplicate(self):
        city = City(name='A')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_model_train_duplicate(self):
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=29)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_train_train_duplicate(self):
        train = Train(name='tr123', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Изменить время в пути']}, e.message_dict)
            self.assertIn('Изменить время в пути', e.messages)

    def test_home_routes_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(response.resolver_match.func, routes_view.home)

    def test_cbv_detail_views(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.pk}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/detail.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            cities_view.CityDetailView.as_view().__name__
        )

    def test_find_all_routes(self):
        qs = Train.objects.all()
        graph = get_graph(qs)
        all_routes = list(dfs_paths(graph, self.city_A.pk, self.city_E.pk))
        self.assertEqual(len(all_routes), 4)

    def test_valid_route_form(self):
        data = {'from_city': self.city_A.pk,
                'to_city': self.city_B.pk,
                'travelling_time': 9,
                'cities': [self.city_E.pk, self.city_D.pk], }
        data_invalid = {'from_city': self.city_A.pk,
                        'to_city': self.city_B.pk,
                        'cities': [self.city_E.pk, self.city_D.pk], }
        form = RouteForm(data=data)
        form_invalid = RouteForm(data=data_invalid)
        self.assertTrue(form.is_valid())
        self.assertFalse(form_invalid.is_valid())

    def test_message_error_more_time(self):
        data = {'from_city': self.city_A.pk,
                'to_city': self.city_E.pk,
                'travelling_time': 9,
                'cities': [self.city_C.pk], }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Время в пути больше заданного', 1, 200)

    def test_message_error_from_cities(self):
        data = {'from_city': self.city_B.pk,
                'to_city': self.city_E.pk,
                'travelling_time': 35000,
                'cities': [self.city_C.pk], }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Маршрут через эти города невозможен', 1, 200)
