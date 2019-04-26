from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from sisred_app.models import RED, ProyectoRED, RolAsignado, Perfil, Metadata, Recurso, ProyectoConectate, HistorialFases
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your views here.

# Metodo para agregar un proyecto RED
@csrf_exempt
def post_proyecto_red(request):
    if request.method == 'POST':
        json_proyecto_red = json.loads(request.body)
        red = RED.objects.get(id=json_proyecto_red['RED'])
        nuevo_proyecto_red = ProyectoRED(
            nombre=json_proyecto_red['nombre'],
            tipo=json_proyecto_red['tipo'],
            carpeta=json_proyecto_red['carpeta'],
            descripcion=json_proyecto_red['descripcion'],
            autor=json_proyecto_red['autor'],
            red=red)
        nuevo_proyecto_red.save()
        return HttpResponse(serializers.serialize("json", [nuevo_proyecto_red]))

# Metodo para obtener detalle de las personas asignadas al RED
@csrf_exempt
def get_detallered_personas(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        personas = RolAsignado.objects.filter(red=red)
        respuesta = []
        for persona in personas:
            usuario = persona.usuario.usuario
            nombre= usuario.first_name + " " + usuario.last_name
            rol = persona.rol.nombre
            respuesta.append({"name": nombre, "rol": rol})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle de proyectos RED
@csrf_exempt
def get_detallered_proyectosred(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        proyectos = ProyectoRED.objects.filter(red=red)
        respuesta = []
        for pro in proyectos:
            respuesta.append({"id": pro.pk, "name": pro.nombre, "autor": pro.autor, "typeFile": pro.tipo, "createdDate": red.fecha_creacion.strftime('%Y/%m/%d'),"description":pro.descripcion})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle de los metadatas del RED
@csrf_exempt
def get_detallered_metadata(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        metas = Metadata.objects.filter(red=red)
        respuesta = []
        for met in metas:
            respuesta.append({"id": met.pk, "tag": met.tag})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle de los recursos asociados al RED
@csrf_exempt
def get_detallered_recursos(request):
    if request.method == 'GET':
        red = RED.objects.get(id=request.GET['RED'])
        recursos = Recurso.objects.filter(red=red)
        respuesta = []
        for re in recursos:
            respuesta.append({"id": re.pk, "name": re.nombre, "typeFormat": re.tipo})
        return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener detalle del RED
@csrf_exempt
def get_detallered(request):
    if request.method == 'GET':
        red = request.GET['RED']
        red = RED.objects.get(id=red)
        nombreRed = red.nombre
        url = 'conectatePrueba.com/'+nombreRed
        status = 'No tiene'
        nombreProject = red.proyecto_conectate.nombre
        historiales = HistorialFases.objects.filter(red=red.pk)

        if len(historiales) > 1:
            ultimo = historiales[0]
            ultimoDate = datetime.date(datetime(1800,1,1))
            for hist in historiales :
                datAct = hist.fecha_cambio
                actDate = hist.fecha_cambio
                if datAct > ultimoDate:
                    ultimo = hist
                    ultimoDate = actDate
            status = ultimo.estado.nombre_estado

        respuesta = {"nombreRed": nombreRed, "nombreProject":nombreProject, "status":status, "url": url}

    return HttpResponse(json.dumps(respuesta), content_type="application/json")

# Metodo para obtener los REDs asignados
@csrf_exempt
def get_reds_asignados(request, id):
    if request.method == 'GET':
        usuario = User.objects.get(pk=id);
        nombreUsuario = usuario.first_name + " " + usuario.last_name
        perfil = Perfil.objects.get(usuario=usuario);
        reds_asignados = []
        rolesAsignado = RolAsignado.objects.filter(usuario=perfil)
        for rolAsignado in rolesAsignado:
            red = rolAsignado.red
            rol = rolAsignado.rol.nombre
            reds_asignados.append({"idRed": red.pk, "nombreRed": red.nombre_corto, "rol": rol})
        respuesta = {"nombreUsuario": nombreUsuario, "redsAsignados": reds_asignados}
        return JsonResponse(respuesta, safe=False)
