import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from sisred_app.models import Perfil, RED, Version, Recurso, Comentario, ComentarioMultimedia, ComentarioPDF, ProyectoConectate


class SisredTestCase(TestCase):
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
            print(current_data)

            self.assertEqual(current_data[0]['listo'], True)

    def test_get_comentario_pdf(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")
        proyectoConectate= ProyectoConectate.objects.create(id_conectate="1", nombre="test", codigo="123", fecha_inicio="2019-12-31", fecha_fin="2019-12-31")
        red = RED.objects.create( id_conectate="S0001", nombre="null", nombre_corto="null", descripcion="1 video", fecha_inicio="2019-12-31", fecha_cierre="2019-12-31", fecha_creacion="2019-12-31", porcentaje_avance="0", tipo="Sin definir", solicitante="PR0011(Sandra)", horas_estimadas="0", horas_trabajadas="0", proyecto_conectate=proyectoConectate)
        version = Version.objects.create(numero=1, archivo="prueba", red=red)
        recurso = Recurso.objects.create(nombre="test",archivo="test",thumbnail="test",tipo="test",descripcion="test",autor=profile1,usuario_ultima_modificacion=profile1)
        comentario = Comentario.objects.create(usuario=profile1, version=version, recurso=recurso,  contenido="prueba")
        comMultimedia = ComentarioMultimedia.objects.create(x1=121, x2=121, y1=121, y2=121, comentario=comentario)
        comPDF= ComentarioPDF.objects.create(height=123,width=123,comentario_multimedia=comMultimedia)
        id = recurso.id

        response = self.client.get('/api/comentarios/pdf/'+str(id)+'/')
        current_data = json.loads(response.content)
        print(current_data)

        self.assertEqual(current_data[0]['comentario'], "prueba")

    def test_post_comentario_pdf(self):
        user_model1 = User.objects.create_user(username='test1', password='kd8wke-DE34', first_name='test1',
                                               last_name='test1', email='test1@test.com')

        profile1 = Perfil.objects.create(usuario=user_model1, numero_identificacion="1100960499", estado="1")
        proyectoConectate = ProyectoConectate.objects.create(id_conectate="1", nombre="test", codigo="123",
                                                             fecha_inicio="2019-12-31", fecha_fin="2019-12-31")
        red = RED.objects.create(id_conectate="S0001", nombre="null", nombre_corto="null", descripcion="1 video",
                                 fecha_inicio="2019-12-31", fecha_cierre="2019-12-31", fecha_creacion="2019-12-31",
                                 porcentaje_avance="0", tipo="Sin definir", solicitante="PR0011(Sandra)",
                                 horas_estimadas="0", horas_trabajadas="0", proyecto_conectate=proyectoConectate)
        version = Version.objects.create(numero=1, archivo="prueba", red=red)
        recurso = Recurso.objects.create(nombre="test", archivo="test", thumbnail="test", tipo="test",
                                         descripcion="test", autor=profile1, usuario_ultima_modificacion=profile1)

        coordenadas = {"x1": 142432,"x2": 134234,"y1": 142432,"y2": 142432,"width": 200,"height": 300}
        data={"rutaPdf": "http://www.orimi.com/pdf-test.pdf",
              "usuario":profile1.id,
              "version":version.id,
              "recurso":recurso.id,
              "coordenadas":coordenadas,
              "comentario": "contenido"}
        js=json.dumps(data)
        print(js)
        response = self.client.post('/api/comentarios/pdf/',js,'application/json')

        self.assertEqual(response.status_code, 201)

