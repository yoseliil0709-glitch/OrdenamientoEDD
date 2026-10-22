import os
import subprocess
import platform
import pandas as pd

ES_WINDOWS = platform.system() == "Windows"

def ejecutar_comandos():
    print("=" * 70)
    print("       EJECUTANDO BENCHMARK (TAMAÑO: 100) - LOS 5 LENGUAJES       ")
    print("=" * 70)

    # 1. PYTHON
    print("\n[1/5] Ejecutando Python...")
    try:
        subprocess.run(["python", "Python/Ordenamientos.py"], check=True)
    except Exception as e:
        print(f"-> Error en Python: {e}")

    # 2. JAVASCRIPT
    print("\n[2/5] Ejecutando JavaScript...")
    try:
        subprocess.run(["node", "JavaScript/Ordenamientos.js"], check=True)
    except Exception as e:
        print(f"-> Error en JavaScript: {e}")

    # 3. JAVA
    print("\n[3/5] Ejecutando Java...")
    try:
        subprocess.run(["javac", "Java/Ordenamientos.java"], check=True)
        subprocess.run(["java", "-cp", "Ordenamientos"], check=True)
    except Exception as e:
        print(f"-> Error en Java: {e}")

    # 4. C++
    print("\n[4/5] Ejecutando C++...")
    try:
        salida_exe = "programa_cpp.exe" if ES_WINDOWS else "./programa_cpp"
        subprocess.run(["g++", "C++/Ordenamientos.cpp", "-o", "programa_cpp", "-O3"], check=True)
        subprocess.run([salida_exe if ES_WINDOWS else "./programa_cpp"], check=True)
    except Exception as e:
        print(f"-> Error en C++: {e}")

    # 5. C#
    print("\n[5/5] Ejecutando C#...")
    try:
        subprocess.run(["dotnet", "run"], check=True)
    except Exception as e:
        print(f"-> Error en C#: {e}")

def generar_reporte_txt():
    print("\nAnalizando y generando el reporte en TXT...")
    
    archivos = [
        "Resultados.csv", "Resultado.csv",
        "C/Resultados.csv", "C++/Resultado.csv",
        "Java/Resultados.csv", "JavaScript/Resultado.csv",
        "C#/Resultados.csv"
    ]

    todos_los_datos = []
    for ruta in archivos:
        if os.path.exists(ruta):
            try:
                df = pd.read_csv(ruta)
                todos_los_datos.append(df)
            except:
                pass

    if not todos_los_datos:
        print(" No se encontraron archivos CSV para consolidar.")
        return

    df_total = pd.concat(todos_los_datos, ignore_index=True).drop_duplicates()

    # Filtrar estrictamente para el tamaño 100
    df_100 = df_total[df_total["Tamano"] == 100]

    if df_100.empty:
        print("No hay registros con tamaño 100 en los CSV.")
        return

    # Encontrar el absoluto ganador para tamaño 100
    ganador = df_100.loc[df_100["TiempoMs"].idxmin()]

    # Crear el archivo de reporte en formato TXT
    nombre_txt = "Reporte_Resultados_100.txt"
    with open(nombre_txt, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("           REPORTE DE BENCHMARKING - ORDENAMIENTOS (TAMAÑO 100)\n")
        f.write("=" * 65 + "\n\n")
        
        f.write("GANADOR ABSOLUTO PARA EL TAMAÑO 100:\n")
        f.write(f"   - Lenguaje:      {ganador['Lenguaje']}\n")
        f.write(f"   - Algoritmo:     {ganador['Algoritmo']}\n")
        f.write(f"   - Estado:        {ganador['Estado']}\n")
        f.write(f"   - Tiempo:        {ganador['TiempoMs']} ms\n")
        f.write(f"   - Comparaciones: {ganador['Comparaciones']}\n")
        f.write(f"   - Intercambios:  {ganador['Intercambios']}\n\n")
        
        f.write("-" * 65 + "\n")
        f.write("TABLA GENERAL DE RESULTADOS (ORDENADOS POR TIEMPO):\n")
        f.write("-" * 65 + "\n")
        
        # Ordenar los datos del tamaño 100 de menor a mayor tiempo
        df_ordenado = df_100.sort_values(by="TiempoMs", ascending=True)
        f.write(df_ordenado.to_string(index=False))
        f.write("\n\n" + "=" * 65 + "\n")

    print(f"\n¡Listo! El reporte se ha guardado exitosamente en el archivo: '{nombre_txt}'.")

if __name__ == "__main__":
    # Recuerda configurar temporalmente cada archivo de lenguaje con tamanios = [100]
    ejecutar_comandos()
    generar_reporte_txt()