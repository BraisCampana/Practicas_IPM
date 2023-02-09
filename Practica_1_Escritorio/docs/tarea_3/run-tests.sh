#!/bin/bash

if [ $# -eq 0 ]
  then
    python3 pruebas.py ./tarea3.py
else
  if [ "$*" == '-notUP' ]
    then
      python3 pruebas.py ./tarea3.py -notUP
    else echo "Has introducido un flag incorrecto"
fi
fi
