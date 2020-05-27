from django.test import TestCase
from django.contrib.auth import get_user_model
from miscosas.models import Comentario

# Create your tests here.


class TestViewsIndex(TestCase):
    # def test_post_ok(self):
    #     response = self.client.post('/', {'alim': 35, 'action': 'eliminar'})
    #     self.assertEqual(response.status_code, 200)
    def test_get_ok(self):
        response = self.client.get('/')
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h2>Top 10 items mas votados:</h2>", content)

class TestViewsAlims(TestCase):
    def test_get_ok(self):
        response = self.client.get('/alimentadores')
        self.assertEqual(response.status_code, 200)

class TestsViewsUsuarios(TestCase):
    def test_get_ok(self):
        response = self.client.get('/usuarios')
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h2>Lista de usuarios con cuenta</h2>", content)

class TestViewsInfo(TestCase):
    def test_get_ok(self):
        response = self.client.get('/informacion')
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h3> Funcionamiento</h3>", content)

# class TestViewsUser(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
#
#     def test_get_ok(self):
#         self.client.login(username='temporary', password='temporary')
#         response = self.client.get('/usuario/temporary', follow=True)
#         content = response.content.decode(encoding='UTF-8')
#         print("-----d-d-d-----"+content)
#         self.assertInHTML("<h3> Cambiar foto de perfil</h3>", content)

class TestViewsItem(TestCase):
    def setUp(self):
             User = get_user_model()
             user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
    def test_get_ok(self):
        response = self.client.get('/item/0')
        self.assertEqual(response.status_code, 404)
    def test_post_ok(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post('/item/586', {'texto': 'algo586'})

        content = response.content.decode(encoding='UTF-8')
        print(content)
        print("-----d-d-d-----"+content)
        self.assertInHTML("<p> algo586</p>", content)
