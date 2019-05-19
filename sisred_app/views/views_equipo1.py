import json

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
import json
import datetime
import requests

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from sisred_app.models import Recurso, RED, Perfil, Fase, HistorialFases, Version, Comentario, ComentarioMultimedia, ProyectoConectate
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


#Autor:         Ramiro Vargas
#Fecha:         2019-04-22
#Parametros:    id_conectate -> Id del RED
#Descripcion:   Funcionalidad para actualizar cuando un RED esta listo para revision

@api_view(['GET','PUT'])
def getREDByIdentification(request, id_conectate):
    reds=[]
    try:
        red = RED.objects.get(id_conectate=id_conectate)
    except RED.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    if request.method == 'PUT':

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
    if request.method == 'GET':
        return Response(makeReds(red))

def makeReds(red):

    reds = []

    reds.append({"listo": red.listo})

    return reds

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


#Autor:         Ramiro Vargas
#Fecha:         2019-05-13
#Parametros:    idVersion -> Id dVersion PyS

#Descripcion:   Funcionalidad para marcar version
@csrf_exempt
def marcarVersionLista(request,id):
    if request.method == 'POST':
        version = get_object_or_404(Version, id=id)

        otherVersions = get_list_or_404(Version, red_id = version.red_id)
        for v in otherVersions:
            v.es_lista=False
            v.save()

        version.es_lista = True
        version.save()
        return JsonResponse(str(id), safe=False)
    return HttpResponseNotFound()
#Autor:         Alejandro Garcia
#Fecha:         2019-05-08
#Parametros:    idRed -> Id del RED
#Descripcion:   Funcionalidad para obtener el avance de un  RED

@api_view(['GET','PUT'])
def getAvanceRED(request, idRED):
    fases=[]
    lista_fases=[]
    recursos = []

    if request.method == 'GET':
        try:
            red = RED.objects.get(id=idRED)
            fecha = red.fecha_inicio
            primera_fecha = True
            proyecto_conectate = ProyectoConectate.objects.get(id=red.proyecto_conectate.id)
        except RED.DoesNotExist:
            raise NotFound(detail="Error 404, RED not found", code=404)

        lista_fases = HistorialFases.objects.filter(red=idRED)
        lista_fases.order_by('fecha_cambio')
        recursos = red.recursos.all()
        recursos.order_by('-fecha_creacion')
        ultimoRecurso = recursos[0]
        uhmodificacion = ultimoRecurso.fecha_creacion
        tamaño = lista_fases.__len__()
        count = 0
        for fase in lista_fases:
            fs = Fase.objects.get(id=fase.id)
            fecha_final = "null"
            fecha_inicial = fase.fecha_cambio
            if(count+1<tamaño):
                fecha_final = lista_fases[count+1].fecha_cambio
            fases.append({"fase": fs.nombre_fase, "fechaInicio": fecha_inicial, "fechaFinal": fecha_final, "comentario": fase.comentario})
            count=count+1

        jsonObject ={"id": red.id,"nombre": red.nombre, "proyecto": proyecto_conectate.nombre, "uhmodificacion": uhmodificacion, "fases":fases}
        return Response(jsonObject)
