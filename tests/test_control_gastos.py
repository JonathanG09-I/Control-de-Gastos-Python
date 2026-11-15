import tempfile
import unittest
from datetime import date
from pathlib import Path

from almacenamiento import cargar_movimientos, guardar_movimientos
from gestor import GestorGastos
from modelos import Gasto, Ingreso


class ModelosTests(unittest.TestCase):
    def test_ingreso_suma_al_balance(self):
        movimiento = Ingreso(date(2026, 1, 10), 100, "Beca")
        self.assertEqual(movimiento.efecto_en_balance(), 100)

    def test_gasto_resta_del_balance(self):
        movimiento = Gasto(date(2026, 1, 10), 25, "Alimentación")
        self.assertEqual(movimiento.efecto_en_balance(), -25)

    def test_rechaza_monto_no_positivo(self):
        with self.assertRaises(ValueError):
            Gasto(date(2026, 1, 10), 0, "Transporte")

    def test_rechaza_monto_infinito(self):
        with self.assertRaises(ValueError):
            Gasto(date(2026, 1, 10), float("inf"), "Transporte")


class PersistenciaTests(unittest.TestCase):
    def test_csv_con_comas_se_guarda_y_recupera(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "datos" / "movimientos.csv"
            original = Gasto(date(2026, 2, 3), 12.5, "Otros", "Café, pan y fruta")
            guardar_movimientos(str(ruta), [original])
            recuperados, errores = cargar_movimientos(str(ruta))

            self.assertEqual(errores, 0)
            self.assertEqual(len(recuperados), 1)
            self.assertEqual(recuperados[0].descripcion, "Café, pan y fruta")
            self.assertEqual(recuperados[0].monto, 12.5)


class GestorTests(unittest.TestCase):
    def test_balance_y_resumen_mensual(self):
        with tempfile.TemporaryDirectory() as temporal:
            gestor = GestorGastos(
                str(Path(temporal) / "movimientos.csv"),
                str(Path(temporal) / "presupuestos.csv"),
            )
            gestor.agregar(Ingreso(date(2026, 3, 1), 200, "Mesada"))
            gestor.agregar(Gasto(date(2026, 3, 2), 50, "Alimentación"))

            self.assertEqual(gestor.balance(), 150)
            self.assertEqual(gestor.resumen_mes(2026, 3)["balance"], 150)

    def test_paginacion_rechaza_cantidad_cero(self):
        with self.assertRaises(ValueError):
            GestorGastos.paginar([], 1, 0)

    def test_eliminar_datos_ejemplo_conserva_movimientos_personales(self):
        with tempfile.TemporaryDirectory() as temporal:
            gestor = GestorGastos(
                str(Path(temporal) / "movimientos.csv"),
                str(Path(temporal) / "presupuestos.csv"),
            )
            personal = Ingreso(date(2026, 3, 1), 500, "Mesada", "Ingreso personal")
            ejemplo = Gasto(date(2026, 3, 2), 25, "Otros", "Gasto de ejemplo")
            gestor.agregar(personal)
            gestor.agregar(ejemplo)

            eliminados = gestor.eliminar_datos_ejemplo()

            self.assertEqual(eliminados, 1)
            self.assertEqual(gestor.movimientos, [personal])
            self.assertEqual(gestor.balance(), 500)


if __name__ == "__main__":
    unittest.main()
