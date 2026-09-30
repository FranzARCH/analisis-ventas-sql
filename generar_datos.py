"""Genera una base SQLite con datos SINTETICOS de una tienda online en Lima.

Los datos son simulados (semilla fija) para practicar SQL. Reemplazalos por
datos reales/abiertos cuando los tengas: el esquema y las consultas se mantienen.
"""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
DB = Path(__file__).parent / "tienda_lima.db"

DISTRITOS = ["Miraflores", "San Isidro", "San Miguel", "Surco", "Lince",
             "La Molina", "Comas", "Villa El Salvador", "San Juan de Lurigancho"]
CATEGORIAS = {
    "Laptops": (1800, 4500), "Perifericos": (40, 350), "Audio": (60, 900),
    "Monitores": (450, 1800), "Almacenamiento": (90, 700),
}
SINGULAR = {"Laptops": "Laptop", "Perifericos": "Periferico", "Audio": "Audio",
            "Monitores": "Monitor", "Almacenamiento": "Almacenamiento"}
NOMBRES = ["Ana", "Luis", "Carla", "Diego", "Rosa", "Jose", "Lucia", "Mateo",
           "Sofia", "Pedro", "Valeria", "Andres", "Camila", "Jorge", "Elena"]
APELLIDOS = ["Quispe", "Huaman", "Flores", "Rojas", "Chavez", "Vargas",
             "Mendoza", "Torres", "Castillo", "Ramos"]


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE clientes (
        id_cliente INTEGER PRIMARY KEY, nombre TEXT, distrito TEXT, fecha_registro DATE);
    CREATE TABLE productos (
        id_producto INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL);
    CREATE TABLE pedidos (
        id_pedido INTEGER PRIMARY KEY, id_cliente INTEGER, fecha DATE, estado TEXT,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente));
    CREATE TABLE detalle_pedido (
        id_pedido INTEGER, id_producto INTEGER, cantidad INTEGER,
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto));
    """)

    inicio = date(2025, 1, 1)
    clientes = []
    for i in range(1, 301):
        nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
        f = inicio + timedelta(days=random.randint(0, 300))
        clientes.append((i, nombre, random.choice(DISTRITOS), f.isoformat()))
    cur.executemany("INSERT INTO clientes VALUES (?,?,?,?)", clientes)

    productos = []
    pid = 1
    for cat, (lo, hi) in CATEGORIAS.items():
        for k in range(1, 9):
            productos.append((pid, f"{SINGULAR[cat]} modelo {k}",
                              cat, round(random.uniform(lo, hi), 2)))
            pid += 1
    cur.executemany("INSERT INTO productos VALUES (?,?,?,?)", productos)

    pedidos, detalle = [], []
    for id_pedido in range(1, 2001):
        cli = random.choice(clientes)
        f_reg = date.fromisoformat(cli[3])
        f = f_reg + timedelta(days=random.randint(0, max(1, (date(2025, 12, 31) - f_reg).days)))
        estado = random.choices(["entregado", "cancelado", "pendiente"], [0.85, 0.08, 0.07])[0]
        pedidos.append((id_pedido, cli[0], f.isoformat(), estado))
        for prod in random.sample(productos, random.randint(1, 3)):
            detalle.append((id_pedido, prod[0], random.randint(1, 3)))
    cur.executemany("INSERT INTO pedidos VALUES (?,?,?,?)", pedidos)
    cur.executemany("INSERT INTO detalle_pedido VALUES (?,?,?)", detalle)
    con.commit()
    con.close()
    print(f"Base creada: {DB.name} | {len(clientes)} clientes, {len(productos)} productos, "
          f"{len(pedidos)} pedidos, {len(detalle)} lineas de detalle")


if __name__ == "__main__":
    main()
