from django.contrib.auth.models import User
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
import datetime


from sisred_app.models import Recurso, RED, Perfil
from sisred_app.serializer import RecursoSerializer, FaseSerializer, RecursoSerializer_post, RecursoSerializer_put, \
    REDSerializer




#Autor: Francisco Perneth
#Fecha: 2019-03-30
#Parametros:
#    Request -> Datos de la solicitud
#Descripcion:
#   Permite registrar un recurso
@api_view(['POST'])
def recurso_post(request):
    autor = Perfil.objects.get(id=int(request.data.get("autor")))
    idRed = request.data.get("idRed")
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
    IdRecurso=rec.id

    Red=RED.objects.get(id=idRed)
    if (Red!=None):
        Red.recursos.add(rec)
        return Response(request.data, status=status.HTTP_201_CREATED)

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
    usuario_perfil = []

    try:
        perfil = Perfil.objects.get(numero_identificacion=numero_identificacion)
    except Perfil.DoesNotExist:
        raise NotFound(detail="Error 404, User not found", code=404)

    usuario = User.objects.get(username=perfil.usuario)

    if request.method == 'GET':

        usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                               "first_name": usuario.first_name, "lastname": usuario.last_name,
                               "numero_identificacion": perfil.numero_identificacion,
                               "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

        return Response(usuario_perfil)

    elif request.method == 'PUT':

        perfil.estado_sisred = 1
        perfil.save()

        usuario_perfil.append({"username": usuario.username, "email": usuario.email,
                               "first_name": usuario.first_name, "lastname": usuario.last_name,
                               "numero_identificacion": perfil.numero_identificacion,
                               "estado": perfil.estado, "estado_sisred": perfil.estado_sisred})

        return Response(usuario_perfil)