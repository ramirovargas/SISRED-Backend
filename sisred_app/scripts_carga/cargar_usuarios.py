import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisred.settings")
django.setup()
from django.contrib.auth.models import User
from sisred_app.models import Perfil

# Metodo para cargar los usuarios desde un archivo plano
with open('./archivos/usuarios.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de las columnas {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}')
            id_persona = row[0]
            identificacion = row[1]
            apellidos1 = row[2]
            apellidos2 = row[3]
            nombres = row[4]
            correo = row[5]
            est = row[6]

            if est == "1":
                try:
                    user_exist = User.objects.get(email=correo)
                    print("Usuario con correo: "+correo+" ya existe!")
                except User.DoesNotExist:
                    user_model = User.objects.create_user(
                        username=correo,
                        first_name=nombres,
                        last_name=apellidos1 + " " + apellidos2,
                        email=correo
                    )

                    usuario = User.objects.get(email=correo)

                    perfil = Perfil(
                        id_conectate=id_persona,
                        usuario=usuario,
                        numero_identificacion=identificacion,
                        estado=est
                    )
                    perfil.save()
                    line_count += 1
    print(f'{line_count} lineas procesadas.')
