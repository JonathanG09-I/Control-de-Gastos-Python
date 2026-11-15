"""Modelos de datos para los ingresos y gastos personales."""

import math
from datetime import date


class Movimiento:
    """Representa una entrada o salida de dinero."""

    tipo = "movimiento"

    def __init__(self, fecha, monto, categoria, descripcion=""):
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser un objeto date.")
        self.fecha = fecha
        self.__monto = 0.0
        self.monto = monto
        self.categoria = str(categoria).strip()
        if not self.categoria:
            raise ValueError("La categoría no puede estar vacía.")
        self.descripcion = str(descripcion).strip()

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El monto debe ser un número válido.") from error
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("El monto debe ser un número mayor que cero.")
        self.__monto = round(valor, 2)

    def efecto_en_balance(self):
        """Devuelve el efecto del movimiento sobre el balance."""
        return 0.0

    def __str__(self):
        return (f"{self.fecha}  {self.tipo.capitalize():<8} {self.categoria:<15} "
                f"B/. {self.monto:>9.2f}  {self.descripcion}")


class Ingreso(Movimiento):
    """Dinero que entra, por ejemplo una mesada, salario o beca."""

    tipo = "ingreso"

    def efecto_en_balance(self):
        return self.monto


class Gasto(Movimiento):
    """Dinero que sale."""

    tipo = "gasto"

    def efecto_en_balance(self):
        return -self.monto
