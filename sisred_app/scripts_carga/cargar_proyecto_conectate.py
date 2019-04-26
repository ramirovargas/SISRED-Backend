import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisred.settings")
django.setup()
from sisred_app.models import Rol, Perfil, RED, RolAsignado, ProyectoConectate
from django.core.exceptions import ObjectDoesNotExist

#Metodo para cargar los roles desde el archivo plano
with open('./archivos/proyectoconectate.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de las columnas {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}, {row[1]}')
            id_conectate = row[0]
            nombre = row[1]
            nombre_corto = row[2]
            codigo  = row[3]
            fecha_inicio= row[4]
            fecha_fin= row[5]
            obj, created = ProyectoConectate.objects.update_or_create(
                id_conectate=id_conectate, defaults={'nombre': nombre,'nombre_corto':nombre_corto,'codigo':codigo,'fecha_inicio':fecha_inicio,'fecha_fin':fecha_fin}
            )
            obj.save()
            line_count += 1
    print(f'{line_count} lineas procesadas.')

