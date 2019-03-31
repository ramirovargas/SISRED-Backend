from .models import Recurso, RED
from rest_framework import  serializers

class RecursoSerializer(serializers.ModelSerializer):
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
    subproductos_del_red=serializers.StringRelatedField(many=True)
    class Meta:
        model=RED
        fields=('codigo','fase','subproductos_del_red')