#!/usr/bin/env python3

from ipm import e2e

import gi
import sys
import os
import re
from time import sleep

gi.require_version("Gtk", "3.0")
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__

def enter_entry(name_entry, data):
    entry = e2e.find_obj(app, role='text', name=name_entry)
    assert entry is not None
    entry.set_text_contents(data)

def step_la_interface_sigue_respondiendo(app: Atspi.Object) -> None:
# ELiminamos el timeout de arrancar la app
    Atspi.set_timeout(800, -1)
    assert app.get_name() != "", "La interface no responde"


if __name__== "__main__":

    path = sys.argv[1]
    process, app = e2e.run(path,"prueba")

    if app is None:
        process and process.kill()
        assert False, f"There is no aplication {path} in the desktop"

    do, shows = e2e.perform_on(app)

    enter_entry("name_entry", "Purificacion")
    enter_entry("surname_entry", "Vega")
    do('click', role= "push button", name= "Buscar")
    sleep(6)
    block_print()
    e2e.dump_app("prueba")
    enable_print()
    do('click', role="push button", name="alertas")
    step_la_interface_sigue_respondiendo(app)
    do('click', role="push button", name="instalaciones")
    sleep(6)

    process and process.kill()
