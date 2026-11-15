"""Funciones para guardar y recuperar información mediante archivos CSV."""

import csv
import math
import os
from datetime import datetime

from modelos import Ingreso, Gasto

CAMPOS_MOVIMIENTOS = ("fecha", "tipo", "categoria", "monto", "descripcion")
CAMPOS_PRESUPUESTOS = ("categoria", "limite_mensual")


def _crear_carpeta(ruta):
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)


def cargar_movimientos(ruta):
    """Devuelve (movimientos, cantidad_de_filas_invalidas) desde un CSV."""
    movimientos = []
    errores = 0

    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if not lector.fieldnames or not set(CAMPOS_MOVIMIENTOS).issubset(lector.fieldnames):
                return movimientos, 1

            for fila in lector:
                try:
                    fecha = datetime.strptime(fila["fecha"], "%Y-%m-%d").date()
                    tipo = fila["tipo"].strip().lower()
                    monto = float(fila["monto"])
                    categoria = fila["categoria"]
                    descripcion = fila.get("descripcion") or ""

                    if tipo == "ingreso":
                        movimiento = Ingreso(fecha, monto, categoria, descripcion)
                    elif tipo == "gasto":
                        movimiento = Gasto(fecha, monto, categoria, descripcion)
                    else:
                        raise ValueError("Tipo de movimiento desconocido.")
                    movimientos.append(movimiento)
                except (TypeError, ValueError, KeyError):
                    errores += 1
    except FileNotFoundError:
        pass

    return movimientos, errores


def guardar_movimientos(ruta, movimientos):
    """Guarda los movimientos sin perder comas ni caracteres especiales."""
    _crear_carpeta(ruta)
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_MOVIMIENTOS)
        escritor.writeheader()
        for movimiento in movimientos:
            escritor.writerow({
                "fecha": movimiento.fecha.isoformat(),
                "tipo": movimiento.tipo,
                "categoria": movimiento.categoria,
                "monto": f"{movimiento.monto:.2f}",
                "descripcion": movimiento.descripcion,
            })


def cargar_presupuestos(ruta):
    """Carga presupuestos válidos y omite filas dañadas."""
    presupuestos = {}
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if not lector.fieldnames or not set(CAMPOS_PRESUPUESTOS).issubset(lector.fieldnames):
                return presupuestos
            for fila in lector:
                try:
                    categoria = fila["categoria"].strip()
                    limite = float(fila["limite_mensual"])
                    if categoria and limite > 0 and math.isfinite(limite):
                        presupuestos[categoria] = round(limite, 2)
                except (TypeError, ValueError, AttributeError):
                    continue
    except FileNotFoundError:
        pass
    return presupuestos


def guardar_presupuestos(ruta, presupuestos):
    """Guarda los presupuestos mensuales en un archivo CSV."""
    _crear_carpeta(ruta)
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_PRESUPUESTOS)
        escritor.writeheader()
        for categoria, limite in presupuestos.items():
            escritor.writerow({"categoria": categoria, "limite_mensual": f"{limite:.2f}"})
