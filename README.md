# MVP Venture One – Consolidación de información inmobiliaria

Reto empresarial 13 (EstudIA · Análisis de datos). Consolida anuncios, inmuebles de prueba y ubicaciones en una sola vista por inmueble.

## Estructura

```
├── app.py                 # Interfaz web (Streamlit)
├── requirements.txt       # Librerías que instala Streamlit Cloud
├── data/
│   ├── raw/               # Datos originales de la empresa (no se editan)
│   └── processed/         # Datos limpios; app.py lee base_inmobiliaria_limpia.xlsx
├── notebooks/             # Notebook de Colab con el proceso (SQL + Python)
├── powerbi/               # Tablero .pbix y capturas
└── docs/                  # Ficha del reto, diccionario y documentos de apoyo
```

## Ver la interfaz

- En línea: _[pegar aquí el enlace de Streamlit Cloud]_
- En local:
  ```
  pip install -r requirements.txt
  streamlit run app.py
  ```

## Proceso de datos

1. Carga de los tres archivos y conversión a tablas SQLite.
2. Cruce `Inmuebles_prueba` + `Anuncios_muestra` + `ubicaciones` (11 inmuebles, 0 sin coincidencia).
3. Limpieza: parqueaderos, normalización de coordenadas, validación de rango.
4. Dirección de referencia con OpenStreetMap para los inmuebles sin dirección (aproximada).

## Limitaciones conocidas (pendientes)

- Parqueaderos sin dato quedaron en 0 (supuesto).
- Algunas coordenadas son a nivel de barrio (inmuebles con la misma coordenada).
- Falta deduplicar la tabla de anuncios, unificar estados y calcular comparables.
- Falta integrar capas GeoJSON (Metro, equipamientos, POT).

## Equipo

- _Nombre 1_
- _Nombre 2_
