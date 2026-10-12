"""
Recolector de datos de contaminacion atmosferica de Valencia.
Toma una muestra cada hora durante 24 horas y guarda los resultados en CSV.
"""

import os
import json
from time import sleep, strftime

import requests
import pandas as pd
from pyproj import Transformer

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------
SERVER_URL   = "https://geoportal.valencia.es/server/rest/services/OPENDATA/"
BASE_URL     = SERVER_URL + "MedioAmbiente/MapServer/156/query"
PARAMS       = {"f": "json", "outFields": "*", "where": "1=1"}

SLEEP_TIME   = 60 * 60                        # 1 hora en segundos
TOTAL_TIME   = (24 * 60 * 60) + SLEEP_TIME    # 25 horas para asegurar 24 muestras

OUTPUT_DIR   = "res"
OUTPUT_FILE  = os.path.join(OUTPUT_DIR, "valencia_pollution_dataset.csv")

# Columnas numericas que deben convertirse de object a float
NUMERIC_COLS = ["so2", "no2", "o3", "co", "pm10", "pm25", "lon", "lat"]

# ---------------------------------------------------------------------------
# Transformador de coordenadas UTM (EPSG:32630) -> GPS (EPSG:4326)
# ---------------------------------------------------------------------------
transformer = Transformer.from_crs("EPSG:32630", "EPSG:4326", always_xy=True)


def make_request(url, params):
    """Realiza una peticion GET y devuelve el JSON de la respuesta."""
    response = requests.get(url, params=params)
    if response:
        # Forzar UTF-8 para que caracteres como Tráfico, Molí no se corrompan
        response.encoding = "utf-8"
        return response.json()
    print(f"Error HTTP: {response.status_code}")
    raise Exception("Error al descargar JSON desde la API")


def fetch_dataframe():
    """Descarga las lecturas actuales de la API y las devuelve como DataFrame."""
    features = make_request(BASE_URL, PARAMS)["features"]

    df = pd.DataFrame()
    for feature in features:
        serie = pd.Series(feature["attributes"])
        # Convertir coordenadas de UTM a GPS lat/lon
        serie["lon"], serie["lat"] = transformer.transform(
            feature["geometry"]["x"], feature["geometry"]["y"]
        )
        df = pd.concat([df, serie.to_frame().T], axis=0, ignore_index=True)

    # Convertir epoch (ms) a timestamp ISO legible y guardarlo como string para el CSV
    df["fecha_carg"] = pd.to_datetime(df["fecha_carg"], unit="ms").dt.strftime("%Y-%m-%d %H:%M:%S")

    # Convertir columnas de contaminantes de object a float para calculos estadisticos
    df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(pd.to_numeric, errors="coerce")

    return df


def main():
    # Crear el directorio de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    current_time = 0
    # Escribir cabeceras solo si el archivo no existe o está vacío, evita duplicados al reiniciar
    first_write = not (os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0)

    print("=" * 60)
    print("Recolector de contaminacion atmosferica - Valencia")
    print(f"Guardando datos en: {OUTPUT_FILE}")
    print(f"Muestras cada:      {SLEEP_TIME // 60} minutos")
    print(f"Duracion total:     ~{TOTAL_TIME // 3600} horas")
    print("=" * 60)

    while current_time < TOTAL_TIME:
        timestamp = strftime("%Y-%m-%d %H:%M:%S")
        try:
            df = fetch_dataframe()
            # Guardar en CSV modo append con UTF-8-sig para que Excel y pandas lean tildes correctamente
            df.to_csv(OUTPUT_FILE, sep=",", header=first_write, mode="a", index=False, encoding="utf-8-sig")
            print(f"[{timestamp}] t={current_time}s | {len(df)} registros guardados")
            first_write = False
        except Exception as e:
            # Si falla una muestra, registra el error y continua en la siguiente hora
            print(f"[{timestamp}] ERROR en muestra: {e}")

        sleep(SLEEP_TIME)
        current_time += SLEEP_TIME

    print("\nRecoleccion completada.")
    print(f"Datos guardados en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
