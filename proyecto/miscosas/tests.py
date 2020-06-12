from django.test import TestCase
from django.contrib.auth import get_user_model
from miscosas.models import Comentario, PagUsuario, Item, Alimentador, Like

# Create your tests here.


class TestViewsAlims(TestCase):
    def test_get_ok(self):
        response = self.client.get('/alimentadores')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h2>Lista de alimentadores</h2>", content)

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

class TestViewsIndex(TestCase):
    def setUp(self):
         alim = Alimentador(nombre="gato")
         alim.save()
         item = Item(titulo="pechuga", alimentador=alim)
         item.save()
         User = get_user_model()
         user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_post_eliminar(self):
        alim = Alimentador.objects.get(nombre="gato")
        response = self.client.post('/', {'alim': alim.id, 'action': 'eliminar'})
        self.assertEqual(response.status_code, 302) #me redirige otra vez a la /
        self.assertEqual(response.url, "/")


    def test_get_ok(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/')
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h2>Top 10 items mas votados:</h2>", content)
        self.assertInHTML("<h2>Top 5 ultimos items votados:</h2>", content)

    def test_post_like(self):
        self.client.login(username='temporary', password='temporary')
        User = get_user_model()
        user = User.objects.get(username="temporary")
        item = Item.objects.get(titulo="pechuga")
        response = self.client.post('/', {'item': item.id, 'action': 'like'})
        self.assertEqual(response.status_code, 302) #me redirige otra vez a la /
        self.assertTrue(Like.objects.filter(usuario=user, item=item).exists())

class TestViewsAlim(TestCase):
    def setUp(self):
         alim = Alimentador(nombre="gato")
         alim.save()

    def test_post_ok(self):
        id = "UCT9zcQNlyht7fRlcjmflRSA"
        response = self.client.post('/alimentador/-1', {'identificador_o_nombre': id,
                                    'tipo_alimentador': 'yt', 'action': "enviar"})
        content = response.content.decode(encoding='UTF-8')
        self.assertTrue(Alimentador.objects.filter(id_canal=id).exists())
        alim = Alimentador.objects.get(id_canal=id)
        response = self.client.post('/alimentador/'+str(alim.id), {'alim': alim.id, 'action': "eliminar"})
        print(alim.elegido)
        self.assertFalse(alim.elegido)

    def test_get_ok(self):
        alim = Alimentador.objects.get(nombre="gato")
        response = self.client.get('/alimentador/'+str(alim.id))
        content = response.content.decode(encoding='UTF-8')
        self.assertIn("Nombre: "+alim.nombre, content)

class TestViewsUser(TestCase):
    def setUp(self):
         User = get_user_model()
         user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
         pag =PagUsuario(usuario=user)
         pag.save()

    def test_get_nok(self):
        response = self.client.get('/usuario/xx')
        self.assertEqual(response.status_code, 404)

    def test_get_ok(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/usuario/temporary', follow=True)
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML("<h3> Cambiar foto de perfil</h3>", content)

    def test_post_estilo(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post('/usuario/temporary', {'action': 'formato', 'tamano': 'grande', 'estilo':'oscuro'})
        css = self.client.get('/style.css', follow=True)
        content = css.content.decode(encoding='UTF-8')
        self.assertIn('url(static/miscosas/fondo_cabecera_oscuro.jpg)', content)


class TestViewsItem(TestCase):
    def setUp(self):
         User = get_user_model()
         user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
         alim = Alimentador(nombre="gato")
         alim.save()
         item = Item(titulo="pechuga", alimentador=alim)
         item.save()

    def test_get_ok(self):
        response = self.client.get('/item/0')
        self.assertEqual(response.status_code, 404)
        item = Item.objects.get(titulo="pechuga")
        response = self.client.get('/item/'+str(item.id))
        self.assertEqual(response.status_code, 200)


    def test_post_ok(self):
        self.client.login(username='temporary', password='temporary')
        item = Item.objects.get(titulo="pechuga")
        response = self.client.post('/item/'+str(item.id), {'action': 'comentario', 'texto': 'algopechuga'})
        content = response.content.decode(encoding='UTF-8')
        self.assertIn("<p>   - El usuario temporary ha dicho: algopechuga", content)

    def test_post_dislike(self):
        self.client.login(username='temporary', password='temporary')
        User = get_user_model()
        user = User.objects.get(username="temporary")
        item = Item.objects.get(titulo="pechuga")
        response = self.client.post('/', {'item': item.id, 'action': 'like'})
        self.assertEqual(response.status_code, 302) #me redirige otra vez a la /
        self.assertTrue(Like.objects.filter(usuario=user, item=item).exists())
