# MÉTODO DE EJECUCIÓN
#python3 pruebas.py ./tarea3.py

# 1) BD up --> 10/10
# 2)
    # - desactivar BD y hacer ./run-tests.sh -notUP --> 3/3

# 3) Si BD up y ./run-tests.sh -notUP --> 2/3

import re

import textwrap
from ipm import e2e

import sys
import os

from pathlib import Path
import random
import subprocess
import time


def show(text):
    print(textwrap.dedent(text))

def enter_entry(name_entry, data):
    entry = e2e.find_obj(app, role='text', name=name_entry)
    assert entry is not None
    entry.set_text_contents(data)

def show_passed():
    print('\033[92m', "  Passed",'\033[0m')

def show_not_passed(e):
    print('\033[91m', "  Not passed",'\033[0m')
    print(textwrap.indent(str(e), "    "))

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__

def db_down():
    os.system("sudo -p '\n\033[93mAuthentication required to run database down test: \033[0m' systemctl stop docker.socket")
    os.system("sudo systemctl stop docker.service")

def db_up():
    os.system("sudo systemctl start docker.socket")
    os.system("sudo systemctl start docker.service")

passed_tests = 0

######## PRIMER TEST ##########
path = sys.argv[1]
process, app = e2e.run(path, "tarea3")

if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

do, shows = e2e.perform_on(app)

show("""
    GIVEN the app was launched
    THEN I see a window with two entrys and a button to perform a search of a user
""")

try:
    assert shows(role= "label", text= "Nombre")
    assert shows(role= "label", text= "Apellido")
    assert shows(role= "push button", name= "Buscar")
    assert shows(role = "text", name="name_entry") # entry nombre
    assert shows(role = "text", name="surname_entry") # entry apellido
    show_passed()
    passed_tests += 1
except Exception as e:
    show_not_passed(e)
    process and process.kill()


# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()


###### SEGUNDO TEST ########
path = sys.argv[1]
process, app = e2e.run(path, "tarea3")

if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

do, shows = e2e.perform_on(app)
show("""
    GIVEN the app was launched
    WHEN I click the button without introducing anything in the form
    THEN the app shows an error to the user
""")

try:
    do('click', role= "push button", name= "Buscar") # si le damos a buscar sin introducir nada, salta un diálogo
    label = e2e.find_obj(app, role="label", name="dialog_label")
    assert label is not None
    assert label.get_text(0, -1) == "Introduce un nombre y apellido"
    show_passed()
    passed_tests += 1
except Exception as e:
    show_not_passed(e)
    process and process.kill()

process and process.kill()

############ TERCER TEST ########

server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user that does not exist in the form and click the button
        THEN the app shows an error to the user
    """)

    try:
        enter_entry("name_entry", "David")
        enter_entry("surname_entry", "Gayoso")
        do('click', role= "push button", name= "Buscar")
        label = e2e.find_obj(app, role="label", name="label_not_found")
        assert label is not None
        assert label.get_text(0, -1) == "No se encontró ningún usuario"
        show_passed()
        passed_tests += 1
    except Exception as e:
        show_not_passed(e)
        process and process.kill()

    process and process.kill()


############ CUARTO TEST ##########
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        enable_print()
        ventana = e2e.find_obj(app, role="frame", name="ventana_info") # cogemos la ventana de Info
        assert ventana is not None

        label = e2e.find_obj(app, role="label", name="nombre")
        assert label is not None
        assert label.get_text(0, -1) == "Nombre\t\tPurificacion"

        label = e2e.find_obj(app, role="label", name="apellido")
        assert label is not None
        assert label.get_text(0, -1) == "Apellidos\tVega"

        label = e2e.find_obj(app, role="label", name="nick")
        assert label is not None
        assert label.get_text(0, -1) == "Nick usuario\torangebear723"

        label = e2e.find_obj(app, role="label", name="correo")
        assert label is not None
        assert label.get_text(0, -1) == "Correo\t\tpurificacion.vega@example.com"

        label = e2e.find_obj(app, role="label", name="telefono")
        assert label is not None
        assert label.get_text(0, -1) == "Teléfono\t924-406-959"

        label = e2e.find_obj(app, role="label", name="vacunado")
        assert label is not None
        assert label.get_text(0, -1) == "Vacunado\t\tNo"

        label = e2e.find_obj(app, role="label", name="uuid")
        assert label is not None
        assert label.get_text(0, -1) == "UUID\t\t692d192a-f854-4f5c-8b31-bdf9563f6fca"

        button = e2e.find_obj(app, role="push button", name="alertas")
        assert button is not None

        button = e2e.find_obj(app, role="push button", name="instalaciones")
        assert button is not None

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()

######### QUINTO TEST #############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
        WHEN I click the button of instalaciones
        THEN the app shows the instalaciones of the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        do('click', role="push button", name="instalaciones")
        e2e.dump_app("tarea3")
        enable_print()

        assert shows(role="table", name="Lista Instalaciones")
        assert shows(role="push button", name="Anterior")
        assert shows(role="push button", name="Siguiente")
        assert shows(role="table column header", name="Fecha")
        assert shows(role="table column header", name="Hora")
        assert shows(role="table column header", name="Temperatura")
        assert shows(role="table column header", name="Nombre instalación")
        assert shows(role="table column header", name="Id instalación")
        assert shows(role="label", text="1/2")
        do('click', role="push button", name="Siguiente")
        block_print()
        e2e.dump_app("tarea3") # en el árbol de widgets aparecen siempre tanto el botón de siguiente como en el de anterior porque lo único que hacemos es esconderlos en la vista
        assert shows(role="label", text="2/2")
        do('click', role="push button", name="Anterior")
        e2e.dump_app("tarea3")
        enable_print()
        assert shows(role="table cell", name="Centro cultural Valentin Vega")
        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()

########### SEXTO TEST #############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
        WHEN I click the button of alertas
        THEN the app shows the alerts of the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        do('click', role="push button", name="alertas")
        e2e.dump_app("tarea3")
        enable_print()

        assert shows(role="table", name="Lista Alertas")
        assert shows(role="push button", name="Filtrar")
        assert shows(role="label", name="fecha inicial")
        assert shows(role="label", name="fecha final")
        assert shows(role="text", name="entry inicial")
        assert shows(role="text", name="entry final")

        assert shows(role="table column header", name="Fecha")
        assert shows(role="table column header", name="Hora")
        assert shows(role="table column header", name="Temperatura")
        assert shows(role="table column header", name="Nombre")
        assert shows(role="table column header", name="Apellido")
        assert shows(role="table column header", name="Vacunado")
        assert shows(role="table column header", name="Phone")
        assert shows(role="table column header", name="Id instalación")

        assert shows(role="push button", name="Anterior")
        assert shows(role="push button", name="Siguiente")
        assert shows(role="label", text="1/85")
        do('click', role="push button", name="Siguiente")
        block_print()
        e2e.dump_app("tarea3")
        assert shows(role="label", text="2/85")
        do('click', role="push button", name="Anterior")
        e2e.dump_app("tarea3")
        enable_print()
        assert shows(role="label", text="1/85")

        assert shows(role="table cell", name="Nieves")
        assert shows(role="table cell", name="Vargas")

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()


############ SÉPTIMO TEST ############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
        WHEN I click the button of alertas
        THEN the app shows the alerts of the user
        WHEN I do not introduce a date and click the filter button
        THEN the app shows an error message to the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        do('click', role="push button", name="alertas")
        e2e.dump_app("tarea3")
        enable_print()

        do('click', role="push button", name="Filtrar")
        label = e2e.find_obj(app, role="label", name="label_no_dates")
        assert label is not None
        assert label.get_text(0, -1) == "Debes introducir fecha inicial y fecha final"

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()

############ OCTAVO TEST ############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
        WHEN I click the button of alertas
        THEN the app shows the alerts of the user
        WHEN I introduce a date in a wrong format and click the filter button
        THEN the app shows an error message to the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        do('click', role="push button", name="alertas")
        e2e.dump_app("tarea3")
        enable_print()

        enter_entry("entry inicial", "06/09-2021")
        enter_entry("entry final", "09-09-2021")
        do('click', role="push button", name="Filtrar")
        label = e2e.find_obj(app, role="label", name="wrong_format")
        assert label is not None
        assert label.get_text(0, -1) == "La fecha inicial introducida no está en el formato correcto. El formato correcto es: Día-Mes-Año (22-09-2021)"

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()


############ NOVENO TEST ############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user in the form and click the button
        THEN the app shows the personal information of the user
        WHEN I click the button of alertas
        THEN the app shows the alerts of the user
        WHEN I introduce a final date that is before the initial one and click the filter button
        THEN the app shows an error message to the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        do('click', role="push button", name="alertas")
        e2e.dump_app("tarea3")
        enable_print()

        enter_entry("entry inicial", "09-09-2021")
        enter_entry("entry final", "07-09-2021")
        do('click', role="push button", name="Filtrar")
        label = e2e.find_obj(app, role="label", name="wrong_dates")
        assert label is not None
        assert label.get_text(0, -1) == "La fecha final es anterior a la fecha inicial"

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()

############ DÉCIMO TEST ############
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server != "-notUP":
    process, app = e2e.run(path, "tarea3")

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched
        WHEN I introduce a user that is repeated in the BD and click the search button
        THEN the app shows a window with all the users with that name and surname
    """)

    try:
        enter_entry("name_entry", "Nieves")
        enter_entry("surname_entry", "Vargas")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        enable_print()

        assert shows(role="frame", name="Elige al usuario del que deseas ver la información")
        assert shows(role="table", name="Lista More1User")


        assert shows(role="table column header", name="Nombre")
        assert shows(role="table column header", name="Apellido")
        assert shows(role="table column header", name="Vacunado")
        assert shows(role="table column header", name="Telefono")
        assert shows(role="table column header", name="Nick")
        assert shows(role="table column header", name="Email")
        assert shows(role="table column header", name="UUID")

        phoneTree = e2e.find_obj(app, role="table cell", name="990-350-465")
        vacunadoTree = e2e.find_obj(app, role="table cell", name="No")
        nombreTree = e2e.find_obj(app, role="table cell", name="Nieves")
        apellidoTree = e2e.find_obj(app, role="table cell", name="Vargas")
        emailTree = e2e.find_obj(app, role="table cell", name="nieves.vargas@example.com")
        nickTree = e2e.find_obj(app, role="table cell", name="sadsnake479")
        uuidTree = e2e.find_obj(app, role="table cell", name="5faf6c72-da4b-45a5-a17d-659121c4e4bf")
        do('edit', role="table cell", name="990-350-465")
        block_print()
        e2e.dump_app("tarea3")
        enable_print()

        assert shows(role="frame", name="ventana_info")

        # COMPROBAMOS QUE EL CONTENIDO QUE APARECE EN EL TREE VIEW COINCIDE CON LA INFORMACIÓN DE LA VENTANA QUE SE ABRE

        nombre = e2e.find_obj(app, role="label", name="nombre")
        apellido = e2e.find_obj(app, role="label", name="apellido")
        nick = e2e.find_obj(app, role="label", name="nick")
        email = e2e.find_obj(app, role="label", name="correo")
        telefono = e2e.find_obj(app, role="label", name="telefono")
        vacunado = e2e.find_obj(app, role="label", name="vacunado")
        uuid = e2e.find_obj(app, role="label", name="uuid")

        assert phoneTree.get_text(0, -1) == telefono.get_text(0, -1).split("\t")[1]
        assert vacunadoTree.get_text(0, -1) == vacunado.get_text(0, -1).split("\t")[2]
        assert nombreTree.get_text(0, -1) == nombre.get_text(0, -1).split("\t")[2]
        assert apellidoTree.get_text(0, -1) == apellido.get_text(0, -1).split("\t")[1]
        assert emailTree.get_text(0, -1) == email.get_text(0, -1).split("\t")[2]
        assert nickTree.get_text(0, -1) == nick.get_text(0, -1).split("\t")[1]
        assert uuidTree.get_text(0, -1) == uuid.get_text(0, -1).split("\t")[2]

        show_passed()
        passed_tests += 1
    except Exception as e:
        enable_print()
        show_not_passed(e)
        process and process.kill()

    process and process.kill()


##### UNDÉCIMO TEST #####
##### SI DESEA PROBAR ESTE TEST SIN NINGUN TIPO DE FALLO, DEBE TIRAR LA BD ABAJO CON docker rm -f $(docker ps -a -q) Y DESPUÉS EJECUTAR ./run-tests.sh -notUP
server = ""
path = sys.argv[1]
if len(sys.argv) == 3:
    server = sys.argv[2]
if server == "-notUP":
    db_down()
    process, app = e2e.run(path, "tarea3");

    if app is None:
        process and process.kill()
        assert False, f"La aplicación {path} no aparece en el escritorio"

    do, shows = e2e.perform_on(app)
    show("""
        GIVEN the app was launched but the database server is not up
        WHEN I introduce a user in the form and click the search button
        THEN the app shows an error to the user
    """)

    try:
        enter_entry("name_entry", "Purificacion")
        enter_entry("surname_entry", "Vega")
        do('click', role= "push button", name= "Buscar")
        block_print()
        e2e.dump_app("tarea3")
        enable_print()

        label = e2e.find_obj(app, role="label", name="label_error")
        assert label is not None
        assert label.get_text(0, -1) == "No es posible conectarse con el servidor"
        show_passed()
        passed_tests += 1
        db_up()
    except Exception as e:
        enable_print()
        show_not_passed(e)
        db_up()
        process and process.kill()

    process and process.kill()

if server != "-notUP": # database is up
    print("Tests passed: " +str(passed_tests)+"/10(" + str((passed_tests/10)*100)+"%)")
else: print(("Tests passed: " +str(passed_tests)+"/3(" + str((passed_tests/3)*100)+"%)"))
