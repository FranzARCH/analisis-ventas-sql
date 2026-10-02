"""Ejecuta consultas.sql sobre tienda_lima.db y guarda cada resultado en resultados/*.csv"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).parent
DB = AQUI / "tienda_lima.db"
SALIDA = AQUI / "resultados"


def main():
    if not DB.exists():
        raise SystemExit("Falta la base de datos. Ejecuta primero: python generar_datos.py")
    SALIDA.mkdir(exist_ok=True)
    texto = (AQUI / "consultas.sql").read_text(encoding="utf-8")
    bloques = re.split(r"^-- (Q\d+): (.*)$", texto, flags=re.MULTILINE)[1:]
    con = sqlite3.connect(DB)
    for i in range(0, len(bloques), 3):
        codigo, titulo, sql = bloques[i], bloques[i + 1], bloques[i + 2]
        df = pd.read_sql_query(sql.strip().rstrip(";"), con)
        df.to_csv(SALIDA / f"{codigo.lower()}.csv", index=False)
        print(f"\n=== {codigo}: {titulo} ===")
        print(df.to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()
