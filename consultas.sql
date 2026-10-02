-- Consultas de analisis para la tienda online (SQLite).
-- Cada bloque empieza con "-- Q<n>:" y es ejecutado por ejecutar_consultas.py

-- Q1: Ingresos totales y ticket promedio (solo pedidos entregados)
SELECT
    ROUND(SUM(d.cantidad * p.precio), 2)                       AS ingresos_totales,
    COUNT(DISTINCT o.id_pedido)                                AS pedidos_entregados,
    ROUND(SUM(d.cantidad * p.precio) / COUNT(DISTINCT o.id_pedido), 2) AS ticket_promedio
FROM pedidos o
JOIN detalle_pedido d ON d.id_pedido = o.id_pedido
JOIN productos p      ON p.id_producto = d.id_producto
WHERE o.estado = 'entregado';

-- Q2: Ingresos por categoria y su porcentaje del total
WITH ventas AS (
    SELECT p.categoria, SUM(d.cantidad * p.precio) AS ingresos
    FROM pedidos o
    JOIN detalle_pedido d ON d.id_pedido = o.id_pedido
    JOIN productos p      ON p.id_producto = d.id_producto
    WHERE o.estado = 'entregado'
    GROUP BY p.categoria
)
SELECT categoria,
       ROUND(ingresos, 2) AS ingresos,
       ROUND(100.0 * ingresos / SUM(ingresos) OVER (), 1) AS pct_del_total
FROM ventas
ORDER BY ingresos DESC;

-- Q3: Ingresos mensuales y variacion vs. el mes anterior (funcion ventana LAG)
WITH mensual AS (
    SELECT STRFTIME('%Y-%m', o.fecha) AS mes,
           SUM(d.cantidad * p.precio) AS ingresos
    FROM pedidos o
    JOIN detalle_pedido d ON d.id_pedido = o.id_pedido
    JOIN productos p      ON p.id_producto = d.id_producto
    WHERE o.estado = 'entregado'
    GROUP BY mes
)
SELECT mes,
       ROUND(ingresos, 2) AS ingresos,
       ROUND(100.0 * (ingresos - LAG(ingresos) OVER (ORDER BY mes))
             / LAG(ingresos) OVER (ORDER BY mes), 1) AS variacion_pct
FROM mensual
ORDER BY mes;

-- Q4: Top 5 distritos por ingresos
SELECT c.distrito,
       COUNT(DISTINCT o.id_pedido)              AS pedidos,
       ROUND(SUM(d.cantidad * p.precio), 2)     AS ingresos
FROM clientes c
JOIN pedidos o        ON o.id_cliente = c.id_cliente
JOIN detalle_pedido d ON d.id_pedido = o.id_pedido
JOIN productos p      ON p.id_producto = d.id_producto
WHERE o.estado = 'entregado'
GROUP BY c.distrito
ORDER BY ingresos DESC
LIMIT 5;

-- Q5: Top 10 clientes con ranking (RANK) y su gasto acumulado
SELECT RANK() OVER (ORDER BY SUM(d.cantidad * p.precio) DESC) AS ranking,
       c.nombre,
       c.distrito,
       ROUND(SUM(d.cantidad * p.precio), 2) AS gasto_total
FROM clientes c
JOIN pedidos o        ON o.id_cliente = c.id_cliente
JOIN detalle_pedido d ON d.id_pedido = o.id_pedido
JOIN productos p      ON p.id_producto = d.id_producto
WHERE o.estado = 'entregado'
GROUP BY c.id_cliente
ORDER BY ranking
LIMIT 10;

-- Q6: Producto mas vendido (unidades) dentro de cada categoria
WITH unidades AS (
    SELECT p.categoria, p.nombre, SUM(d.cantidad) AS unidades,
           ROW_NUMBER() OVER (PARTITION BY p.categoria ORDER BY SUM(d.cantidad) DESC) AS rn
    FROM detalle_pedido d
    JOIN productos p ON p.id_producto = d.id_producto
    JOIN pedidos o   ON o.id_pedido = d.id_pedido
    WHERE o.estado = 'entregado'
    GROUP BY p.id_producto
)
SELECT categoria, nombre, unidades FROM unidades WHERE rn = 1 ORDER BY unidades DESC;

-- Q7: Tasa de cancelacion por mes
SELECT STRFTIME('%Y-%m', fecha) AS mes,
       COUNT(*) AS pedidos,
       SUM(estado = 'cancelado') AS cancelados,
       ROUND(100.0 * SUM(estado = 'cancelado') / COUNT(*), 1) AS tasa_cancelacion_pct
FROM pedidos
GROUP BY mes
ORDER BY mes;

-- Q8: Clientes registrados que nunca compraron (LEFT JOIN + IS NULL)
SELECT COUNT(*) AS clientes_sin_compras
FROM clientes c
LEFT JOIN pedidos o ON o.id_cliente = c.id_cliente
WHERE o.id_pedido IS NULL;
