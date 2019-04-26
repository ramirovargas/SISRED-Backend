import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
import datetime
import requests

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from sisred_app.models import Recurso, RED, Perfil, Fase, HistorialFases
from sisred_app.serializer import RecursoSerializer, RecursoSerializer_post, RecursoSerializer_put, \
     REDSerializer




#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite registrar un recurso
@api_view(['POST'])
def recurso_post(request):
    serializer = RecursoSerializer_post(data=request.data)
    if serializer.is_valid():
        autor = Perfil.objects.get(id=int(request.data.get("autor")))

        rec = Recurso.objects.create(nombre=request.data.get('nombre'),
                                     archivo=request.data.get('archivo'),
                                     thumbnail=request.data.get('thumbnail'),
                                     descripcion=request.data.get('descripcion'),
                                     tipo=request.data.get('tipo'),
                                     autor=autor,
                                     usuario_ultima_modificacion=autor
                                     )
        rec.fecha_creacion=datetime.datetime.now()
        rec.fecha_ultima_modificacion = datetime.datetime.now()
        rec.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para obtener
#Descripcion:
#   Permite consultar un recurso mediante su identificador (id)
@api_view(['GET'])
def recurso_get(request,id):
    recurso = Recurso.objects.filter(id=id).first()
    if(recurso==None):
        raise NotFound(detail="Error 404, recurso not found", code=404)
    serializer = RecursoSerializer(recurso)
    return Response(serializer.data)

#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite modificar un recurso mediante.
#   los datos permitios a modificar son: nombre y descripción. la fecha y usaurio de la modificación son valores tomados de
#   el usuario que está realizando la operación (auntenticado en el sistema) y la fecha del sistema.
@api_view(['PUT'])
def recurso_put(request):
    serializer = RecursoSerializer_put(data=request.data)
    if serializer.is_valid():
        id=int(request.data.get("id"))
        ItemRecurso = Recurso.objects.filter(id=id).first()
        if (ItemRecurso==None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        ItemRecurso.nombre=request.data.get("nombre")
        ItemRecurso.descripcion=request.data.get("descripcion")
        Per=Perfil.objects.get(id=int(request.data.get("usuario_ultima_modificacion")))
        if (Per!=None):
            ItemRecurso.usuario_ultima_modificacion=Per
        ItemRecurso.fecha_ultima_modificacion=datetime.datetime.now()
        ItemRecurso.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Autor: Ramiro Vargas
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#    id -> id del recurso para consultar
#Descripcion:
#   Permite consultar  la información de un RED, especialmente información del avance
@api_view(['GET', 'POST'])
def fase_byid(request,id):
    if request.method == 'GET':
        red = RED.objects.filter(id=id)
        if (red == None):
            raise NotFound(detail="Error 404, recurso not found", code=404)
        print(red)
        serializer = REDSerializer(red, many=True)
        return Response(serializer.data)


#Autor:         Adriana Vargas
#Fecha:         2019-04-11
#Parametros:    request -> Datos de la solicitud
#               numero_identificacion -> número de identificación del usuario
#Descripcion:   Permite consultar la información de un usuario con su número de identificación y actualizar el estado del mismo en sisred

@api_view(['GET', 'PUT'])
def getUserByIdentification(request, numero_identificacion):

    try:
        perfil = Perfil.objects.get(numero_identificacion=numero_identificacion)
    except Perfil.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    usuario = User.objects.get(username=perfil.usuario)

    if request.method == 'GET':

        return Response(usuarioPerfilJson(perfil, usuario))

    elif request.method == 'PUT':

        perfil.estado_sisred = 1
        perfil.save()

        return Response(usuarioPerfilJson(perfil, usuario))

def usuarioPerfilJson(perfil, usuario):

    usuario_perfil = []

    usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                           "first_name": usuario.first_name, "lastname": usuario.last_name,
                           "numero_identificacion": perfil.numero_identificacion,
                           "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

    return usuario_perfil

@api_view(['GET', 'PUT'])
def getREDByIdentification(request, id_conectate):
    reds=[]
    try:
        red = RED.objects.get(id_conectate=id_conectate)
    except RED.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    if request.method == 'GET':
        serializer = REDSerializer(red, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':

        red.listo=True
        red.save()
        reds.append({"nombre": red.nombre, "nombre_corto": red.nombre_corto,
                    "descripcion": red.descripcion, "fecha_inicio": red.fecha_inicio,
                    "fecha_cierre": red.fecha_cierre,
                    "fecha_creacion": red.fecha_creacion, "porcentaje_avance": red.porcentaje_avance,
                    "tipo": red.tipo, "solicitante": red.solicitante,
                    "horas_estimadas": red.horas_estimadas, "horas_trabajadas": red.horas_trabajadas,
                    "proyecto_conectate_id": red.proyecto_conectate_id,
                    "listo": True})
        return Response(reds)


'''Codigo extraido de la rama E4-GR-02_Cambiar_de_fase_al_RED
se debe borrar al hacer la integración

Vista para cambiar fase de un red (PUT)
Parametros: request, id del red, id de la fase'''

@api_view(['PUT'])
def putCambiarFaseRed(request1, idRed, idFase):
    if request1.method == 'PUT':
        try:
            red = RED.objects.get(id_conectate=idRed)
            fase = Fase.objects.get(id_conectate=idFase)

            idActual = int(red.fase.id_conectate)

            print("putCambiarFaseRed", idActual, idFase)
            if (idFase > (idActual + 1)) | (idFase < (idActual - 1)):
                error = 'Debe seleccionar una fase consecutiva para poder hacer el cambio'
                return HttpResponseBadRequest(content=error, status=HTTP_400_BAD_REQUEST)

            red.fase = fase
            red.save()

            # Llamado a la funcion de sincronizarFases
            sincronizarFases(idRed, idActual, idFase)

            historialFase = HistorialFases.objects.create(fase=fase, red=red)
            historialFase.save()

            return HttpResponse(status=HTTP_200_OK)
        except ObjectDoesNotExist as e:
            if (e.__class__ == Fase.DoesNotExist):
                error = 'No existe la fase con id ' + str(idFase)
            else:
                error = 'No existe el red con id ' + str(idRed)
            return HttpResponseBadRequest(content=error, status=HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

#Autor:         Adriana Vargas
#Fecha:         2019-04-22
#Parametros:    idRed -> Id del RED en el sistema de PyS
#               idActual -> Id de la fase actual del RED
#               idFase -> Id de la nueva fase del RED
#Descripcion:   Funcionalidad para sincronizar el cambio de fase con el sistema de PyS

def sincronizarFases(idRed, idActual, idFase):
    url = 'http://sincronizar-red.mocklab.io/cambioFase'
    data = {"id_conectate": idRed, "fase_actual": idActual, "nueva_fase": idFase}
    response = requests.post(url, data=json.dumps(data))
    print(response)

    return Response(response)