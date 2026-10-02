# Análisis de ventas de una tienda online con SQL

Proyecto de práctica de SQL sobre una tienda de tecnología en Lima: 8 consultas que responden preguntas de negocio usando `JOIN`, `GROUP BY`, CTE y funciones ventana.

> **Nota sobre los datos:** la base es **sintética** (generada con semilla fija por `generar_datos.py`) para poder practicar sin datos sensibles. El esquema y las consultas funcionan igual con datos reales.

## Preguntas de negocio

| # | Pregunta | Técnicas |
|---|----------|----------|
| Q1 | ¿Cuánto se vendió y cuál es el ticket promedio? | JOIN, SUM, COUNT DISTINCT |
| Q2 | ¿Qué categorías generan más ingresos? | CTE, `SUM() OVER ()` |
| Q3 | ¿Cómo evolucionan los ingresos mes a mes? | CTE, `LAG` |
| Q4 | ¿Qué distritos compran más? | JOIN de 4 tablas, LIMIT |
| Q5 | ¿Quiénes son los 10 mejores clientes? | `RANK` |
| Q6 | ¿Cuál es el producto líder de cada categoría? | `ROW_NUMBER() PARTITION BY` |
| Q7 | ¿Cuál es la tasa de cancelación mensual? | agregación condicional |
| Q8 | ¿Cuántos clientes nunca compraron? | `LEFT JOIN ... IS NULL` |

## Esquema

`clientes` ← `pedidos` → `detalle_pedido` → `productos`

## Cómo ejecutarlo

`§bash
pip install pandas
python generar_datos.py       # crea tienda_lima.db (SQLite)
python ejecutar_consultas.py  # ejecuta consultas.sql y guarda resultados/*.csv
`§

## Hallazgos (sobre los datos simulados)

- Solo se cuentan pedidos con estado `entregado` (unos 1.690 de 2.000).
- Laptops concentra ~56 % de los ingresos, y junto con Monitores suma ~80 %.
- Los ingresos mensuales crecen durante el año porque los clientes se registran de forma escalonada en la simulación; con datos reales habría que revisar estacionalidad.
- La tasa de cancelación se mueve entre 3 % y 11 %, sin tendencia clara.

## Qué aprendí / próximos pasos

- Practiqué modelado relacional y consultas analíticas.
- Próximo paso: conectar los resultados a un dashboard en Power BI y repetir el análisis con datos abiertos del Perú.
