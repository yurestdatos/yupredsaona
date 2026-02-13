from django.shortcuts import render
import pandas as pd
from datetime import datetime
from db import bd_llamada_ocr


def tabla_consumos(request):

    query = """
    SELECT
        id_local,
        nombre_local,
        fecha,
        id_producto,
        nombre_producto,
        cantidad,
        u_medida,
        cantidad_conv,
        u_conv
    FROM yupred_saona
    """

    df = bd_llamada_ocr(query, params_tuple=())

    # Fecha real para filtros
    df["fecha_real"] = pd.to_datetime(df["fecha"]).dt.date

    # Fecha formateada para mostrar
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%d/%m/%Y")

    # Crear columnas unificadas
    def formatear_num(x):
        if pd.isna(x):
            return ""
        x = round(float(x), 3)
        if x.is_integer():
            return str(int(x))
        return str(x).rstrip("0").rstrip(".")

    df["CANTIDAD"] = (
    "<span class='num'>" +
    df["cantidad"].apply(formatear_num) +
    "</span><span class='unit'>" +
    df["u_medida"].astype(str) +
    "</span>")

    df["CANTIDAD CONV"] = (
        "<span class='num'>" +
        df["cantidad_conv"].apply(formatear_num) +
        "</span><span class='unit'>" +
        df["u_conv"].astype(str) +
        "</span>")



    # Renombrar columnas
    df = df.rename(columns={
        "nombre_local": "NOMBRE LOCAL",
        "fecha": "FECHA",
        "id_producto": "ID PRODUCTO",
        "nombre_producto": "NOMBRE PRODUCTO"
    })

    # Mantener solo las columnas finales
    df = df[
        [
            "NOMBRE LOCAL",
            "FECHA",
            "ID PRODUCTO",
            "NOMBRE PRODUCTO",
            "CANTIDAD",
            "CANTIDAD CONV",
            "fecha_real"
        ]
    ]

    # Listas para filtros
    locales = sorted(df["NOMBRE LOCAL"].unique())
    productos = sorted(df["NOMBRE PRODUCTO"].unique())

    fechas_unicas = sorted(df["fecha_real"].unique())
    fechas = [
        {"value": d.strftime("%Y-%m-%d"), "label": d.strftime("%d/%m/%Y")}
        for d in fechas_unicas
    ]

    local_sel = request.GET.get("local")
    fecha_sel = request.GET.get("fecha")
    producto_sel = request.GET.get("producto")

    # Fecha por defecto (última) solo en primera carga
    if "fecha" not in request.GET and len(fechas_unicas) > 0:
        fecha_sel = fechas_unicas[-1].strftime("%Y-%m-%d")

    # Filtros
    if local_sel:
        df = df[df["NOMBRE LOCAL"] == local_sel]

    if fecha_sel:
        try:
            fecha_sel_date = datetime.strptime(fecha_sel, "%Y-%m-%d").date()
            df = df[df["fecha_real"] == fecha_sel_date]
        except:
            pass

    if producto_sel:
        df = df[df["NOMBRE PRODUCTO"] == producto_sel]

    # Quitar columna interna
    df = df.drop(columns=["fecha_real"])

    context = {
        "tabla": df.to_dict(orient="records"),
        "columnas": df.columns,
        "locales": locales,
        "fechas": fechas,
        "productos": productos,
        "local_sel": local_sel,
        "fecha_sel": fecha_sel,
        "producto_sel": producto_sel
    }

    return render(request, "consumos/tabla.html", context)
