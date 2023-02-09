#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import threading
import requests
import json
import qrcode # sudo apt-get install pyhton3-qrcode
from datetime import datetime
import math
from time import sleep

##################### MODEL ################

class Model: #aquí hariamos una clase user con todos sus atributos y un método que accedería a la base de datos para coger todos los usuarios etc

    # PREGUNTAR A LA PROFE QUÉ SIGNIFICA: EL SERVIDOR DEVUELVE UN MENSAJE DE ERROR
    def __init__(self, controller):
        self.found_user = False
        self.name = ""#str
        self.surname = "" #str
        self.email = "" #str
        self.nick = "" #str
        self.vacunado = ""
        self.uuid = ""
        self.phone = ""
        self.qr = ""
        self.controllerMain = controller
        self.name_search = ""
        self.surname_search = ""
        self.inicial = ""
        self.final = ""
        self.is_calculating = False

    def create_qr(self, name, apellido, uuid):
        qraux = qrcode.QRCode(version = None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
        qraux.add_data("{"+name+"},{"+apellido+"},{"+uuid+"}")
        qraux.make(fit=True)
        img = qraux.make_image(fill_color="black", back_color="white")
        img.save("qr.png")
        self.qr = "qr.png"
        return self.qr

    def set_calculating(self):
        self.is_calculating = True

    def access_BD(self, name, surname):
        self.found_user = False # ponemos esto a falso cada vez que buscamos a alguien
        nombre = name # entrada del usuario objetivo (nombre)
        apellido = surname # entrada del usuario (apellido)

        # comprobar que la base de datos está up
        try:
            r = requests.get("http://localhost:8080/api/rest/user?name=" +nombre+ "&surname=" + apellido, # ejecutamos llamada a la base de datos
            headers={"x-hasura-admin-secret":"myadminsecretkey"}) #request
        except requests.exceptions.ConnectionError as e:
            GLib.idle_add(lambda: self.controllerMain.create_dialog("No se puede conectar con el servidor", self.controllerMain.controller.view))
            return
        except requests.exceptions.Timeout as t:
            GLib.idle_add(lambda: self.controllerMain.create_dialog("El servidor no responde", self.controllerMain.controller.view))
            return
        data = r.json()
        length = 0
        values = None
        sleep(5)
        for key, value in data.items():
            length = len(value) # número de respuestas obtenidas de la base de datos
            values = value
        if bool([a for a in data.values() if a != []]) is True and length == 1:
            self.found_user = True # encontramos al usuario
            for key, value in data.items():
                self.uuid = value[0]['uuid']
                self.nick = value[0]['username']
                self.name = value[0]['name']
                self.email = value[0]['email']
                self.surname = value[0]['surname']
                self.phone = value[0]['phone']
                if value[0]['is_vaccinated'] is False:
                    self.vacunado = "No"
                else: self.vacunado = "Sí"
            if self.controllerMain.controllerInfo is None:
                self.controllerMain.set_controller_info() # creamos la ventana de información pero NO la mostramos
            self.create_qr(self.name, self.surname, self.uuid)
            items = {
                "name": self.name,
                "apellido": self.surname,
                "email": self.email,
                "nick": self.nick,
                "telefono": self.phone,
                "vacunado": self.vacunado,
                "uuid": self.uuid,
                "qr": self.qr
            }
            GLib.idle_add(lambda: self.controllerMain.update_view_info(items)) # actualizamos la ventana con los nuevos datos y la mostramos
        elif length > 1:
            if self.controllerMain.controllerInfo is None:
                self.controllerMain.set_controller_info()
            self.controllerMain.set_controller_more1user() # creamos el controlador y, consecuentemente, la ventana con la información de todos los usuarios encontrados
            GLib.idle_add(lambda: self.controllerMain.get_info_allusers(values))
        elif bool([a for a in data.values() if a != []]) is False:
            GLib.idle_add(lambda: self.controllerMain.controller.not_found())

    def check_entry(self, name, surname):
        if name == "" or surname == "":
            return False
        return True

    def set_user_search(self, name, surname):
        self.name_search = name
        self.surname_search = surname

    def get_filtrado_dates(self, inicial, final):
        self.inicial = inicial
        self.final = final

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_instalaciones(self, fromAlerts, offset, limit): #este método accede a la BD y coge las instalaciones de dicho usuario desde offset y coge hasta limit elementos
        try:
            if offset is None or limit is None:
                r = requests.get("http://localhost:8080/api/rest/user_access_log/"+ self.uuid, headers={"x-hasura-admin-secret":"myadminsecretkey"}) # cogemos las instalaciones
            else:
                r = requests.get("http://localhost:8080/api/rest/user_access_log/"+ self.uuid+"?offset="+str(offset)+"&limit="+str(limit), headers={"x-hasura-admin-secret":"myadminsecretkey"})
        except requests.exceptions.ConnectionError as e:
            GLib.idle_add(lambda: self.controllerMain.create_dialog("No se puede conectar con el servidor", self.controllerMain.controllerInfo.view))
            return
        except requests.exceptions.Timeout as t:
            GLib.idle_add(lambda: self.controllerMain.create_dialog("No se puede conectar con el servidor", self.controllerMain.controllerInfo.view))
            return
        data = r.json()
        if data["access_log"] == []: # si la lista está vacía y NO llamamos a la función desde get_alerts(), mostramos este diálogo
            if fromAlerts == False:
                GLib.idle_add(lambda: self.controllerMain.create_dialog("Este usuario aún no ha visitado ninguna instalación", self.controllerMain.get_view_info()))
                return None
            return None
        content = [] # lista de diccionarios con la información
        i = 0
        sleep(3)
        for key, value in data.items(): # value es el array que contiene todos los diccionarios de cada key
            for i in range(len(value)):
                fecha_hora = value[i]["timestamp"].split("T")
                fecha = fecha_hora[0]
                hora = fecha_hora[1].split(".")[0]
                info = {
                    "Fecha": fecha, # incluye fecha y hora --> hay que separar (value[1] accede a la segunda hora, es decir, a la segunda instalación)
                    "Hora": hora,
                    "Temperatura": value[i]["temperature"],
                    "Nombre": value[i]["facility"]["name"],
                    "ID": value[i]["facility"]["id"]
                }
                content.append(info)
        if fromAlerts is False:
            GLib.idle_add(lambda: self.controllerMain.controllerInstalaciones.get_content(content)) # volvemos al controller de instalaciones y actualizamos la vista
        else:
            return content

    def get_alerts(self, withRange): # coger todas las instalaciones donde estuvo el usuario y coger todos los datos de cada una de las instalaciones y meterlos en un diccionario
        infoInstalaciones = self.get_instalaciones(True, None, None)
        if infoInstalaciones == None:
            GLib.idle_add(lambda: self.controllerMain.create_dialog("Este usuario aún no ha visitado ninguna instalación, por lo tanto no ha recibido ninguna alerta", self.controllerMain.get_view_info()))
            return None
        auxVacunado = ""
        i = 0
        listID = []
        for i in range(len(infoInstalaciones)):
            if infoInstalaciones[i]["ID"] in listID:
                continue
            listID.append(infoInstalaciones[i]["ID"]) # contiene la lista con los ids de las instalaciones donde estuvo el usuario
        i = j = 0
        content = []
        aux = []
        S = set()
        sleep(2)
        for i in range(len(listID)): # ahora hay que hacer una request a la BD por cada uno de los ids y guardar todo en un json
            try:
                if withRange is False: r = requests.get("http://localhost:8080/api/rest/facility_access_log/" + str(listID[i]), headers={"x-hasura-admin-secret":"myadminsecretkey"})
                else: r = requests.get("http://localhost:8080/api/rest/facility_access_log/" + str(listID[i])+"/daterange",
                headers={"x-hasura-admin-secret":"myadminsecretkey"},  json={"startdate": self.inicial+"T02:03:00+00:000", "enddate": self.final+"T02:03:00+00:000"})
            except requests.exceptions.ConnectionError as e:
                GLib.idle_add(lambda: self.controllerMain.create_dialog("No se puede conectar con el servidor", self.controllerMain.controllerAlerts.view))
                return
            except requests.exceptions.Timeout as t:
                GLib.idle_add(lambda: self.controllerMain.create_dialog("No se puede conectar con el servidor", self.controllerMain.controllerAlerts.view))
                return
            data = r.json()
            if data["access_log"] == []:
                continue
            for key, value in data.items(): # value es el array que contiene todos los diccionarios de cada key
                for j in range(len(value)):
                    fecha_hora = value[j]["timestamp"].split("T")
                    fecha = fecha_hora[0]
                    hora = fecha_hora[1].split(".")[0]
                    if value[j]["user"]["is_vaccinated"] is False:
                        auxVacunado = "No"
                    else: auxVacunado = "Sí"
                    info = {
                        "Fecha": fecha, # incluye fecha y hora --> hay que separar (value[1] accede a la segunda hora, es decir, a la segunda instalación)
                        "Hora": hora,
                        "Temperatura": value[j]["temperature"],
                        "Nombre": value[j]["user"]["name"],
                        "Apellido": value[j]["user"]["surname"],
                        "Phone": value[j]["user"]["phone"],
                        "Vacunado": auxVacunado,
                        "ID": str(listID[i])
                    }
                    aux.append(info) # lista que contiene la información de los usuarios que estuvieron en una instalación (además, contiene el propio id de la instalación --> mostrar en el tree)
        for item in aux:
            if item["Nombre"]+" "+ item["Apellido"] not in S:
                S.add(item["Nombre"]+" "+ item["Apellido"])
                if self.name == item["Nombre"] and self.surname == item["Apellido"]:
                    continue
                else: content.append(item)
                aux = [current for current in aux if current["Nombre"] != item["Nombre"] and current["Apellido"] != item["Apellido"]]
        GLib.idle_add(lambda: self.controllerMain.controllerAlerts.get_content(content, withRange))

################ CONTROLLER + VIEW BÚSQUEDA ######################

class View:
    def __init__(self, controller):
        self.controller = controller
        self.win = Gtk.Window(title = "Búsqueda")
        self.win.connect('delete-event', Gtk.main_quit)
        self.win.set_default_size(400, 150)

        self.spinner = Gtk.Spinner()

        self.vbox = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing=10, margin = 10)

        self.dummy_field = Gtk.Entry()
        self.vbox.pack_start(self.dummy_field, False, False, 0)

        self.labelname = Gtk.Label(label = "Nombre", xalign = 0)
        self.vbox.pack_start(self.labelname, False, False, 0)
        self.input = Gtk.Entry()
        self.input.get_accessible().set_name("name_entry")
        self.vbox.pack_start(self.input, False, False, 0)
        self.input.set_placeholder_text("Ex: David")

        self.labelsurname = Gtk.Label(label = "Apellido", xalign = 0)
        self.vbox.pack_start(self.labelsurname, False, False, 0)
        self.inputsurname = Gtk.Entry()
        self.inputsurname.get_accessible().set_name("surname_entry")
        self.vbox.pack_start(self.inputsurname, False, False, 0)
        self.inputsurname.set_placeholder_text("Ex: Campaña")

        self.hbox = Gtk.HBox(halign = Gtk.Align.CENTER)

        self.search = Gtk.Button(label = "Buscar")
        self.search.connect('clicked', self.controller.show_info)
        self.hbox.pack_start(self.search, False, False, 0)

        self.vbox.pack_start(self.hbox, False, False, 0)
        self.vbox.pack_start(self.spinner, False, False, 0)

        self.win.add(self.vbox)
        self.show_all()
        self.dummy_field.hide()

    def show_all(self):
        self.win.show_all()

    def show_activity(self, shown):
        if shown:
            self.spinner.start()
        else: self.spinner.stop()

class Controller:
    def __init__(self, controllerZ):
        self.controllerZ = controllerZ
        self.view = View(self)

    def not_found(self):
        self.view.show_activity(False)
        self.controllerZ.create_dialog("No se encontró ningún usuario", self.view) # se muestra un diálogo de error informando de que no se encontró ningún usuario

    def show_info(self, widget):
        if self.controllerZ.model.check_entry(self.view.input.get_text().strip(), self.view.inputsurname.get_text().strip()) == False: # comprobamos el contenido de la entrada del usuario
            self.controllerZ.create_dialog("Introduce un nombre y apellido", self.view)
            return
        self.controllerZ.model.set_user_search(self.view.input.get_text().strip(), self.view.inputsurname.get_text().strip())
        name = self.view.input.get_text().strip()
        surname = self.view.inputsurname.get_text().strip()
        self.view.show_activity(True) # activamos el spinner
        t = threading.Thread(target=self.controllerZ.model.access_BD, args=(name, surname), daemon=True)# accedemos a la base de datos
        t.start()

####################### CONTROLLER + VIEW INFORMACIÓN PERSONAL ############################s


class ViewInfo:
    def __init__(self, controller):
        self.win = Gtk.Window(title = "Informacion Personal de {}".format(controller.controllerZ.model.name_search.strip() + " " + controller.controllerZ.model.surname_search.strip()))
        self.win.set_default_size(600, 150)

        self.spinnerI = Gtk.Spinner()
        self.spinnerA = Gtk.Spinner()

        self.qr = Gtk.Image()

        self.hboxGlobal = Gtk.HBox(halign = Gtk.Align.START) # caja global

        self.vbox = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing=10, margin = 10, valign = Gtk.Align.START)

        self.hboxalertas = Gtk.HBox(spacing= 8, halign= Gtk.Align.START)
        self.alertas = Gtk.Button(label = "Alertas Covid")
        self.alertas.get_accessible().set_name("alertas")
        self.alertas.set_size_request(70, 30)
        self.alertas.connect('clicked', controller.show_alerts)

        self.hboxinstalaciones = Gtk.HBox(spacing= 8, halign= Gtk.Align.START)
        self.instalaciones = Gtk.Button(label = "Instalaciones")
        self.instalaciones.get_accessible().set_name("instalaciones")
        self.instalaciones.set_size_request(70, 30)
        self.instalaciones.connect('clicked', controller.show_instalaciones)

        self.hboxalertas.pack_start(self.alertas, expand= False, fill= False, padding= 8)
        self.hboxalertas.pack_start(self.spinnerA, False, False, 0)
        self.hboxinstalaciones.pack_start(self.instalaciones, expand = False, fill = False, padding=8)
        self.hboxinstalaciones.pack_start(self.spinnerI, False, False, 0)

        self.hboxinformaciones = Gtk.HBox(spacing = 100, halign = Gtk.Align.START)

        self.vboxinformacion1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5, valign = Gtk.Align.START)

        self.nombre = Gtk.Label(label = "Nombre")
        self.nombre.set_halign(Gtk.Align.START)

        self.nick = Gtk.Label(label = "Nick usuario")
        self.nick.set_halign(Gtk.Align.START)

        self.correo = Gtk.Label(label = "Correo")
        self.correo.set_halign(Gtk.Align.START)

        self.vacunado = Gtk.Label(label = "Vacunado")
        self.vacunado.set_halign(Gtk.Align.START)

        self.vboxinformacion1.pack_start(self.nombre, expand = False, fill = False, padding = 0)
        self.vboxinformacion1.pack_start(self.nick, expand = False, fill = False, padding = 0)
        self.vboxinformacion1.pack_start(self.correo, expand = False, fill = False, padding = 0)
        self.vboxinformacion1.pack_start(self.vacunado, expand = False, fill = False, padding = 0)
        self.vboxinformacion1.pack_start(self.hboxinstalaciones, expand= False, fill= False, padding= 0)
        self.vboxinformacion1.pack_start(self.hboxalertas, expand= False, fill= False, padding= 0)

        self.vboxinformacion2= Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5, valign = Gtk.Align.START)

        self.apellidos = Gtk.Label(label = "Apellidos")
        self.apellidos.set_halign(Gtk.Align.START)

        self.telefono = Gtk.Label(label = "Teléfono")
        self.telefono.set_halign(Gtk.Align.START)

        self.uuid = Gtk.Label(label = "UUID")
        self.uuid.set_halign(Gtk.Align.START)

        self.vboxinformacion2.pack_start(self.apellidos, expand = False, fill = False, padding = 0)
        self.vboxinformacion2.pack_start(self.telefono, expand = False, fill = False, padding = 0)
        self.vboxinformacion2.pack_start(self.uuid, expand = False, fill = False, padding = 0)
        self.vboxinformacion2.pack_start(self.qr, False, False, 0)

        self.hboxinformaciones.pack_start(self.vboxinformacion1, expand = False, fill = False, padding = 1)
        self.hboxinformaciones.pack_start(self.vboxinformacion2, expand = False, fill = False, padding = 1)

        self.vbox.pack_start(self.hboxinformaciones, expand=False, fill=False, padding=0)

        self.win.add(self.vbox)

    def show_all(self):
        self.win.show_all()

    def show_activityI(self, shown):
        if shown:
            self.spinnerI.start()
        else: self.spinnerI.stop()

    def show_activityA(self, shown):
        if shown:
            self.spinnerA.start()
        else: self.spinnerA.stop()

class ControllerInfo:
    def __init__(self, controller):
        self.controllerZ = controller
        self.view = ViewInfo(self)

    def show_alerts(self, widget):
        self.controllerZ.set_controller_alerts()
        self.view.show_activityA(True)
        t = threading.Thread(target = self.controllerZ.get_alerts, daemon=True) # ponemos la función sin () porqué sino no se estaría creando
        t.start()

    def show_instalaciones(self, widget):
        self.controllerZ.set_controller_instalaciones()
        self.view.show_activityI(True)
        t = threading.Thread(target= self.controllerZ.get_instalaciones, daemon=True)
        t.start()

    def set_labels(self, items):
        self.view.nombre.set_text(self.view.nombre.get_text().strip()+"\t\t" + items["name"])
        self.view.apellidos.set_text(self.view.apellidos.get_text().strip()+"\t" + items["apellido"])
        self.view.nick.set_text(self.view.nick.get_text().strip()+"\t" + items["nick"]) #username
        self.view.uuid.set_text(self.view.uuid.get_text().strip()+"\t\t" + items["uuid"])
        self.view.telefono.set_text(self.view.telefono.get_text().strip() + "\t" + items["telefono"])
        self.view.vacunado.set_text(self.view.vacunado.get_text().strip() +"\t\t" + items["vacunado"])
        self.view.correo.set_text(self.view.correo.get_text().strip() + "\t\t" + items["email"])
        self.view.qr.set_from_file(items["qr"])

    def update_view(self, items): #este método se encargará de actualizar la vista con la información correspondiente, es decir, añadir a los labels la info
        self.controllerZ.set_spinner(False)
        self.view = ViewInfo(self)
        self.set_labels(items)
        self.view.show_all()

    def get_view(self):
        return self.view


######################### CONTROLLER + VIEW ALERTS ##############################

class ViewAlerts():
    def __init__(self, controller): # controller : controllerAlerts
        self.win = Gtk.Window(title = "Alertas Covid")
        self.win.set_default_size(600, 550)

        self.currentPage = 0
        self.dummy_entry = Gtk.Entry() # entrada que tiene el focus y no se mostrará

        self.spinnerF = Gtk.Spinner()

        #FILTRADO
        self.filtrar = Gtk.Button(label = "Filtrar")
        self.filtrar.set_size_request(70, 30)
        self.filtrar.connect('clicked', controller.filtrar)

        self.hboxFI = Gtk.HBox(spacing = 35, halign = Gtk.Align.END)
        self.labelFI = Gtk.Label(label = "Fecha inicial")
        self.labelFI.set_halign(Gtk.Align.START)
        self.hboxFI.pack_start(self.labelFI, False, False, 0)
        self.entryFI = Gtk.Entry()
        self.entryFI.set_placeholder_text("Ex: 20-09-2021")
        self.hboxFI.pack_start(self.entryFI, False, False, 0)

        self.hboxFF = Gtk.HBox(spacing = 35, halign = Gtk.Align.END)
        self.labelFF = Gtk.Label(label = "Fecha final")
        self.labelFF.set_halign(Gtk.Align.START)
        self.hboxFF.pack_start(self.labelFF, False, False, 0)
        self.entryFF = Gtk.Entry()
        self.entryFF.set_placeholder_text("Ex: 22-09-2021")
        self.hboxFF.pack_start(self.entryFF, False, False, 0)

        self.vboxFechas = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 15, valign = Gtk.Align.START)
        self.vboxFechas.pack_start(self.dummy_entry, False, False, 0)
        self.vboxFechas.pack_start(self.hboxFI, False, False, 0)
        self.vboxFechas.pack_start(self.hboxFF, False, False, 0)

        self.hboxFG = Gtk.HBox(spacing = 5, halign = Gtk.Align.CENTER)
        self.hboxFG.pack_start(self.vboxFechas, False, False, 0)
        self.hboxFG.pack_start(self.filtrar, False, False, 0)
        self.hboxFG.pack_start(self.spinnerF, False, False, 0)

        #BOTONES ANTERIOR SIGUIENTE
        self.showPage = Gtk.Label()
        self.hbox = Gtk.HBox(spacing = 50, halign = Gtk.Align.CENTER)
        self.anterior = Gtk.Button(label = "Anterior")
        self.anterior.set_size_request(70, 30)
        self.anterior.connect('clicked', controller.previous_page)
        self.siguiente = Gtk.Button(label = "Siguiente")
        self.siguiente.set_size_request(70, 30)
        self.siguiente.connect('clicked', controller.next_page)
        self.hbox.pack_start(self.anterior, False, False, 0)
        self.hbox.pack_start(self.siguiente, False, False, 0)
        self.hbox.pack_start(self.showPage, False, False, 0)

        self.store = Gtk.ListStore(str, str, str, str, str, str, str, str) # nombre // apellido // email // phone // fecha // id instalacion // nombre
        self.treeview = Gtk.TreeView(model=self.store)

        for i, column_title in enumerate(
            ["Fecha", "Hora", "Temperatura", "Nombre", "Apellido", "Phone", "Vacunado", "Id instalación"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # a la hora de meter los datos, si pulsamos siguiente/anterior se actualizan los datos y se muestran nuevos

        self.treeview.set_size_request(600, 525)

        self.vbox = Gtk.VBox(valign = Gtk.Align.END)
        self.vbox.pack_end(self.hbox, False, False, 0)
        self.vbox.pack_start(self.hboxFG, False, False, 0)
        self.vbox.pack_start(self.treeview, False, False, 0)

        self.win.add(self.vbox)
        #self.show_all()

    def show_all(self):
        self.win.show_all()
        self.dummy_entry.hide()

    def show_activity(self, shown):
        if shown:
            self.spinnerF.start()
        else: self.spinnerF.stop()

class ControllerAlerts():
    def __init__(self, controller):
        self.controllerZ = controller
        self.view = ViewAlerts(self)
        self.elementsPage = 20
        self.pages = 0
        self.content = []
        self.inicial = ""
        self.final = ""
        self.leftValues = 0

    def filtrar(self, widget):
        self.inicial = self.view.entryFI.get_text().strip()
        self.final = self.view.entryFF.get_text().strip()

        if self.inicial == "" or self.final == "":
            self.controllerZ.create_dialog("Debes introducir fecha inicial y final", self.view)
            return
        else:
            # filtrar entre las dos fechas introducidas
            try:
                fechaInicial = datetime.strptime(self.inicial, "%d-%m-%Y")
            except ValueError as e:
                self.controllerZ.create_dialog("La fecha inicial introducida no está en el formato correcto. El formato correcto es: Día-Mes-Año (22-09-2021)", self.view)
                return
            try:
                fechaFinal = datetime.strptime(self.final, "%d-%m-%Y")
            except ValueError as f:
                self.controllerZ.create_dialog("La fecha final introducida no está en el formato correcto. El formato correcto es: Día-Mes-Año (22-09-2021)", self.view)
                return
            if fechaFinal < fechaInicial:
                self.controllerZ.create_dialog("La fecha final es anterior a la fecha inicial", self.view)
                return
            cachos = self.inicial.split("-")
            self.inicial = cachos[2]+"-"+cachos[1]+"-"+cachos[0]
            cachos2 = self.final.split("-")
            self.final = cachos2[2]+"-"+cachos2[1]+"-"+cachos2[0]
            self.view.show_activity(True)
            t = threading.Thread(target= self.controllerZ.get_alerts_range, args=(self.inicial, self.final), daemon=True)
            t.start()

    def get_content(self, content, withRange):
        self.controllerZ.set_spinnerA(False)
        if withRange:
            self.view.show_activity(False)
        self.view.currentPage = 0
        self.content.clear()
        self.content = sorted(content, key=lambda k: k['Fecha'], reverse = True) # lista ordenada desde la última instalación visitada
        self.pages = (int(len(self.content) / self.elementsPage)) + 1 # número de páginas (se puede usar para indicar a partir de qué offset se empieza a mostrar, elementsPage * currentPage)
        if (int(len(self.content) % self.elementsPage)) == 0: # si el número de elementos a mostrar es múltiplo del número de elementos por página, necesitamos una menos
            self.pages -= 1

        self.leftValues = len(self.content)
        self.update_view_alerts()

    def update_view_alerts(self):
        self.view.store.clear()
        principio = self.elementsPage * self.view.currentPage # si estamos en la primera página, empezamos en la posición 0
        final = (self.elementsPage * (self.view.currentPage+1)) # si estamos en la primera página, sería elemento 20

        currentList = []
        i = principio
        if self.view.currentPage == self.pages-1:
            final = self.leftValues + principio
        for i in range(principio,final):
            info = (str(self.content[i]["Fecha"]), str(self.content[i]["Hora"]), str(self.content[i]["Temperatura"]),  self.content[i]["Nombre"],  str(self.content[i]["Apellido"]),
            self.content[i]["Phone"], self.content[i]["Vacunado"], self.content[i]["ID"])
            currentList.append(info)
        for xlist in currentList:
            self.view.store.append(list(xlist))
        self.view.treeview.set_model(self.view.store)
        self.view.showPage.set_text(str(self.view.currentPage+1)+"/"+str(self.pages))
        self.view.show_all()

        if self.view.currentPage == 0:
            self.view.anterior.hide()
        else: self.view.anterior.show()
        if self.view.currentPage == self.pages-1: # si estamos en la última página, no se muestra siguiente
            self.view.siguiente.hide()
        else: self.view.siguiente.show()

    def next_page(self, widget):
        if self.view.currentPage < self.pages:
            self.view.currentPage += 1
        self.leftValues -= self.elementsPage
        self.update_view_alerts()

    def previous_page(self, widget):
        if self.view.currentPage > 0:
            self.view.currentPage -= 1
        self.leftValues += self.elementsPage
        self.update_view_alerts()


########################## CONTROLLER + VIEW INSTALACIONES ####################################


class ViewInstalaciones():
    def __init__(self, controller):
        self.win = Gtk.Window(title = "Instalaciones visitadas por el usuario")
        self.win.set_default_size(600, 550)

        self.currentPage = 0

        self.showPage = Gtk.Label()
        self.hbox = Gtk.HBox(spacing = 50, halign = Gtk.Align.CENTER)
        self.anterior = Gtk.Button(label = "Anterior")
        self.anterior.set_size_request(70, 30)
        self.anterior.connect('clicked', controller.previous_page)
        self.siguiente = Gtk.Button(label = "Siguiente")
        self.siguiente.set_size_request(70, 30)
        self.siguiente.connect('clicked', controller.next_page)
        self.hbox.pack_start(self.anterior, False, False, 0)
        self.hbox.pack_start(self.siguiente, False, False, 0)

        self.store = Gtk.ListStore(str, str, str, str, str) # fecha // hora // temperatura // nombre instalación // id instalacion
        self.treeview = Gtk.TreeView(model=self.store)

        for i, column_title in enumerate(
            ["Fecha", "Hora", "Temperatura", "Nombre instalación", "Id instalación"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # a la hora de meter los datos, si pulsamos siguiente/anterior se actualizan los datos y se muestran nuevos

        self.treeview.set_size_request(600, 525)

        self.vbox = Gtk.VBox(valign = Gtk.Align.END)
        self.vbox.pack_end(self.hbox, False, False, 0)
        self.vbox.pack_start(self.treeview, False, False, 0)

        self.win.add(self.vbox)

    def show_all(self):
        self.win.show_all()

class ControllerInstalaciones():
    def __init__(self, controller):
        self.controllerZ = controller
        self.view = ViewInstalaciones(self)
        self.elementsPage = 20
        self.pages = 0
        self.content = []
        self.leftValues = 0

    def get_content(self, content):
        self.controllerZ.set_spinnerI(False)
        self.content = sorted(content, key=lambda k: k['Fecha'], reverse = True) # lista ordenada desde la última instalación visitada
        self.pages = (int(len(self.content) / self.elementsPage)) + 1 # número de páginas (se puede usar para indicar a partir de qué offset se empieza a mostrar, elementsPage * currentPage)
        # suponemos que el número de elementos a mostrar NO es múltiplo de self.elementsPage, por lo que necesitamos 1 page más
        if (int(len(self.content) % self.elementsPage)) == 0: # si el número de elementos a mostrar es múltiplo del número de elementos por página, necesitamos una menos
            self.pages -= 1

        self.view.hbox.pack_start(self.view.showPage, False, False, 0)
        self.leftValues = len(self.content)
        self.update_view_instalaciones()

    def update_view_instalaciones(self):
        self.view.store.clear()
        principio = self.elementsPage * self.view.currentPage # si estamos en la primera página, empezamos en la posición 0
        final = (self.elementsPage * (self.view.currentPage+1)) # si estamos en la primera página, sería elemento 20

        currentList = []
        i = principio
        if self.view.currentPage == self.pages-1:
            final = self.leftValues + principio
        for i in range(principio,final):
            info = (str(self.content[i]["Fecha"]), str(self.content[i]["Hora"]), str(self.content[i]["Temperatura"]),  self.content[i]["Nombre"],  str(self.content[i]["ID"]))
            currentList.append(info)
        for xlist in currentList:
            self.view.store.append(list(xlist))
        self.view.treeview.set_model(self.view.store)
        self.view.showPage.set_text(str(self.view.currentPage+1)+ "/"+str(self.pages))
        self.view.show_all()

        if self.view.currentPage == 0:
            self.view.anterior.hide()
        else: self.view.anterior.show()
        if self.view.currentPage == self.pages-1: # si estamos en la última página, no se muestra siguiente
            self.view.siguiente.hide()
        else: self.view.siguiente.show()

    def next_page(self, widget):
        if self.view.currentPage < self.pages:
            self.view.currentPage += 1
        self.leftValues -= self.elementsPage
        # habría que hacer otra petición al servidor con el offset = limitanterior y limit = self.elementsPage + limitanterior || len(self.content) en caso de que se acabe
        # por ejemplo, si tenemos 34 elementos en total y estamos en la última página, el offset sería 20 y el limit 34
        self.update_view_instalaciones()

    def previous_page(self, widget):
        if self.view.currentPage > 0:
            self.view.currentPage -= 1
        self.leftValues += self.elementsPage
        self.update_view_instalaciones()


######################## MAIN CONTROLLER ################################################

class ControllerZ:
    def __init__(self):
        self.model = Model(self)
        self.controller = Controller(self)
        self.controllerInfo = None
        self.controllerAlerts = None
        self.controllerInstalaciones = None
        self.ControllerMore1User = None

    def set_controller_info(self):  # necesitamos crear la ventana de info en el momento preciso
        self.controllerInfo = ControllerInfo(self)

    def set_controller_alerts(self):
        self.controllerAlerts = ControllerAlerts(self)

    def set_controller_instalaciones(self):
        self.controllerInstalaciones = ControllerInstalaciones(self)

    def set_controller_more1user(self):
        self.ControllerMore1User = ControllerMore1User(self)

    def update_view_info(self, items):
        self.controllerInfo.update_view(items)

    def connection_error(self):
        self.controller.show_connection_error()

    def not_answer(self):
        self.controller.show_notserver_answer()

    def get_instalaciones(self):
        #content = self.model.get_instalaciones(False, offset, limit)
        self.model.get_instalaciones(False, None, None)

    def get_alerts_range(self, inicial, final):
        self.model.get_filtrado_dates(inicial, final)
        self.model.get_alerts(True)

    def get_alerts(self):
        self.model.get_alerts(False)

    def get_info_allusers(self, content):
        self.set_spinner(False)
        self.ControllerMore1User.get_info_users(content)

    def create_dialog(self, text, view):
        dialog = Gtk.MessageDialog(parent= view.win, message_type= Gtk.MessageType.ERROR, buttons= Gtk.ButtonsType.CLOSE, text= text)
        dialog.run()
        dialog.destroy()

    def get_view_info(self):
        return self.controllerInfo.get_view()

    def set_spinner(self, value:bool):
        self.controller.view.show_activity(value)

    def set_spinnerI(self, value):
        self.controllerInfo.view.show_activityI(False)

    def set_spinnerA(self, value):
        self.controllerInfo.view.show_activityA(False)


############ CONTROLLER + VIEW con MÁS DE 1 USUARIO ###############################

class ViewMore1User():
    def __init__(self, controller):
        self.win = Gtk.Window(title = "Elige al usuario del que deseas ver la información")
        self.win.set_default_size(600, 550)

        self.vbox = Gtk.VBox(valign = Gtk.Align.CENTER)

        self.showPage = Gtk.Label()
        self.hbox = Gtk.HBox(spacing = 50, halign = Gtk.Align.CENTER)
        self.anterior = Gtk.Button(label = "Anterior")
        self.anterior.set_size_request(70, 30)
        self.anterior.connect('clicked', controller.previous_page)
        self.siguiente = Gtk.Button(label = "Siguiente")
        self.siguiente.set_size_request(70, 30)
        self.siguiente.connect('clicked', controller.next_page)
        self.hbox.pack_start(self.anterior, False, False, 0)
        self.hbox.pack_start(self.siguiente, False, False, 0)
        self.hbox.pack_start(self.showPage, False, False, 0)

        self.store = Gtk.ListStore(str, str, str, str, str, str, str) # Nombre // Apellido // Email // nick // uuid //telefono //vacunado
        self.treeview = Gtk.TreeView(model=self.store)

        for i, column_title in enumerate(
            ["Nombre", "Apellido", "Email", "Nick", "UUID", "Telefono", "Vacunado"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # a la hora de meter los datos, si pulsamos siguiente/anterior se actualizan los datos y se muestran nuevos

        self.treeview.set_size_request(600, 525)
        self.vbox.pack_start(self.treeview, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

        self.tree_selection = self.treeview.get_selection()
        self.tree_selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.tree_selection.connect("changed", controller.onSelectionChanged)

        self.win.add(self.vbox)

        #self.show_all()

    def show_all(self):
        self.win.show_all()


class ControllerMore1User:
    def __init__(self, controllerZ):
        self.controllerZ = controllerZ
        self.view = ViewMore1User(self)
        self.info = [] # contiene la información de todos los usuarios que se corresponden con la información introducida
        self.elementsPage = 10
        self.pages = 0
        self.currentPage = 0
        self.leftValues = 0

    def get_info_users(self, info):
        self.info = info
        self.pages = (int(len(self.info)/self.elementsPage))+1 # suponemos que el número de elementos a mostrar NO es múltiplo de self.elementsPage, por lo que necesitamos 1 page más
        if (int(len(self.info) % self.elementsPage)) == 0: # si el número de elementos a mostrar es múltiplo del número de elementos por página, necesitamos una menos
            self.pages -= 1

        self.leftValues = len(self.info) # número de valores ({}, diccionarios) que nos faltan por recorrer

        self.update_view_more1user()

    def update_view_more1user(self):
        self.view.store.clear()
        principio = self.elementsPage * self.currentPage # si estamos en la primera página, empezamos en la posición 0
        final = (self.elementsPage * (self.currentPage+1)) # si estamos en la primera página, sería elemento 20

        currentList = []
        i = principio
        vacunado = ""
        if self.currentPage == self.pages-1:
            final = self.leftValues + principio
        for i in range(principio,final):
            if self.leftValues == 0: # si estamos en la última página y vamos a escribir el nuevo elemento después del úlimto, salimos
                break
            if self.info[i]["is_vaccinated"] is False:
                vacunado = "No"
            else: vacunado = "Sí"
            info = (str(self.info[i]["name"]), str(self.info[i]["surname"]), str(self.info[i]["email"]), self.info[i]["username"],  str(self.info[i]["uuid"]),
            self.info[i]["phone"], vacunado)
            currentList.append(info)
        for xlist in currentList:
            self.view.store.append(list(xlist))
        self.view.treeview.set_model(self.view.store)
        self.view.showPage.set_text(str(self.currentPage+1)+"/"+str(self.pages))
        self.view.show_all()

        if self.currentPage == 0:
            self.view.anterior.hide()
        else: self.view.anterior.show()
        if self.currentPage == self.pages-1: # si estamos en la última página, no se muestra siguiente
            self.view.siguiente.hide()
        else: self.view.siguiente.show()

    def next_page(self, widget):
        if self.currentPage < self.pages:
            self.currentPage += 1
        self.leftValues -= self.elementsPage
        self.update_view_more1user()

    def previous_page(self, widget):
        if self.currentPage > 0:
            self.currentPage -= 1
        self.leftValues += self.elementsPage
        self.update_view_more1user()

    def onSelectionChanged(self, widget) :
        (model, pathlist) = self.view.tree_selection.get_selected_rows() # devuelve un path a cada una de las filas seleccionadas (solo una fila!)
        items = None
        for path in pathlist :
            tree_iter = model.get_iter(path)
            items = {
                "name": model.get_value(tree_iter, 0),
                "apellido": model.get_value(tree_iter, 1),
                "email": model.get_value(tree_iter, 2),
                "nick": model.get_value(tree_iter, 3),
                "uuid": model.get_value(tree_iter, 4),
                "telefono": model.get_value(tree_iter, 5),
                "vacunado": model.get_value(tree_iter, 6),
                "qr": self.controllerZ.model.create_qr(model.get_value(tree_iter, 0), model.get_value(tree_iter, 1), model.get_value(tree_iter, 4))
            }
        self.controllerZ.model.set_uuid(items["uuid"])
        self.controllerZ.controllerInfo.update_view(items)


ControllerZ()

Gtk.main()
