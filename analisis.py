import numpy as np
import matplotlib.pyplot as plt


def cargar_y_limpiar_datos(filepath):
    fechas, pm25_list, pm10_list, temp_list, hum_list = [], [], [], [], []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    data_lines = lines[1:]

    print(f"Total de registros cargados: {len(data_lines)}")

    print("\n--- Primeras 5 filas del dataset ---")
    for i in range(min(5, len(data_lines))):
        print(data_lines[i])

    for line in data_lines:
        parts = line.split(',')

        fechas.append(parts[0])
        pm25_list.append(float(parts[1]) if parts[1] != '' else np.nan)
        pm10_list.append(float(parts[2]))
        temp_list.append(float(parts[3]))
        hum_list.append(float(parts[4]))

    pm25_arr = np.array(pm25_list)
    temp_arr = np.array(temp_list)

    # Limpieza: detección de outlier (>500) y reemplazo por NaN
    pm25_limpio = pm25_arr.copy()
    pm25_limpio[pm25_limpio > 500] = np.nan

    # Imputación de faltantes mediante la mediana de la serie
    mediana_val = np.nanmedian(pm25_limpio)
    pm25_limpio[np.isnan(pm25_limpio)] = mediana_val

    return fechas, pm25_arr, pm25_limpio, temp_arr


def realizar_analisis_estadistico(pm25_raw, pm25_clean):
    print("\n--- Métricas Estadísticas (NumPy) ---")

    print(
        f"Media sin limpiar (con outlier): "
        f"{np.nanmean(pm25_raw):.2f} ug/m3"
    )

    print(f"Media limpia: {np.mean(pm25_clean):.2f} ug/m3")
    print(f"Mediana limpia: {np.median(pm25_clean):.2f} ug/m3")
    print(
        f"Desviación Estándar limpia: "
        f"{np.std(pm25_clean):.2f} ug/m3"
    )
    print(f"Mínimo limpio: {np.min(pm25_clean):.2f} ug/m3")
    print(f"Máximo limpio: {np.max(pm25_clean):.2f} ug/m3")


def generar_visualizaciones(pm25_clean, temp_arr):
    plt.figure(figsize=(7, 4))

    plt.hist(
        pm25_clean,
        bins=6,
        color='skyblue',
        edgecolor='black'
    )

    plt.title('Distribución de PM2.5 en Cartago')
    plt.xlabel('Concentración (ug/m3)')
    plt.ylabel('Días')
    plt.tight_layout()

    plt.savefig('grafico_distribucion_pm25.png')
    plt.close()

    plt.figure(figsize=(7, 4))

    plt.scatter(
        temp_arr,
        pm25_clean,
        color='crimson'
    )

    plt.title('Relación Temperatura vs PM2.5')
    plt.xlabel('Temperatura (C)')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.tight_layout()

    plt.savefig('grafico_relacion_variables.png')
    plt.close()


if __name__ == '__main__':
    fechas, raw, clean, temp = cargar_y_limpiar_datos(
        'grupo_05.csv'
    )

    realizar_analisis_estadistico(raw, clean)

    generar_visualizaciones(clean, temp)