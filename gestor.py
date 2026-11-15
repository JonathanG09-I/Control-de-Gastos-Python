"""
gestor.py
Lógica del programa: la clase GestorGastos administra los movimientos,
los presupuestos y los cálculos. No contiene menús ni input/print;
eso está en main.py (así cada archivo tiene una sola responsabilidad).
"""

import math
import random
from datetime import date, timedelta

from modelos import Ingreso, Gasto
from almacenamiento import (cargar_movimientos, guardar_movimientos,
                            cargar_presupuestos, guardar_presupuestos)

CATEGORIAS_GASTO = ("Alimentación", "Transporte", "Vivienda", "Servicios",
                    "Salud", "Educación", "Ocio", "Otros")
CATEGORIAS_INGRESO = ("Mesada", "Salario", "Beca", "Otros ingresos")

RANGOS_EJEMPLO = {
    "Alimentación": (3, 25), "Transporte": (1, 12), "Vivienda": (60, 150),
    "Servicios": (15, 60), "Salud": (5, 40), "Educación": (5, 50),
    "Ocio": (3, 30), "Otros": (2, 20),
}


class GestorGastos:
    """Administra los movimientos (ingresos y gastos) y los presupuestos."""

    def __init__(self, ruta_movimientos, ruta_presupuestos):
        self.ruta_movimientos = ruta_movimientos
        self.ruta_presupuestos = ruta_presupuestos
        self.movimientos, self.lineas_con_error = cargar_movimientos(ruta_movimientos)
        self.presupuestos = cargar_presupuestos(ruta_presupuestos)

    def guardar(self):
        guardar_movimientos(self.ruta_movimientos, self.movimientos)
        guardar_presupuestos(self.ruta_presupuestos, self.presupuestos)

    def agregar(self, movimiento):
        self.movimientos.append(movimiento)
        self.guardar()

    def eliminar(self, posicion):
        """Elimina el movimiento en esa posición (empezando en 0) y lo devuelve."""
        if posicion < 0 or posicion >= len(self.movimientos):
            raise IndexError("No existe un movimiento con ese número.")
        eliminado = self.movimientos.pop(posicion)
        self.guardar()
        return eliminado

    def definir_presupuesto(self, categoria, limite):
        if not math.isfinite(limite) or limite <= 0:
            raise ValueError("El presupuesto debe ser un número mayor que cero.")
        self.presupuestos[categoria] = round(limite, 2)
        self.guardar()

    def balance(self):
        """Suma de todos los efectos: ingresos suman, gastos restan."""
        return round(sum(m.efecto_en_balance() for m in self.movimientos), 2)

    def movimientos_del_mes(self, anio, mes):
        """Devuelve los movimientos de un año y mes."""
        return [m for m in self.movimientos
                if m.fecha.year == anio and m.fecha.month == mes]

    def categorias_usadas(self):
        return {m.categoria for m in self.movimientos}

    def meses_con_datos(self):
        meses = {(m.fecha.year, m.fecha.month) for m in self.movimientos}
        return sorted(meses)

    def buscar(self, texto):
        texto = texto.lower()
        return [(pos, m) for pos, m in enumerate(self.movimientos)
                if texto in m.categoria.lower() or texto in m.descripcion.lower()]

    def ordenados(self, criterio):
        pares = list(enumerate(self.movimientos))
        if criterio == "monto":
            return sorted(pares, key=lambda par: par[1].monto, reverse=True)
        return sorted(pares, key=lambda par: par[1].fecha, reverse=True)

    @staticmethod
    def paginar(lista, pagina, por_pagina=10):
        if por_pagina <= 0:
            raise ValueError("La cantidad de elementos por página debe ser mayor que cero.")
        total_paginas = max(1, math.ceil(len(lista) / por_pagina))
        pagina = min(max(pagina, 1), total_paginas)
        inicio = (pagina - 1) * por_pagina
        return lista[inicio:inicio + por_pagina], total_paginas

    def gastos_por_categoria(self, movimientos):
        totales = {}
        for m in movimientos:
            if m.tipo == "gasto":
                totales[m.categoria] = round(totales.get(m.categoria, 0) + m.monto, 2)
        return totales

    def resumen_mes(self, anio, mes):
        movs = self.movimientos_del_mes(anio, mes)
        ingresos = round(sum(m.monto for m in movs if m.tipo == "ingreso"), 2)
        lista_gastos = [m.monto for m in movs if m.tipo == "gasto"]
        gastos = round(sum(lista_gastos), 2)
        por_categoria = self.gastos_por_categoria(movs)
        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": round(ingresos - gastos, 2),
            "cantidad_gastos": len(lista_gastos),
            "promedio_gasto": round(gastos / len(lista_gastos), 2) if lista_gastos else 0,
            "mayor_gasto": max(lista_gastos) if lista_gastos else 0,
            "por_categoria": por_categoria,
        }

    def alertas_presupuesto(self, anio, mes, umbral=80):
        gastado = self.gastos_por_categoria(self.movimientos_del_mes(anio, mes))
        alertas = []
        for categoria, limite in self.presupuestos.items():
            total = gastado.get(categoria, 0)
            porcentaje = round(total / limite * 100, 1)
            if porcentaje >= umbral:
                alertas.append((categoria, total, limite, porcentaje))
        return sorted(alertas, key=lambda a: a[3], reverse=True)

    def generar_ejemplo(self, cantidad=40):
        hoy = date.today()
        for _ in range(cantidad):
            fecha = hoy - timedelta(days=random.randint(0, 89))
            categoria = random.choice(CATEGORIAS_GASTO)
            minimo, maximo = RANGOS_EJEMPLO[categoria]
            monto = round(random.uniform(minimo, maximo), 2)
            self.movimientos.append(Gasto(fecha, monto, categoria, "Gasto de ejemplo"))
        for meses_atras in range(3):
            fecha = hoy - timedelta(days=30 * meses_atras)
            self.movimientos.append(Ingreso(fecha, 400, "Mesada", "Ingreso de ejemplo"))
        self.movimientos.sort(key=lambda m: m.fecha)
        self.guardar()

    def eliminar_datos_ejemplo(self):
        cantidad_inicial = len(self.movimientos)
        self.movimientos = [
            movimiento for movimiento in self.movimientos
            if movimiento.descripcion not in ("Gasto de ejemplo", "Ingreso de ejemplo")
        ]
        eliminados = cantidad_inicial - len(self.movimientos)
        if eliminados:
            self.guardar()
        return eliminados
