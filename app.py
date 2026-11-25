"""
MVP Venture One - Visualizador de inmuebles (versión con los datos actuales)
Ejecutar localmente:  streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

ARCHIVO = Path(__file__).parent / "data" / "processed" / "base_inmobiliaria_limpia.xlsx"

st.set_page_config(page_title="Venture One | MVP Inmuebles", layout="wide")


@st.cache_data
def cargar_datos(ruta: Path) -> pd.DataFrame:
    df = pd.read_excel(ruta)
    # Precio por m² calculado con el área del anuncio
    df["precio_m2"] = (df["precio"] / df["area_anuncio"]).round(0)
    # Textos uniformes para filtros
    for col in ["municipio_ubicacion", "barrio_ubicacion", "estado_inmueble"]:
        df[col] = df[col].astype(str).str.strip().str.title()
    return df


if not ARCHIVO.exists():
    st.error(f"No se encontró el archivo de datos: {ARCHIVO.name}. "
             "Súbelo a la carpeta data/ del repositorio.")
    st.stop()

df = cargar_datos(ARCHIVO)

# ---------------- Encabezado ----------------
st.title("Venture One · Consolidado de inmuebles")
st.caption("MVP con datos de prueba. Coordenadas y direcciones marcadas como "
           "aproximadas deben validarse antes de tomar decisiones.")

# ---------------- Filtros ----------------
st.sidebar.header("Filtros")
municipios = st.sidebar.multiselect(
    "Municipio", sorted(df["municipio_ubicacion"].unique()),
    default=sorted(df["municipio_ubicacion"].unique()))
datos = df[df["municipio_ubicacion"].isin(municipios)]

barrios = st.sidebar.multiselect(
    "Barrio", sorted(datos["barrio_ubicacion"].unique()),
    default=sorted(datos["barrio_ubicacion"].unique()))
datos = datos[datos["barrio_ubicacion"].isin(barrios)]

estados = st.sidebar.multiselect(
    "Estado del inmueble", sorted(datos["estado_inmueble"].unique()),
    default=sorted(datos["estado_inmueble"].unique()))
datos = datos[datos["estado_inmueble"].isin(estados)]

if datos.empty:
    st.warning("No hay inmuebles con esos filtros.")
    st.stop()

# ---------------- Indicadores ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Inmuebles", len(datos))
c2.metric("Precio promedio", f"${datos['precio'].mean():,.0f}")
c3.metric("Precio promedio por m²", f"${datos['precio_m2'].mean():,.0f}")
c4.metric("Sin dirección original", int(datos["direccion"].isna().sum()))

# ---------------- Mapa y gráfico ----------------
col_mapa, col_graf = st.columns(2)

with col_mapa:
    st.subheader("Ubicación")
    st.map(datos[datos["coordenadas_validas"]][["lat", "lon"]], zoom=12)

with col_graf:
    st.subheader("Precio por m² promedio por barrio")
    st.bar_chart(datos.groupby("barrio_ubicacion")["precio_m2"].mean().sort_values())

# ---------------- Tabla ----------------
st.subheader("Detalle por inmueble")
columnas = ["id_inmueble", "municipio_ubicacion", "barrio_ubicacion", "estado_inmueble",
            "area_anuncio", "precio", "precio_m2", "habitaciones", "banos",
            "parqueadero", "direccion_referencial", "fuente_direccion", "fuente"]
st.dataframe(datos[[c for c in columnas if c in datos.columns]],
             width="stretch", hide_index=True)
