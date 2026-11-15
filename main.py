"""
main.py  -  Control de Gastos Personales
Programa de consola con menú. Se ejecuta con:   python main.py

"""

import math
from datetime import date, datetime

from modelos import Ingreso, Gasto
from gestor import GestorGastos, CATEGORIAS_GASTO, CATEGORIAS_INGRESO

RUTA_MOVIMIENTOS = "datos/movimientos.csv"
RUTA_PRESUPUESTOS = "datos/presupuestos.csv"

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def pedir_numero(mensaje):
    """Pide un número positivo y repite la pregunta hasta que sea válido."""
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))
            if not math.isfinite(valor) or valor <= 0:
                print("  ✗ Escribe un número válido mayor que cero.")
            else:
                return valor
        except ValueError:
            print("  ✗ Eso no es un número. Intenta de nuevo.")


def pedir_fecha(mensaje):
    """Pide una fecha AAAA-MM-DD. Si el usuario solo pulsa Enter, usa la de hoy."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return date.today()
        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()
            if fecha > date.today():
                print("  ⚠ La fecha es futura. Se registrará como movimiento programado.")
            return fecha
        except ValueError:
            print("  ✗ Formato incorrecto. Ejemplo: 2026-11-18")


def elegir_categoria(opciones):
    for numero, categoria in enumerate(opciones, start=1):
        print(f"   {numero}. {categoria}")
    while True:
        try:
            eleccion = int(input("  Número de categoría: "))
            if 1 <= eleccion <= len(opciones):
                return opciones[eleccion - 1]
            print("  ✗ Ese número no está en la lista.")
        except ValueError:
            print("  ✗ Escribe solo el número.")


def pedir_mes():
    hoy = date.today()
    while True:
        texto = input(f"  Mes (AAAA-MM) [Enter = {hoy.year}-{hoy.month:02d}]: ").strip()
        if texto == "":
            return hoy.year, hoy.month
        try:
            fecha = datetime.strptime(texto, "%Y-%m")
            return fecha.year, fecha.month
        except ValueError:
            print("  ✗ Formato incorrecto. Ejemplo: 2026-11")


def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


def registrar(gestor, clase, categorias, nombre):
    titulo(f"REGISTRAR {nombre.upper()}")
    fecha = pedir_fecha("  Fecha AAAA-MM-DD [Enter = hoy]: ")
    categoria = elegir_categoria(categorias)
    monto = pedir_numero("  Monto en B/.: ")
    descripcion = input("  Descripción (opcional): ").strip()
    try:
        movimiento = clase(fecha, monto, categoria, descripcion)
        gestor.agregar(movimiento)
        print(f"\n  ✔ {nombre.capitalize()} guardado.")
    except ValueError as error:
        print(f"  ✗ No se pudo guardar: {error}")
        return
    if clase is Gasto:
        for cat, total, limite, porc in gestor.alertas_presupuesto(fecha.year, fecha.month):
            if cat == categoria:
                aviso = "SUPERASTE" if porc >= 100 else "te acercas a"
                print(f"  ⚠ Atención: {aviso} el presupuesto de {cat} "
                      f"(B/. {total:.2f} de B/. {limite:.2f}, {porc}%).")


def mostrar_pares(pares):
    if not pares:
        print("  (No hay movimientos para mostrar.)")
        return
    print(f"  {'N°':>3}  {'Fecha':<10}  {'Tipo':<8} {'Categoría':<15} {'Monto':>12}  Descripción")
    for posicion, mov in pares:
        print(f"  {posicion + 1:>3}  {mov}")


def listar(gestor):
    titulo("MOVIMIENTOS")
    if not gestor.movimientos:
        print("  Todavía no hay movimientos. Registra uno o genera datos de ejemplo.")
        return
    criterio = "fecha"
    pagina = 1
    while True:
        pares = gestor.ordenados(criterio)
        visibles, total_paginas = gestor.paginar(pares, pagina)
        mostrar_pares(visibles)
        print(f"\n  Página {pagina} de {total_paginas}  |  ordenado por {criterio}")
        accion = input("  [S]iguiente  [A]nterior  [F]echa  [M]onto  [Enter] volver: ").strip().lower()
        if accion == "s":
            pagina += 1
        elif accion == "a":
            pagina -= 1
        elif accion == "f":
            criterio, pagina = "fecha", 1
        elif accion == "m":
            criterio, pagina = "monto", 1
        else:
            break
        pagina = min(max(pagina, 1), total_paginas)


def resumen(gestor):
    titulo("RESUMEN DEL MES")
    anio, mes = pedir_mes()
    datos = gestor.resumen_mes(anio, mes)
    print(f"\n  {MESES[mes - 1].capitalize()} de {anio}")
    print(f"  Ingresos : B/. {datos['ingresos']:>10.2f}")
    print(f"  Gastos   : B/. {datos['gastos']:>10.2f}")
    print(f"  Balance  : B/. {datos['balance']:>10.2f}")
    if datos["cantidad_gastos"] == 0:
        print("\n  No hay gastos registrados en ese mes.")
        return
    print(f"\n  {datos['cantidad_gastos']} gastos | promedio B/. {datos['promedio_gasto']:.2f} "
          f"| el mayor B/. {datos['mayor_gasto']:.2f}")
    print("\n  Gastos por categoría:")
    por_categoria = datos["por_categoria"]
    mayor = max(por_categoria, key=lambda c: por_categoria[c])
    for categoria, total in sorted(por_categoria.items(), key=lambda par: par[1], reverse=True):
        porcentaje = total / datos["gastos"] * 100
        barra = "█" * round(porcentaje / 5)
        print(f"   {categoria:<15} B/. {total:>9.2f}  {porcentaje:>5.1f}%  {barra}")
    print(f"\n  La categoría donde más gastaste fue: {mayor}.")


def presupuestos(gestor):
    titulo("PRESUPUESTOS MENSUALES")
    if gestor.presupuestos:
        for categoria, limite in gestor.presupuestos.items():
            print(f"   {categoria:<15} B/. {limite:>9.2f}")
    else:
        print("  Aún no has definido presupuestos.")
    print("\n  1. Definir o cambiar un presupuesto")
    print("  2. Ver alertas del mes")
    print("  Enter. Volver")
    opcion = input("  Opción: ").strip()
    if opcion == "1":
        categoria = elegir_categoria(CATEGORIAS_GASTO)
        limite = pedir_numero("  Límite mensual en B/.: ")
        gestor.definir_presupuesto(categoria, limite)
        print("  ✔ Presupuesto guardado.")
    elif opcion == "2":
        anio, mes = pedir_mes()
        alertas = gestor.alertas_presupuesto(anio, mes)
        if not alertas:
            print("  ✔ Ninguna categoría está cerca de su límite.")
        for categoria, total, limite, porc in alertas:
            estado = "SUPERADO" if porc >= 100 else "cerca del límite"
            print(f"   ⚠ {categoria}: B/. {total:.2f} de B/. {limite:.2f} ({porc}%) - {estado}")


def buscar(gestor):
    titulo("BUSCAR")
    texto = input("  Texto a buscar (categoría o descripción): ").strip()
    if texto == "":
        print("  ✗ No escribiste nada.")
        return
    resultados = gestor.buscar(texto)
    print(f"\n  {len(resultados)} resultado(s):")
    mostrar_pares(resultados)


def eliminar(gestor):
    titulo("ELIMINAR UN MOVIMIENTO")
    mostrar_pares(gestor.ordenados("fecha")[:10])
    print("  (Se muestran los 10 más recientes. Usa 'Buscar' para ver otros.)")
    try:
        numero = int(input("  Número a eliminar (Enter para cancelar): "))
        confirmar = input("  ¿Seguro? (s/n): ").strip().lower()
        if confirmar == "s":
            eliminado = gestor.eliminar(numero - 1)
            print(f"  ✔ Eliminado: {eliminado}")
        else:
            print("  Cancelado.")
    except ValueError:
        print("  Cancelado.")
    except IndexError as error:
        print(f"  ✗ {error}")


def datos_de_ejemplo(gestor):
    titulo("DATOS DE EJEMPLO")
    print("  Se agregarán gastos al azar de los últimos 90 días y 3 ingresos.")
    print("  Estos registros se mezclarán con tus movimientos actuales.")
    if input("  ¿Continuar? (s/n): ").strip().lower() == "s":
        gestor.generar_ejemplo()
        print("  ✔ Datos de ejemplo creados.")
        print("  Puedes retirarlos después desde la opción 9.")


def eliminar_ejemplos(gestor):
    titulo("ELIMINAR DATOS DE EJEMPLO")
    cantidad = sum(
        movimiento.descripcion in ("Gasto de ejemplo", "Ingreso de ejemplo")
        for movimiento in gestor.movimientos
    )
    if cantidad == 0:
        print("  No hay datos de ejemplo registrados.")
        return
    print(f"  Se encontraron {cantidad} movimiento(s) de ejemplo.")
    print("  Tus ingresos y gastos personales no serán eliminados.")
    if input("  ¿Deseas eliminarlos? (s/n): ").strip().lower() == "s":
        eliminados = gestor.eliminar_datos_ejemplo()
        print(f"  ✔ Se eliminaron {eliminados} movimiento(s) de ejemplo.")
    else:
        print("  Operación cancelada.")


def main():
    gestor = GestorGastos(RUTA_MOVIMIENTOS, RUTA_PRESUPUESTOS)
    titulo("CONTROL DE GASTOS PERSONALES")
    print(f"  {len(gestor.movimientos)} movimientos cargados | balance total: B/. {gestor.balance():.2f}")
    if gestor.lineas_con_error > 0:
        print(f"  ⚠ Se ignoraron {gestor.lineas_con_error} línea(s) dañadas del archivo.")

    while True:
        print("\n--------------- MENÚ ---------------")
        print("  1. Registrar ingreso")
        print("  2. Registrar gasto")
        print("  3. Ver movimientos")
        print("  4. Resumen del mes")
        print("  5. Presupuestos y alertas")
        print("  6. Buscar")
        print("  7. Eliminar un movimiento")
        print("  8. Generar datos de ejemplo")
        print("  9. Eliminar datos de ejemplo")
        print("  0. Salir")
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            registrar(gestor, Ingreso, CATEGORIAS_INGRESO, "ingreso")
        elif opcion == "2":
            registrar(gestor, Gasto, CATEGORIAS_GASTO, "gasto")
        elif opcion == "3":
            listar(gestor)
        elif opcion == "4":
            resumen(gestor)
        elif opcion == "5":
            presupuestos(gestor)
        elif opcion == "6":
            buscar(gestor)
        elif opcion == "7":
            eliminar(gestor)
        elif opcion == "8":
            datos_de_ejemplo(gestor)
        elif opcion == "9":
            eliminar_ejemplos(gestor)
        elif opcion == "0":
            gestor.guardar()
            print("\n  Datos guardados. ¡Hasta pronto!")
            break
        else:
            print("  ✗ Opción no válida.")


if __name__ == "__main__":
    main()
