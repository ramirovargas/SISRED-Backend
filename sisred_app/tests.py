import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from sisred_app.models import Perfil


class SisredTestCase(TestCase):
    def test_find_user_by_identification_number(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")

        response = self.client.get('/api/habilitar-usuario/' + str(profile1.numero_identificacion))
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['username'], 'test1')

    def test_update_user_state_in_sisred(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")

        response = self.client.put('/api/habilitar-usuario/' + str(profile1.numero_identificacion))
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['estado_sisred'], 1)

