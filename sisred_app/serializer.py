from .models import Recurso, RED, Metadata, Fase, ProyectoConectate
from rest_framework import  serializers

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Metadata
        fields=('id','tag')

class RecursoSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(many=True, read_only=True)
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','fecha_creacion','fecha_ultima_modificacion','tipo','descripcion','metadata','autor','usuario_ultima_modificacion','getAutor','getResponsableModificacion')

class RecursoSerializer_post(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','archivo','thumbnail','tipo','descripcion','autor')

class RecursoSerializer_put(serializers.ModelSerializer):
    class Meta:
        model=Recurso
        fields=('nombre','descripcion','usuario_ultima_modificacion')

class FaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fase
        fields=('id_conectate','nombre_fase')
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProyectoConectate
        fields=('nombre','codigo')

class REDSerializer(serializers.ModelSerializer):

    class Meta:
        model=RED
        fields=('codigo','nombre','fecha_inicio','fecha_cierre','fecha_creacion','porcentaje_avance','tipo','fase','getFase','getProyecto','proyecto_conectate')
