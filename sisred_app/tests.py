from django.test import TestCase
from .models import Version, RED, ProyectoConectate, Metadata, Perfil, Recurso, RolAsignado, Rol, ComentarioMultimedia, \
    Comentario
from django.contrib.auth.models import User
import datetime
import json
from django.forms.models import model_to_dict
from sisred_app.views.views_equipo4 import createNotification
from .models import User, Perfil, RED, Fase, ProyectoConectate, Recurso, NotificacionTipo, Rol, RolAsignado, \
    Notificacion
from django.contrib.auth.models import User
import json


# Create your tests here.
class sisred_appTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        self.perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        self.rol = Rol.objects.create(id_conectate='1', nombre='rolPrueba')

    def testMarcarComoVersionFinalJustOne(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "1"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=1, es_final=False, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter = Version.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter.es_final, True)

    def testMarcarComoVersionFinalFirstMark(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "2"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2, es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1, es_final=False, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter1.es_final, False)
        self.assertEqual(versionMainAfter2.es_final, True)

    def testMarcarComoVersionFinalSecondMark(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "2"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2, es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1, es_final=True, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter1.es_final, False)
        self.assertEqual(versionMainAfter2.es_final, True)

    def testBuscarRedNameAllParameters(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        buscarNombre = "video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 1)

    def testBuscarRedNameAllByNameNoDates(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        buscarNombre = "video"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 1)

    def testBuscarRedNameByName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red",
                           nombre_corto="sred", descripcion="descripcion de video",
                           fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)

        buscarNombre = "video3"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 1)
        self.assertEqual(reds[0]['id'], 1)

    def testBuscarRedNameByshortName(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="sred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        buscarNombre = "sred"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 2)
        self.assertEqual(reds[0]['id'], 2)
        self.assertEqual(reds[1]['id'], 3)

    def testBuscarRedNameByDescription(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="sred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        buscarNombre = "descripcion de video"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 2)
        self.assertEqual(reds[0]['id'], 1)
        self.assertEqual(reds[1]['id'], 3)

    def testBuscarRedNameByTag(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="sred", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="sred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)

        tag = Metadata.objects.create(id=1, tag="tag1")

        red1.metadata.add(tag)

        buscarNombre = "tag1"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 1)
        self.assertEqual(reds[0]['id'], 1)

    def testBuscarRedNameByAllText(self):
        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)

        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test",
                                  nombre_corto="vred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="sonido red",
                                  nombre_corto="test", descripcion="descripcion de sonido",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="sred", descripcion="descripcion de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="video3 red",
                                  nombre_corto="sred", descripcion="descripcion test de video",
                                  fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "test"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?text={buscarNombre}&fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 3)
        self.assertEqual(reds[0]['id'], 1)
        self.assertEqual(reds[1]['id'], 2)
        self.assertEqual(reds[2]['id'], 4)

    def testBuscarRedNameByDates(self):
        fecha = datetime.datetime.now()

        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2019-12-30', '%Y-%m-%d'))
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2019-06-01', '%Y-%m-%d'))
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'))
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2017-12-31', '%Y-%m-%d'))

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"
        fecha_fin = "2019-12-31"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?fstart={fecha_inicio}&fend={fecha_fin}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 1)
        self.assertEqual(reds[0]['id'], 1)

    def testBuscarRedNameByOneDate(self):
        fecha = datetime.datetime.now()

        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)
        # RED.objects.create(id=, proyecto_conectate=proyecto, nombre="", nombre_corto="", descripcion=)
        red1 = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-01-02', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2019-12-30', '%Y-%m-%d'))
        red2 = RED.objects.create(id=2, id_conectate="2", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2019-06-01', '%Y-%m-%d'))
        red3 = RED.objects.create(id=3, id_conectate="3", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2019-06-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'))
        red4 = RED.objects.create(id=4, id_conectate="4", proyecto_conectate=proyecto, nombre="a", nombre_corto="a",
                                  descripcion="a", fecha_inicio=datetime.datetime.strptime('2017-01-01', '%Y-%m-%d'),
                                  fecha_cierre=datetime.datetime.strptime('2017-12-31', '%Y-%m-%d'))

        RolAsignado.objects.create(id_conectate='1', estado=1, red=red1, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='2', estado=1, red=red2, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='3', estado=1, red=red3, rol=self.rol, usuario=self.perfil)
        RolAsignado.objects.create(id_conectate='4', estado=1, red=red4, rol=self.rol, usuario=self.perfil)

        buscarNombre = "b"
        fecha_inicio = "2019-01-01"

        url = f"/api/buscarReds/{self.perfil.usuario.pk}/?fstart={fecha_inicio}"

        response = self.client.get(url, format='json')
        reds = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reds), 2)
        self.assertEqual(reds[0]['id'], 1)
        self.assertEqual(reds[1]['id'], 3)


class CrearVersion(TestCase):
    def testCrearVersionHappyPath(self):
        fecha = datetime.datetime.now()
        userModel = User.objects.create_user(username="testImagen", password="testImagen", first_name="testImagen",
                                             last_name="testImagen", email="testImagen@test.com")
        perfil = Perfil.objects.create(usuario=userModel, estado=0)
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)

        red = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test",
                                 nombre_corto="vred", descripcion="descripcion de video",
                                 fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        r1 = Recurso.objects.create(nombre="mi recurso", archivo="c:/miArchivo.txt", thumbnail="c:/miArchivo.txt",
                                    tipo="txt", descripcion="", autor=perfil, usuario_ultima_modificacion=perfil)

        url = "/api/versiones/"

        response = self.client.post(url, json.dumps(
            {
                "imagen": "img.png",
                "archivos": "carpeta/",
                "redId": red.id,
                "recursos": [r1.id],
                "creado_por": userModel.username,

            }), content_type='application/json')

        # version = json.loads(response.content)

        self.assertEqual(response.status_code, 200)

    def testCrearVersionHappyPath2(self):
        fecha = datetime.datetime.now()
        userModel = User.objects.create_user(username="testImagen", password="testImagen", first_name="testImagen",
                                             last_name="testImagen", email="testImagen@test.com")
        perfil = Perfil.objects.create(usuario=userModel, estado=0)
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)

        red = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test",
                                 nombre_corto="vred", descripcion="descripcion de video",
                                 fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        r1 = Recurso.objects.create(nombre="mi recurso", archivo="c:/miArchivo.txt", thumbnail="c:/miArchivo.txt",
                                    tipo="txt", descripcion="", autor=perfil, usuario_ultima_modificacion=perfil)
        r2 = Recurso.objects.create(nombre="mi recurso2", archivo="c:/miArchivo2.txt", thumbnail="c:/miArchivo2.txt",
                                    tipo="txt2", descripcion="", autor=perfil, usuario_ultima_modificacion=perfil)

        url = "/api/versiones/"

        response = self.client.post(url, json.dumps(
            {
                "imagen": "img.png",
                "archivos": "carpeta/",
                "redId": red.id,
                "recursos": [r1.id, r2.id],
                "creado_por": userModel.username,

            }), content_type='application/json')

        version = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(version['recursos']), 2)

    def testCrearVersionHappyPath3(self):
        fecha = datetime.datetime.now()
        userModel = User.objects.create_user(username="testImagen", password="testImagen", first_name="testImagen",
                                             last_name="testImagen", email="testImagen@test.com")
        perfil = Perfil.objects.create(usuario=userModel, estado=0)
        proyecto = ProyectoConectate.objects.create(id=3, fecha_inicio=fecha, fecha_fin=fecha)

        red = RED.objects.create(id=1, id_conectate="1", proyecto_conectate=proyecto, nombre="test",
                                 nombre_corto="vred", descripcion="descripcion de video",
                                 fecha_inicio=datetime.datetime.now(), fecha_cierre=datetime.datetime.now())

        r1 = Recurso.objects.create(nombre="mi recurso", archivo="c:/miArchivo.txt", thumbnail="c:/miArchivo.txt",
                                    tipo="txt", descripcion="", autor=perfil, usuario_ultima_modificacion=perfil)

        Version.objects.create(numero=1, archivos="aaa", red=red)
        url = "/api/versiones/"

        response = self.client.post(url, json.dumps(
            {
                "imagen": "img.png",
                "archivos": "carpeta/",
                "redId": red.id,
                "recursos": [r1.id],
                "creado_por": userModel.username,

            }), content_type='application/json')

        version = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(version['numero'], 2)

    def test_get_recursos_red(self):
        user1 = User.objects.create_user(username='test11', password='123456', email='test@test.com', first_name='test',
                                         last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user1, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo='AVI', archivo='url2', thumbnail='url3', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.red.recursos.set([recurso1, recurso2])

        url = '/api/red/' + str(self.red.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data['context']), 2)

    def test_get_recursos_red1(self):
        user1 = User.objects.create_user(username='test1', password='123456', email='test@test.com', first_name='test',
                                         last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user1, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo='AVI', archivo='url2', thumbnail='url3', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.red.recursos.set([recurso1, recurso2])

        url = '/api/red/' + str(self.red.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['context'][0]['nombre'], 'test')
        self.assertEqual(current_data['context'][1]['nombre'], 'test2')
        self.assertEqual(current_data['context'][0]['tipo'], 'PNG')
        self.assertEqual(current_data['context'][1]['tipo'], 'AVI')


class VersionTestCase(TestCase):

    def test_get_info_version(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/' + str(self.version.pk) + '/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 1)

    def test_get_info_version2(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')
        self.version2 = Version.objects.create(numero=2, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                               imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/' + str(self.version2.pk) + '/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 2)

    def test_get_info_version3(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        url = '/api/versiones/' + str(self.version.pk) + '/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['numero'], 1)
        self.assertEqual(current_data['red']['proyecto_conectate']['nombre'], 'MISO')

    def test_get_recursos_version(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo='AVI', archivo='url2', thumbnail='url3', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([recurso1, recurso2])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/'
        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data['context']), 2)

    def test_get_recursos_version1(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        recurso1 = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        recurso2 = Recurso.objects.create(nombre='test2', tipo='AVI', archivo='url2', thumbnail='url3', descripcion=' ',
                                          autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([recurso1, recurso2])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/'

        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['context'][0]['nombre'], 'test')
        self.assertEqual(current_data['context'][1]['nombre'], 'test2')
        self.assertEqual(current_data['context'][0]['tipo'], 'PNG')
        self.assertEqual(current_data['context'][1]['tipo'], 'AVI')


class ComentarImagen(TestCase):
    def testComentarExistente(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        user2 = User.objects.create_user(username='test25', password='123456', email='test@test.com', first_name='test',
                                         last_name='T')
        perfil2 = Perfil.objects.create(id_conectate=124, usuario=user2, estado=1)
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.recurso = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1',
                                              descripcion=' ',
                                              autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([self.recurso])

        com_mul = ComentarioMultimedia.objects.create(x1=0, x2=1.1, y1=0, y2=2.2)

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/' + str(self.recurso.pk) + '/comentarios/'
        response = self.client.post(url, json.dumps(
            {
                "idTabla": com_mul.id,
                "usuario": user2.pk,
                "contenido": "hola",

            }), content_type='application/json')

        coment = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(coment['comentario_multimedia']['x1'], '0.00')
        self.assertEqual(coment['usuario']['usuario']['username'], 'test25')

    def testCrearComentario(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        user2 = User.objects.create_user(username='test23', password='123456', email='test@test.com', first_name='test',
                                         last_name='T')
        perfil2 = Perfil.objects.create(id_conectate=125, usuario=user2, estado=1)
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.recurso = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1',
                                              descripcion=' ',
                                              autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([self.recurso])

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/' + str(self.recurso.pk) + '/comentariosnuevos/'
        response = self.client.post(url, json.dumps(
            {
                "x1": 0,
                "x2": 1.1,
                "y1": 0,
                "y2": 2.2,
                "usuario": user2.pk,
                "contenido": "hola",

            }), content_type='application/json')

        coment = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(coment['comentario_multimedia']['x1'], '0.00')
        self.assertEqual(coment['usuario']['usuario']['username'], 'test23')

    def testListarComentarios(self):
        user = User.objects.create_user(username='test2', password='123456', email='test@test.com', first_name='test',
                                        last_name='T')
        user2 = User.objects.create_user(username='test25', password='123456', email='test@test.com', first_name='test',
                                         last_name='T')
        perfil2 = Perfil.objects.create(id_conectate=124, usuario=user2, estado=1)
        perfil = Perfil.objects.create(id_conectate=123, usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.recurso = Recurso.objects.create(nombre='test', tipo='PNG', archivo='url', thumbnail='url1',
                                              descripcion=' ',
                                              autor=perfil, usuario_ultima_modificacion=perfil)

        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion=' ',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)

        self.version = Version.objects.create(numero=1, red=self.red, creado_por=perfil, fecha_creacion='2019-03-20',
                                              imagen='https://i.pinimg.com/736x/3e/63/03/3e630381b8e25dda523301dc800c8c1d.jpg')

        self.version.recursos.set([self.recurso])

        self.com_mul = ComentarioMultimedia.objects.create(x1=0, x2=1.1, y1=0, y2=2.2)

        Comentario.objects.create(contenido='Hola que mas', version=self.version, recurso=self.recurso,
                                  usuario=perfil2, comentario_multimedia=self.com_mul)

        Comentario.objects.create(contenido='Hola que mas3', version=self.version, recurso=self.recurso,
                                  usuario=perfil2, comentario_multimedia=self.com_mul)

        Comentario.objects.create(contenido='Hola que mas2', version=self.version, recurso=self.recurso,
                                  usuario=perfil, comentario_multimedia=self.com_mul)

        url = '/api/versiones/' + str(self.version.pk) + '/recursos/' + str(self.recurso.pk) + '/listacomentarios/'

        response = self.client.get(url)
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data['context']), 3)
        self.assertEqual(current_data['context'][0]['contenido'], 'Hola que mas2')
        self.assertEqual(current_data['context'][1]['contenido'], 'Hola que mas3')
        self.assertEqual(current_data['context'][2]['contenido'], 'Hola que mas')


class ListarVersionesTestCase(TestCase):
    red = None

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion='la descripcion',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        Version.objects.create(es_final=False, numero=1, archivos='asd', red=self.red, creado_por=perfil)
        Version.objects.create(es_final=True, numero=2, archivos='asd2', red=self.red, creado_por=perfil)

    def test_respuesta_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_contar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(len(data), 2)

    def test_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['es_final'], False)
        self.assertEqual(data[1]['es_final'], True)
        self.assertEqual(data[0]['numero'], 1)
        self.assertEqual(data[1]['numero'], 2)
        self.assertEqual(data[0]['archivos'], 'asd')
        self.assertEqual(data[1]['archivos'], 'asd2')

    def test_creadores_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[1]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[0]['creado_por']['estado'], 1)
        self.assertEqual(data[1]['creado_por']['estado'], 1)
        self.assertEqual(data[0]['creado_por']['usuario']['username'], 'test')
        self.assertEqual(data[1]['creado_por']['usuario']['username'], 'test')

    def test_404_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk + 1) + '/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)


class VersionMarcarTestCase(TestCase):
    red = None

    def setUp(self):
        user = User.objects.create_user(username='test', password='sihdfnssejkhfse', email='test@test.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, estado=1)
        proyecto = ProyectoConectate.objects.create(id_conectate='1', nombre='MISO', codigo='1234',
                                                    fecha_inicio='2019-03-20', fecha_fin='2019-04-10')
        self.red = RED.objects.create(id_conectate='1', nombre='elRED', descripcion='la descripcion',
                                      tipo='video', solicitante='', proyecto_conectate=proyecto)
        Version.objects.create(es_final=False, numero=1, archivos='asd', red=self.red, creado_por=perfil)
        Version.objects.create(es_final=True, numero=2, archivos='asd2', red=self.red, creado_por=perfil)

    def test_respuesta_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_contar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(len(data), 2)

    def test_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['es_final'], False)
        self.assertEqual(data[1]['es_final'], True)
        self.assertEqual(data[0]['numero'], 1)
        self.assertEqual(data[1]['numero'], 2)
        self.assertEqual(data[0]['archivos'], 'asd')
        self.assertEqual(data[1]['archivos'], 'asd2')

    def test_creadores_versiones(self):
        url = '/api/reds/' + str(self.red.pk) + '/versiones/'
        response = self.client.get(url, format='json')
        data = json.loads(response.content)['context']
        self.assertEqual(data[0]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[1]['creado_por']['id_conectate'], '1')
        self.assertEqual(data[0]['creado_por']['estado'], 1)
        self.assertEqual(data[1]['creado_por']['estado'], 1)
        self.assertEqual(data[0]['creado_por']['usuario']['username'], 'test')
        self.assertEqual(data[1]['creado_por']['usuario']['username'], 'test')

    def test_404_listar_versiones(self):
        url = '/api/reds/' + str(self.red.pk + 1) + '/versiones/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)

    def testMarcarComoVersionFinalJustOne(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "1"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=1, es_final=False, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter = Version.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter.es_final, True)

    def testMarcarComoVersionFinalFirstMark(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "2"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2, es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1, es_final=False, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter1.es_final, False)
        self.assertEqual(versionMainAfter2.es_final, True)

    def testMarcarComoVersionFinalSecondMark(self):
        url1 = '/api/versiones/'
        url2 = '/marcar'
        versionId = "2"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=1, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=1, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=2, es_final=False, numero=2, red=red)
        versionMain = Version.objects.create(id=1, es_final=True, numero=1, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter1 = Version.objects.get(id=1)
        versionMainAfter2 = Version.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter1.es_final, False)
        self.assertEqual(versionMainAfter2.es_final, True)

    def testMarcarComoVersionLista(self):
        url1 = '/api/version-lista/'
        url2 = '/marcar'
        versionId = "2"
        url = url1 + versionId + url2

        fecha = datetime.datetime.now()
        proyecto = ProyectoConectate.objects.create(id=2, fecha_inicio=fecha, fecha_fin=fecha)
        red = RED.objects.create(id=2, proyecto_conectate=proyecto)
        versionMain = Version.objects.create(id=20, es_final=False, es_lista=False, numero=2, red=red)

        response = self.client.post(url, format='json')

        versionMainAfter = Version.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(versionMainAfter.es_lista, True)


class sisRedTestCase(TestCase):

    def test_login(self):
        username = "gl.pinto10@uniandes.edu.co"
        first_name = "first_name"
        last_name = "last_name"
        password = "Test12345"
        id_conectate = "1"
        numero_identificacion = "123455"
        user_model = User.objects.create_user(username=username, password=password, first_name=first_name,
                                              last_name=last_name, email=username)
        user_profile = Perfil.objects.create(usuario=user_model, id_conectate=id_conectate,
                                             numero_identificacion=numero_identificacion, estado=1)
        user_profile.save()
        response = self.client.post('/api/login/', json.dumps({"username": username, "password": password}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(current_data['token'])
        self.assertEqual(id_conectate, current_data['idConectate'])
        self.assertEqual(first_name, current_data['firstName'])
        self.assertEqual(last_name, current_data['lastName'])
        self.assertEqual(numero_identificacion,
                         current_data['numeroIdentificacion'])

    def test_cambiar_fase(self):
        # print("test_cambiar_fase")
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )
        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        fase2 = Fase.objects.create(
            id_conectate='3',
            nombre_fase='preproduccion',
        )
        response = self.client.put(
            '/api/red/' + str(red.id_conectate)
            + '/cambiarfase/' + str(fase2.id_conectate) + '/',
            content_type='application/json')

        # print("response", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_list_fases(self):
        url = '/api/fases/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_add_metadata_recurso_status(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)

        recurso = Recurso.objects.create(nombre='Recurso5', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-25',
                                         fecha_ultima_modificacion='2019-04-25', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = "Recurso5"

        recurso = Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                                         fecha_creacion='2019-04-11',
                                         fecha_ultima_modificacion='2019-04-11', tipo='jpg',
                                         descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)

        url = f'/api/buscarRecurso/?name={buscarNombre}'

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)

    def test_add_metadata_existente_recurso(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user, tipo_identificacion='CC',
                                       numero_identificacion='1234', estado=1)
        Recurso.objects.create(nombre='Recurso1', archivo='archivo1', thumbnail='thumbnail1',
                               fecha_creacion='2019-01-25',
                               fecha_ultima_modificacion='2019-01-25', tipo='jpg',
                               descripcion='descripcion1', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso2', archivo='archivo2', thumbnail='thumbnail1',
                               fecha_creacion='2019-02-25',
                               fecha_ultima_modificacion='2019-02-25', tipo='jpg',
                               descripcion='descripcion2', autor=perfil, usuario_ultima_modificacion=perfil)
        Recurso.objects.create(nombre='Recurso3', archivo='archivo3', thumbnail='thumbnail1',
                               fecha_creacion='2019-03-25',
                               fecha_ultima_modificacion='2019-03-25', tipo='jpg',
                               descripcion='descripcion3', autor=perfil, usuario_ultima_modificacion=perfil)

        buscarNombre = ""
        fecha_desde = "2019-01-01"
        fecha_hasta = "2019-02-28"

        url = f'/api/buscarRecurso/?name={buscarNombre}&fdesde={fecha_desde}&fhasta={fecha_hasta}'

        response = self.client.get(url, format='json')
        recursos = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(recursos), 2)

    def test_list_notificaciones_un_usuario(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(id_conectate=1, usuario=user, numero_identificacion='123',
                                       tipo_identificacion='CC', estado='1')
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )

        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='ASIGNAR_RED', descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(mensaje='prueba', fecha='2019-01-26', visto=False,
                                                   tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(
            id_conectate=1, estado=1, red=red, rol=rol, usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

    def test_numero_notificaciones_no_vistas(self):
        user = User.objects.create(username='user1', password='1234ABC', first_name='nombre1',
                                   last_name='apellido1', email='user@uniandes.edu.co')
        perfil = Perfil.objects.create(
            id_conectate=1, usuario=user, numero_identificacion='123', tipo_identificacion='CC', estado='1')
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='2', nombre='namepy',
                                                              nombre_corto='nameShort',
                                                              codigo='code', fecha_inicio='1999-12-19',
                                                              fecha_fin='2001-12-20')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )

        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio=None,
            fecha_cierre=None,
            porcentaje_avance=50,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=8,
            horas_trabajadas=7,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate=1, nombre='Productor')
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='ASIGNAR_RED', descripcion='El red fue asignado.')
        notificacion = Notificacion.objects.create(
            mensaje='prueba', fecha='2019-01-26', visto=False, tipo_notificacion=tipoNotificacion)
        notificacion2 = Notificacion.objects.create(
            mensaje='prueba2', fecha='2019-01-26', visto=True, tipo_notificacion=tipoNotificacion)

        rolAsignado = RolAsignado.objects.create(
            id_conectate=1, estado=1, red=red, rol=rol, usuario=perfil)
        rolAsignado.notificaciones.add(notificacion)
        rolAsignado.notificaciones.add(notificacion2)
        url = '/api/notificaciones/' + str(perfil.id_conectate) + '/novistos/'

        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_data, 1)

    def test_updateNotificaction(self):
        tipoNotificacion = NotificacionTipo.objects.create(
            nombre='nombre', descripcion='descripcion')
        notificationTest = Notificacion.objects.create(mensaje='texto', visto=False,
                                                       tipo_notificacion=tipoNotificacion)

        response = self.client.put('/api/putNotification/' + str(notificationTest.id) + '/',
                                   content_type='application/json')

        # print("response.content", response.content)
        dataRsp = json.loads(response.content)
        # print("dataRsp", dataRsp)

        self.assertEqual(
            dataRsp, {"mensaje": 'La notificacion ha sido actualizada'})

    def test_createNotification(self):
        # print("test_createNotification")
        proyecto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='name',
                                                              nombre_corto='nameShort',
                                                              codigo='123456', fecha_inicio='2020-09-01',
                                                              fecha_fin='2020-09-01')
        fase = Fase.objects.create(
            id_conectate='2',
            nombre_fase='produccion',
        )
        red = RED.objects.create(
            id_conectate='1',
            nombre='nombre',
            nombre_corto='nombre_corto',
            descripcion='descripcion',
            fecha_inicio='2020-09-01',
            fecha_cierre='2020-09-01',
            fecha_creacion='2019-09-01',
            porcentaje_avance=22,
            tipo='tipo',
            solicitante='solicitante',
            proyecto_conectate=proyecto_conectate,
            horas_estimadas=23,
            horas_trabajadas=11,
            fase=fase,
        )
        rol = Rol.objects.create(id_conectate='1', nombre='nombreROL')
        user_model = User.objects.create_user(
            username='username', password='password')
        user_model.first_name = 'first_name'
        user_model.last_name = 'last_name'
        user_model.email = 'email'
        user_profile = Perfil.objects.create(usuario=user_model, id_conectate='1', numero_identificacion='1022',
                                             estado=1)
        rol_asignado = RolAsignado.objects.create(id_conectate='1', estado=1, red=red, rol=rol,
                                                  usuario=user_profile)
        notificacionTipo = NotificacionTipo.objects.create(
            nombre='nombre', descripcion='descripcion')

        self.assertEqual(createNotification(red.id_conectate, notificacionTipo.pk),
                         {"mensaje": 'La notificacion ha sido creada'})


class RR02TestCase(TestCase):

    def test_get_version(self):
        url = '/api/get_version/'
        fecha_inicio = datetime.datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        proyectto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='prueba',
                                                               codigo='prueba', fecha_inicio=fecha,
                                                               fecha_fin=fecha)
        red = RED.objects.create(id_conectate='1', nombre='pruebaRED', descripcion='prueba',
                                 tipo='prueba', solicitante='prueba', proyecto_conectate=proyectto_conectate)
        version = Version.objects.create(numero=1, imagen='prueba', red=red, id=1)
        response = self.client.get(url, {'id': '1'})
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['nombre'], 'pruebaRED')
        self.assertEqual(current_data[1]['fields']['numero'], 1)

    def test_get_recursos(self):
        url = '/api/get_recursos_by_version/'
        fecha_inicio = datetime.datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime("2018-03-11", "%Y-%m-%d").date()
        proyectto_conectate = ProyectoConectate.objects.create(id_conectate='1', nombre='prueba',
                                                               codigo='prueba', fecha_inicio=fecha,
                                                               fecha_fin=fecha)
        red = RED.objects.create(id_conectate='1', nombre='pruebaRED', descripcion='prueba',
                                 tipo='prueba', solicitante='prueba', proyecto_conectate=proyectto_conectate)
        version = Version.objects.create(numero=1, imagen='prueba', red=red, id=1)
        user_model = User.objects.create_user(username='user1', password='1234ABC*', first_name='Usuario',
                                              last_name='uno', email='user1@coquito.com')
        perfil = Perfil.objects.create(id_conectate='1', usuario=user_model, estado=1)
        recurso = version.recursos.create(nombre='prueba', archivo='prueba', thumbnail='prueba',
                                          fecha_creacion=fecha_inicio,
                                          fecha_ultima_modificacion=fecha_inicio, tipo='prueba', descripcion='prueba',
                                          autor=perfil, usuario_ultima_modificacion=perfil)
        response = self.client.get(url, {'id': '1'})
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 1)


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

    def test_update_ready_state_red(self):
        red = RED.objects.create(id_conectate="S0001", nombre="null", nombre_corto="null", descripcion="1 video",
                                 fecha_inicio="2019-12-31", fecha_cierre="2019-12-31", fecha_creacion="2019-12-31",
                                 porcentaje_avance="0", tipo="Sin definir", solicitante="PR0011(Sandra)",
                                 horas_estimadas="0", horas_trabajadas="0", proyecto_conectate_id="1")

        response = self.client.put('/api/habilitar-red/' + str(red.id_conectate))
        current_data = json.loads(response.content)
        # print(current_data)

        self.assertEqual(current_data[0]['listo'], True)
