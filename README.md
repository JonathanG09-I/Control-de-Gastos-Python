# Control de Gastos Personales

Aplicación de consola desarrollada en Python para registrar ingresos y gastos, consultar balances, organizar movimientos y controlar presupuestos mensuales.

## Funcionalidades

- Registrar ingresos y gastos con fecha, categoría, monto y descripción.
- Consultar movimientos con paginación y orden por fecha o monto.
- Calcular el balance general y los resúmenes mensuales.
- Consultar los gastos agrupados por categoría y porcentaje.
- Definir presupuestos mensuales y recibir alertas al alcanzar el 80 % o superar el 100 %.
- Buscar movimientos por categoría o descripción.
- Eliminar movimientos registrados.
- Generar datos aleatorios de ejemplo y eliminarlos sin afectar los movimientos personales.
- Guardar información localmente en archivos CSV compatibles con Excel.
- Avisar cuando se registra un movimiento con fecha futura.

## Tecnologías y herramientas

- Módulos estándar: `csv`, `datetime`, `math`, `os` y `random`.
- **unittest** para pruebas automatizadas.

No requiere instalar paquetes externos.

## Cómo ejecutar el programa

1. Clona o descarga este repositorio.
2. Abre la carpeta del proyecto en Visual Studio Code o una terminal.
3. Ejecuta:

   ```bash
   python main.py
   ```

   En algunos equipos con Windows también puedes utilizar `py main.py`.

Los archivos de datos se crean automáticamente en la carpeta `datos/` al guardar información.

## Menú principal

| Opción | Descripción |
| --- | --- |
| 1 | Registrar un ingreso |
| 2 | Registrar un gasto |
| 3 | Consultar movimientos |
| 4 | Ver el resumen de un mes |
| 5 | Configurar presupuestos y consultar alertas |
| 6 | Buscar movimientos |
| 7 | Eliminar un movimiento |
| 8 | Generar datos de ejemplo |
| 9 | Eliminar únicamente los datos de ejemplo |
| 0 | Guardar y salir |

## Ejemplo de uso

Una ejecución de prueba con un ingreso de B/. 500.00 y un gasto de B/. 75.50 muestra un balance general de B/. 424.50. Los resúmenes mensuales separan los movimientos según su fecha.

```text
CONTROL DE GASTOS PERSONALES

1. Registrar ingreso
2. Registrar gasto
3. Ver movimientos
4. Resumen del mes
5. Presupuestos y alertas
6. Buscar
7. Eliminar un movimiento
8. Generar datos de ejemplo
9. Eliminar datos de ejemplo
0. Salir
```

## Estructura del proyecto

```text
Control-de-Gastos-Python/
├── main.py             # Menú e interacción con el usuario
├── gestor.py           # Reglas, cálculos, búsquedas y presupuestos
├── modelos.py          # Clases Movimiento, Ingreso y Gasto
├── almacenamiento.py   # Lectura y escritura de archivos CSV
├── tests/              # Pruebas automatizadas
├── datos/              # Datos locales (se crea al ejecutar)
├── .gitignore
└── README.md
```

## Conceptos de Python aplicados

- Variables, tipos de datos, operadores y expresiones.
- Condicionales, ciclos y funciones.
- Listas, tuplas, diccionarios y conjuntos.
- Comprensiones de listas y conjuntos.
- Funciones `lambda` y ordenamiento con `sorted()`.
- Módulos propios e importación de funciones y clases.
- Módulos estándar de Python.
- Manejo de excepciones (`try`, `except`).
- Lectura y escritura de archivos CSV.
- Programación orientada a objetos: clases, objetos, herencia, encapsulamiento y propiedades.

## Ejecutar las pruebas

Desde la carpeta principal del proyecto, ejecuta:

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican cálculos de ingresos y gastos, validaciones, persistencia CSV, resúmenes mensuales, paginación y eliminación segura de datos de ejemplo.

## Almacenamiento y privacidad

Los movimientos y presupuestos se guardan localmente en la carpeta `datos/`. Esta carpeta y los archivos CSV están excluidos del control de versiones para evitar publicar información financiera personal. Utiliza datos ficticios si deseas mostrar una demostración del programa.

Las fechas futuras se permiten, pero el programa muestra una advertencia para que el usuario identifique que está registrando un movimiento programado.

**Proyecto:** Portafolio de aprendizaje – Python
