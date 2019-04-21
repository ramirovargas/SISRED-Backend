from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from psycopg2._psycopg import IntegrityError, DatabaseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from sisred_app.serializer import REDSerializer
from sisred_app.models import *
from django.core.serializers import *
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


"""
Vista para ver los detalles de un RED en donde se incluyen los recursos (GET)
Se usan archivos serializer para import de los modelos con los campos filtrados
"""

class ResorceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = '__all__'

def getRecurso(request, id):
    data = Recurso.objects.filter(id=id)
    if request.method == 'GET':
        serializer = ResorceSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)

"""
Vista para ver recursos asociados al RED (GET)
Se usan archivos serializer para import de los modelos con los campos filtrados
"""

class RedDetSerializer(serializers.ModelSerializer):
    recursos = ResorceSerializer(many=True)
    class Meta:
        model = RED
        fields = ('id_conectate', 'nombre', 'descripcion', 'recursos')

def getRedDetailRecursos(request, id):
    data = RED.objects.filter(id=id)
    if request.method == 'GET':
        serializer = RedDetSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)

"""
Vista para ver que usuario esta autenticado en el sistema SISRED (GET)
Se usan archivos serializer para import de los modelos con los campos filtrados
"""

class UserAutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')

def getUserAut(request):
    serializer = UserAutSerializer(request.user)
    return JsonResponse(serializer.data, safe=False)

"""
Vista para crear un usuario nuevo (POST)
Parametros: request (en el body se agregan los atributos del modelo de User y perfil)
Return: El usuario creado con su id en formato Json
"""
@csrf_exempt
def postUser(request):
    if request.method == 'POST':
        user_model = None
        try:
            json_user = json.loads(request.body)
            username = json_user['username']
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            password = json_user['password']
            email = json_user['email']
            id_conectate=json_user['id_conectate']
            numero_identificacion=json_user['numero_identificacion']
            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()
            user_profile = Perfil.objects.create(usuario=user_model, id_conectate=id_conectate, numero_identificacion=numero_identificacion, estado=1)
            user_profile.save()

            return HttpResponse(serialize("json", [user_model, user_profile]))
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except Exception as ex:
            if(user_model.id > 0):
                User.objects.filter(id=user_model.id).delete()
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )
"""
Vista para editar un usuario nuevo (PUT)
Parametros: request (en el body se agregan los atributos que se pueden modificar del modelo de User y perfil), id
Return: El usuario editado en formato Json
"""
@csrf_exempt
def putUser(request, id):
    if request.method == 'PUT':
        try:
            json_user = json.loads(request.body)
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            email = json_user['email']
            id_conectate=json_user['id_conectate']
            numero_identificacion = json_user['numero_identificacion']

            user = User.objects.get(id=id)
            perfil = Perfil.objects.get(usuario=id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            perfil.id_conectate = id_conectate
            perfil.numero_identificacion = numero_identificacion

            perfil.save()
            user.save()
            return HttpResponse(serialize("json",[user, perfil]))
        except ObjectDoesNotExist as e:
            return HttpResponseBadRequest(
                content='No existe el usuario con id ' + str(id)
            )
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

"""
Vista para consultar todos los usuarios (GET)
Parametros: request
Return: Lista de los usuarios con sus perfiles en formato Json
"""
@csrf_exempt
def getAllUser(request):
    try:
        usersAll = []
        users = User.objects.filter(is_superuser=False)
        for user in users:
            perfil = Perfil.objects.get(usuario=user)
            estado = ""
            if(perfil.estado == 0 ):
                estado = "Eliminado"
            elif perfil.estado == 1:
                estado = "Vigente"
            else:
                estado = "Inactivo"
            usersAll.append({"id":user.id, "username": user.username, "email":user.email,
                             "first_name":user.first_name, "lastname":user.last_name, "password":user.password,
                             "id_conectate": perfil.id_conectate, "numero_identificacion":perfil.numero_identificacion,
                             "estado":estado})
        return JsonResponse(usersAll, safe=False)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )


"""
Vista para consultar el usuario por id (GET)
Parametros: request, id
Return: Usuario con su perfil en formato Json
"""
@csrf_exempt
def getUser(request, id):
    try:
        user = User.objects.get(id=id)
        perfil = Perfil.objects.get(usuario=user)
        return HttpResponse(serialize("json", [user, perfil]))
    except ObjectDoesNotExist as e:
        return HttpResponseBadRequest(
            content='No existe el usuario con id ' + str(id)
        )
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )

"""
Vista para consultar los REDs relacionados a un id de ProyectoConectate (GET)
Parametros: request, id
Return: información del proyecto y una lista de los reds relacionados con su informacion en formato Json
"""
@csrf_exempt
def get_reds_relacionados(request, id):
    if request.method == 'GET':

        proyectoConectate_model = ProyectoConectate.objects.filter(pk=id).first()

        if proyectoConectate_model != None:
            reds_relacionados = []
            rol_model = Rol.objects.filter(nombre='Asesor').first()

            if rol_model != None:
                reds_models = RED.objects.filter(proyecto_conectate=proyectoConectate_model)

                for red in reds_models:
                    rolAsignado_model = RolAsignado.objects.filter(red=red).filter(rol=rol_model).first()

                    if rolAsignado_model != None:
                        perfil_model = Perfil.objects.get(pk=rolAsignado_model.usuario.id)
                        usuario_model = User.objects.get(pk=perfil_model.usuario.id)
                        nombreUsuario = usuario_model.first_name + " " + usuario_model.last_name

                        reds_relacionados.append(
                            {"idRed": red.pk, "nombreRed": red.nombre, "nombreCortoRed": red.nombre_corto,
                             "fechaCreacion": red.fecha_creacion, "tipo": red.tipo,
                             "asesor": nombreUsuario})

                    else:
                        return HttpResponseBadRequest(
                            content='No existe Rol Asesor asignado al red' + str(red.id)
                        )

                respuesta = {"nombreProyecto": proyectoConectate_model.nombre,
                             "nombreCortoProyecto": proyectoConectate_model.nombre_corto,
                             "redsRelacionados": reds_relacionados}

                return JsonResponse(respuesta, safe=False)

            return HttpResponseBadRequest(
                content='No existe Rol Asesor'
            )

        return HttpResponseBadRequest(
            content='No existe el proyecto conectate con id ' + str(id)
        )
"""
Servicio para actualizar o editar un registros del modelo RED (PUT)
Parametros: request (en el body se agregan los atributos del modelo de RED en formato json)
Return: 200 exitoso, 400 fallido explicando en un string el motivo del fallo.
"""
@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def update_sisred(request):

    print("update_sisred")

    if request.method == 'PUT':
        arrayMessages = []
        count = 0
        # Obtengo la lista de REDs del JSON
        json_data = json.loads(request.body)

        # Recorro el listado de REDS con la etiqueta RED
        for data in json_data["RED"]:
            count += 1
            id_conectate = data['id_conectate']
            print('id_conectate', id_conectate)

            try:
                #updateRed = RED.objects.get(id=1)  # debe ir el ID que se creo en el nuevo modelo
                print('updateRed')
                updateRed = RED.objects.filter(id_conectate=id_conectate).first()

                print("updateRed", updateRed.nombre)

                #json_data = json.loads(request.body)


                #updateRed.codigo=json_data['codigo']
                updateRed.nombre=data['nombre']
                updateRed.nombre_corto=data['nombre_corto']
                updateRed.descripcion=data['descripcion']
                updateRed.fecha_inicio = data['fecha_inicio']
                updateRed.fecha_cierre = data['fecha_cierre']
                #   fecha_creacion = json_data['fecha_creacion'],
                updateRed.porcentaje_avance=data['porcentaje_avance']
                updateRed.tipo=data['tipo']
                updateRed.solicitante=data['solicitante']
                #updateRed.proyecto_conectate=ProyectoConectate.objects.get(id=json_data['solicitante']),
                # recursos=res,
                # metadata=met,
                updateRed.horas_estimadas=data['horas_estimadas']
                updateRed.horas_trabajadas=data['horas_trabajadas']

                print("updateRed", updateRed.nombre)

                json_pyConectate = data['proyecto_conectate']
                namep = json_pyConectate['nombre']
                nameShort = json_pyConectate['nombre_corto']
                code = json_pyConectate['codigo']
                initDate = json_pyConectate['fecha_inicio']
                endDate = json_pyConectate['fecha_fin']
                id_conectatePC = json_pyConectate['id_conectate']
                print("endDate", endDate)

                try:
                    proyecto_conectate = ProyectoConectate.objects.get(id=updateRed.proyecto_conectate.id)
                except ProyectoConectate.DoesNotExist:
                    proyectoConectate = None
                    proyecto_conectate = ProyectoConectate.objects.create( id_conectate=id_conectatePC, nombre=namep, nombre_corto=nameShort, codigo=code,
                                                                  fecha_inicio=initDate, fecha_fin=endDate),

                updateRed.proyecto_conectate = proyecto_conectate
                #for Metadata in request..all():
                # met = Metadata.objects.create(tag='metadataTest2')
                # updateRed.metadata.add(met)
                # print("metadata")
                # updateRed.metadata.all()
                # print("met", newRED.metadata.all())

                try:
                    updateRed.save()
                    #json_metadata = json_data['metadata']
                    #tags = json_metadata['tag']
                    #print("Metadata.objects")
                    #met = Metadata.objects.get(id=updateRed.metadata.)
                    #met = updateRed.metadata.all()
                    #print("tags", len(tags))
                    #for tagData in tags :
                    #updateRed.metadata.add();
                    #updateRed.save()
                except IntegrityError as ie:
                    return HttpResponse("Integrity Error", status=400)
                except DatabaseError as e:
                    return HttpResponse("DatabaseError Error", status=400)
                except ValueError as ve:
                    print("ValueError", ve)
                    return HttpResponse("Error value saving", status=400)
                         #headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
                print("updateRed ok")


            except AttributeError:
                arrayMessages.insert(count, ' RED: Proyecto RED ' + updateRed.id_conectate + ' no existe ')
                return HttpResponse(arrayMessages, status=400)

        return HttpResponse("Updated successful", status=200)
    else:
        return HttpResponse("Bad request", status=400)

"""
Vista para eliminar el usuario por id (DELETE)
Parametros: request, id
Return: Usuario marcado como eliminado en formato Json
"""
@csrf_exempt
def deleteUser(request, id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
            perfil = Perfil.objects.get(usuario=user)
            perfil.estado = 0
            perfil.save()
            return HttpResponse(serialize("json", [user, perfil]))
        except ObjectDoesNotExist as e:
            return HttpResponseBadRequest(
                content='No existe el usuario con id ' + str(id)
            )
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )


"""
Vista para consultar los SISREDs
Parametros: request
Return: Lista de SISREDS creados en el sistema
"""
def get_red(request):
    data = RED.objects.all()
    if request.method == 'GET':
        serializer = REDSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


"""
Vista para Crear SISREDs
Parametros: request
Return: Lista en JSON indicando los codigos de REDs que fueron creados
        y los que no fueron creados
"""
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sisred_create(request):
    if request.method == 'POST':
        arrayMessages = []
        count = 0
        # Obtengo la lista de REDs del JSON
        json_data = json.loads(request.body)

        # Recorro el listado de REDS con la etiqueta RED
        for data in json_data["RED"]:
            count += 1
            id_conectate = data['id_conectate']
            print('id_conectate', id_conectate)

            try:
                red = RED.objects.filter(id_conectate=id_conectate).first()
                arrayMessages.insert(count, "RED: Proyecto RED " + red.id_conectate + " Ya existe ")
                continue
            except AttributeError:

                # Seteo los valores del proyecto Conectate
                json_pyConectate = data['proyecto_conectate']
                name = json_pyConectate['nombre']
                nameShort = json_pyConectate['nombre_corto']
                code = json_pyConectate['codigo']
                initDate = json_pyConectate['fecha_inicio']
                endDate = json_pyConectate['fecha_fin']
                id_conectatePC = json_pyConectate['id_conectate']

                # Verifico si el proyecto conectate no existe en la base de datos
                try:
                    proyecto_conectate = ProyectoConectate.objects.filter(id_conectate=id_conectatePC).first()
                    print(proyecto_conectate.nombre)
                except AttributeError:
                    proyecto_conectate = ProyectoConectate.objects.create(id_conectate=id_conectatePC, nombre=name, nombre_corto=nameShort,
                                                                          codigo=code, fecha_inicio=initDate,
                                                                          fecha_fin=endDate)

                # seteo un nuevo objeto RED
                newRED = RED(
                    id_conectate=data['id_conectate'],
                    nombre=data['nombre'],
                    nombre_corto=data['nombre_corto'],
                    descripcion=data['descripcion'],
                    fecha_inicio=data['fecha_inicio'],
                    fecha_cierre=data['fecha_cierre'],
                    fecha_creacion=data['fecha_creacion'],
                    porcentaje_avance=data['porcentaje_avance'],
                    tipo=data['tipo'],
                    solicitante=data['solicitante'],
                    proyecto_conectate=proyecto_conectate,

                    horas_estimadas=data['horas_estimadas'],
                    horas_trabajadas=data['horas_trabajadas'],
                )
                newRED.save()
                arrayMessages.insert(count, " RED: Proyecto RED creado correctamente: " + id_conectate)
                print("newRED create", newRED.nombre)

        # return HttpResponse(arrayMessages)

        return HttpResponse(json.dumps(arrayMessages), content_type="application/json")


"""
Vista para eliminar una lista de SISREDs
Parametros: request
Return: SISREDs que fueron eliminados y los que no
"""
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sisred_remove(request):
    if request.method == 'POST':

        arrayMessages = []
        count = 0
        # Obtengo la lista de REDs del JSON
        json_data = json.loads(request.body)

        # Recorro el listado de REDS con la etiqueta RED
        for data in json_data["RED"]:
            # verificar primero que exista
            count += 1
            id_conectate = data['id_conectate']
            print('id_conectate', id_conectate)

            try:
                red = RED.objects.filter(id_conectate=id_conectate).first()
                print(red.nombre)
                if red.borrado:
                    arrayMessages.insert(count, 'Proyecto RED ' + id_conectate + ' Ya se encuentra eliminado')
                else:
                    RED.objects.filter(id_conectate=id_conectate).update(borrado=True)
                    arrayMessages.insert(count, 'Proyecto RED ' + id_conectate + ' Eliminado correctamente')
                continue
            except AttributeError:
                arrayMessages.insert(count, 'Proyecto RED ' + id_conectate + ' No Existe en SISRED')

        return HttpResponse(json.dumps(arrayMessages), content_type="application/json")

"""
Vista para crear una nueva asignación (POST)
Parametros: request (se deben incluir todos los campos del RolAsignado, incluyendo el id del red, del rol y del usuario)
Return: Un mensaje de confirmación
"""
@csrf_exempt
def postRolAsignado(request):
    if request.method == 'POST':
        error = ''
        try:
            json_rol_asignado = json.loads(request.body)
            id_conectate = json_rol_asignado['id_conectate']
            id_red = json_rol_asignado['id_red']
            id_usuario = json_rol_asignado['id_usuario']
            id_rol = json_rol_asignado['id_rol']
            notificaciones = json_rol_asignado['notificaciones']

            rol_asignado_existente = RolAsignado.objects.filter(id_conectate=id_conectate).first()

            if rol_asignado_existente == None:
                perfil = Perfil.objects.filter(id_conectate=id_usuario).first()

                if perfil != None:
                    rol = Rol.objects.filter(id_conectate=id_rol).first()
                    if rol != None:
                        red = RED.objects.filter(id_conectate=id_red).first()
                        if red != None:
                            rol_asignado = RolAsignado.objects.create(id_conectate=id_conectate, estado=1, red=red,
                                                                      rol=rol, usuario=perfil)

                            for notificacion in notificaciones:
                                rol_asignado.notificaciones.create(mensaje=notificacion['mensaje'],
                                                                   fecha=notificacion['fecha'])

                            mensaje = {"mensaje": 'El rol asignado ha sido creado'}
                            return HttpResponse(json.dumps(mensaje))
                        else:
                            error = {"error": 'No hay un RED con el id ' + str(id_red)}
                            return HttpResponseBadRequest(json.dumps(error))
                    else:
                        error = {"error": 'No hay un rol con el id ' + str(id_rol)}
                        return HttpResponseBadRequest(json.dumps(error))
                else:
                    error = {"error": 'No hay un perfil con el id ' + str(id_usuario)}
                    return HttpResponseBadRequest(json.dumps(error))
            else:
                error = {"error": 'Ya existe un rol asignado con el id ' + str(id_conectate)}
                return HttpResponseBadRequest(json.dumps(error))
        except KeyError as e:
            error = {"error": 'El campo ' + str(e) + ' es requerido.'}
            return HttpResponseBadRequest(json.dumps(error))
        except Exception as ex:
            error = {"errorInfo": 'Error: ' + str(ex), "error": "Se presentó un error realizando la petición"}
            return HttpResponseBadRequest(json.dumps(error))

"""
Vista para actualziar una asignación (PUT)
Parametros: request (se deben incluir todos los campos del RolAsignado, incluyendo el id del red, del rol y del usuario) y id del rol asignado
Return: Un mensaje de confirmación
"""
@csrf_exempt
def putRolAsignado(request, id):
    if request.method == 'PUT':
        error = ''
        try:
            json_rol_asignado = json.loads(request.body)

            id_red = json_rol_asignado['id_red']
            id_usuario = json_rol_asignado['id_usuario']
            id_rol = json_rol_asignado['id_rol']
            estado = json_rol_asignado['estado']
            notificaciones = json_rol_asignado['nuevasNotificaciones']

            rol_asignado_existente = RolAsignado.objects.get(id_conectate=id)

            print(rol_asignado_existente)

            if rol_asignado_existente != None and rol_asignado_existente.estado != 0:
                perfil = Perfil.objects.filter(id_conectate=id_usuario).first()

                if perfil != None:
                    rol = Rol.objects.filter(id_conectate=id_rol).first()
                    if rol != None:
                        red = RED.objects.filter(id_conectate=id_red).first()
                        if red != None:
                            if estado == 1 or estado == 2:
                                rol_asignado_existente.perfil = perfil
                                rol_asignado_existente.rol = rol
                                rol_asignado_existente.red = red
                                rol_asignado_existente.estado = estado

                                rol_asignado_existente.notificaciones.remove()

                                for notificacion in notificaciones:
                                    rol_asignado_existente.notificaciones.create(mensaje=notificacion['mensaje'],
                                                                                 fecha=notificacion['fecha'])

                                rol_asignado_existente.save()
                                mensaje = {"mensaje": 'El rol asignado ha sido actualizado'}
                                return HttpResponse(json.dumps(mensaje))
                            else:
                                error = {"error": 'El estado solo puede ser 1 o 2'}
                                return HttpResponseBadRequest(json.dumps(error))
                        else:
                            error = {"error": 'No hay un RED con el id ' + str(id_red)}
                            return HttpResponseBadRequest(json.dumps(error))
                    else:
                        error = {"error": 'No hay un rol con el id ' + str(id_rol)}
                        return HttpResponseBadRequest(json.dumps(error))
                else:
                    error = {"error": 'No hay un perfil con el id ' + str(id_usuario)}
                    return HttpResponseBadRequest(json.dumps(error))
            else:
                error = {"error": 'No existe un rol asignado con el id ' + str(id)}
                return HttpResponseBadRequest(json.dumps(error))
        except KeyError as e:
            error = {"error": 'El campo ' + str(e) + ' es requerido.'}
            return HttpResponseBadRequest(json.dumps(error))
        except Exception as ex:
            error = {"errorInfo": 'Error: ' + str(ex), "error": "Se presentó un error realizando la petición"}
            return HttpResponseBadRequest(json.dumps(error))

"""
Vista para eliminar un rol asignado (DELETE)
Parametros: request, id
Return: Mensaje que indica que el rol asignado fue eliminado
"""
@csrf_exempt
def deleteRolAsignado(request, id):
    if request.method == 'DELETE':
        try:
            rol_asignado_existente = RolAsignado.objects.filter(id_conectate=id).first()
            if rol_asignado_existente != None and rol_asignado_existente.estado != 0:
                rol_asignado_existente.estado = 0
                rol_asignado_existente.save()
                mensaje = {"mensaje": 'El rol asignado ha sido borrado'}
                return HttpResponse(json.dumps(mensaje))
            else:
                error = {"error": 'No existe un rol asignado con id ' + str(id)}
                return HttpResponseBadRequest(json.dumps(error))
        except ObjectDoesNotExist as e:
            error = {"error": 'No existe un rol asignado con id ' + str(id)}
            return HttpResponseBadRequest(json.dumps(error))
        except Exception as ex:
            error = { "error": "Se presentó un error realizando la petición" + str(ex)}
            return HttpResponseBadRequest(json.dumps(error))

