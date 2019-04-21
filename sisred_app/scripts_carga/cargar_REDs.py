# Librería para leer archivos csv
import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisred.settings")
django.setup()
from sisred_app.models import RED
import datetime

# Metodo para cargar los REDs desde los archivos planos
with open('./archivos/reds.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de las columnas {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]},{row[10]}, {row[11]}, {row[12]}')
            id_conectate = row[0]
            #El nombre y nombre corto se toma de la descripcion dado que no viene en el archivo CSV
            nombre = row[3][1:15]
            nombre_corto = row[3][1:6]
            descripcion = row[3]
            # Se agrega formato de fechas para que la misma esté acorde al campo de la base de datos
            # Se agregan las funciones rstrip().lstrip() para quitar espacios en blanco en las fechas
            fecha_inicio = datetime.datetime.strptime(row[4].rstrip().lstrip(), '%Y-%m-%d')
            fecha_cierre = datetime.datetime.strptime(row[5].rstrip().lstrip(), '%Y-%m-%d')
            fecha_creacion = datetime.datetime.strptime(row[6].rstrip().lstrip(), '%Y-%m-%d')
            porcentaje_avance = row[7]
            tipo = row[8]
            solicitante = row[9]
            horas_estimadas = row[10]
            horas_trabajadas = row[11]
            proyecto_conectate_id = row[12]
            red = RED(
                id_conectate=id_conectate,
                nombre=nombre,
                nombre_corto = nombre_corto,
                descripcion = descripcion,
                fecha_inicio = fecha_inicio,
                fecha_cierre = fecha_cierre,
                fecha_creacion=fecha_creacion,
                porcentaje_avance = porcentaje_avance,
                tipo = tipo,
                solicitante = solicitante,
                horas_estimadas = horas_estimadas,
                horas_trabajadas = horas_trabajadas,
                proyecto_conectate_id = proyecto_conectate_id,
            )
            red.save()
            line_count += 1
            print(f'{line_count} lineas procesadas.')
