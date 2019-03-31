from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_identificacion = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=50)

    def __str__(self):
        return "Rol: " + self.usuario


class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Notificacion: ' + self.mensaje


class Metadata(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return "Metadata: " + self.tag


class Recurso(models.Model):
    nombre = models.CharField(max_length=200)
    archivo = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    fecha_creacion = models.DateField(default=datetime.date.today)
    fecha_ultima_modificacion = models.DateField(default=datetime.date.today)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    metadata = models.ManyToManyField(Metadata,blank=True)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='usuario_autor')
    usuario_ultima_modificacion = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='usuario_ultima_modificacion')

    def __str__(self):
        return "Recurso: " + self.nombre

    @property
    def getAutor(self):
        return self.autor.usuario.first_name + " "  + self.autor.usuario.last_name

    @property
    def getResponsableModificacion(self):
        return self.autor.usuario.first_name + " " + self.autor.usuario.last_name


class ProyectoConectate(models.Model):
    nombre = models.CharField(max_length=200)
    nombre_corto = models.CharField(max_length=50, blank=True, null=True)
    codigo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


    def __str__(self):
        return 'Proyecto conectate: ' + self.nombre

class Fase(models.Model):
    id_conectate = models.CharField(max_length=50)
    nombre_fase = models.CharField(max_length=50)

    def __str__(self):
        return 'Fase: ' + self.nombre_fase
class RED(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    nombre_corto = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    porcentaje_avance = models.IntegerField()
    tipo = models.CharField(max_length=50)
    solicitante = models.CharField(max_length=50)
    proyecto_conectate = models.ForeignKey(ProyectoConectate, on_delete=models.CASCADE)
    recursos = models.ManyToManyField(Recurso)
    metadata = models.ManyToManyField(Metadata)
    horas_estimadas = models.IntegerField()
    horas_trabajadas = models.IntegerField()
    fase = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Red: ' + self.codigo

    @property
    def getFase(self):
            return self.fase.nombre_fase

    @property
    def getProyecto(self):
        return self.proyecto_conectate.nombre


class SubproductoRED(models.Model):
    red = models.ForeignKey(RED, on_delete=models.CASCADE, related_name='subproductos_del_red')
    subproducto = models.ForeignKey(RED, on_delete=models.CASCADE, related_name='reds_del_subproducto')


class ProyectoRED(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50)
    carpeta = models.CharField(max_length=200)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return "Proyecto RED: " + self.nombre



class Estado(models.Model):
    nombre_estado = models.CharField(max_length=50)

    def __str__(self):
        return 'Estado: ' + self.nombre_estado


class HistorialEstados(models.Model):
    fecha_cambio = models.DateField(default=datetime.date.today)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return 'Fecha de cambio: ' + self.fecha_cambio + ', Estado: ' + self.estado + ', Red: ' + self.red


class Version(models.Model):
    es_final = models.BooleanField(default=False)
    numero = models.IntegerField()
    archivo = models.CharField(max_length=200)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return 'Version: ' + self.numero


class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "Rol: " + self.nombre


class RolAsignado(models.Model):
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(blank=True, null=True)
    notificaciones = models.ManyToManyField(Notificacion)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)


class Comentario(models.Model):
    contenido = models.TextField()
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, blank=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    def __str__(self):
        return 'Comentario: ' + self.contenido


class Propiedad(models.Model):
    llave = models.CharField(max_length=200)
    valor = models.CharField(max_length=200)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)

    def __str__(self):
        return 'Llave: ' + self.llave + ', Valor: ' + self.valor