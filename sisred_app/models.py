from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
class Perfil(models.Model):
    id_conectate = models.CharField(unique=True, max_length=50)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_identificacion = models.CharField(max_length=50, blank=True, null=True)
    numero_identificacion = models.CharField(max_length=50, blank=True, null=True)
    estado = models.IntegerField()
    estado_sisred = models.IntegerField(default=0)

    def __str__(self):
        return "Usuario: " + self.usuario.first_name


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
    id_conectate = models.CharField(unique=True, max_length=50)
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


class Estado(models.Model):
    id_conectate = models.CharField(unique=True, max_length=50)
    nombre_estado = models.CharField(max_length=50)

    def __str__(self):
        return 'Estado: ' + self.nombre_estado


class RED(models.Model):
    id_conectate = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=200)
    nombre_corto = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateField(default=datetime.date.today, null=True)
    porcentaje_avance = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=50)
    solicitante = models.CharField(max_length=50)
    proyecto_conectate = models.ForeignKey(ProyectoConectate, on_delete=models.CASCADE)
    recursos = models.ManyToManyField(Recurso, blank=True)
    metadata = models.ManyToManyField(Metadata, blank=True)
    horas_estimadas = models.IntegerField(blank=True, null=True)
    horas_trabajadas = models.IntegerField(blank=True, null=True)
    fase = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True)
    listo = models.BooleanField( blank=True, null=True ,default=False)

    def __str__(self):
        return 'Red: ' + self.id_conectate
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
    autor = models.CharField(max_length=50)
    carpeta = models.CharField(max_length=200)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return "Proyecto RED: " + self.nombre


class HistorialFases(models.Model):
    fecha_cambio = models.DateField(default=datetime.date.today)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, related_name='historial_fases_red')
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return self.fase.__str__() + " " + self.red.__str__()


class Version(models.Model):
    es_final = models.BooleanField(default=False)
    numero = models.IntegerField()
    archivo = models.CharField(max_length=200)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)

    def __str__(self):
        return 'Version: ' + self.numero


class Rol(models.Model):
    id_conectate = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "Rol: " + self.id_conectate


class RolAsignado(models.Model):
    id_conectate = models.CharField(unique=True, max_length=50)
    estado = models.IntegerField()
    notificaciones = models.ManyToManyField(Notificacion, blank=True)
    red = models.ForeignKey(RED, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.__str__() + " " + self.red.__str__() + " " + self.rol.__str__()


class Comentario(models.Model):
    contenido = models.TextField()
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, blank=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=datetime.date.today())
    cerrado = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return 'Comentario: ' + self.contenido

class ComentarioMultimedia(models.Model):

    x1 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    y1 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    x2 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    y2 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)

    def __str__(self):
        return 'x1: ' + str(self.x1) + ', y1: ' + str(self.x2) + ', x2: ' + str(self.x2) + ', y2: ' + str(self.y2)

class ComentarioPDF (models.Model):

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    comentario_multimedia = models.ForeignKey(ComentarioMultimedia, on_delete=models.CASCADE)

    def __srt__(self):
        return 'height: ' + str(self.height) + ', width: ' + str(self.width)

class Propiedad(models.Model):
    llave = models.CharField(max_length=200)
    valor = models.CharField(max_length=200)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)

    def __str__(self):
        return 'Llave: ' + self.llave + ', Valor: ' + self.valor


