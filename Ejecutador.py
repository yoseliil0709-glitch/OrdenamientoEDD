import os
import subprocess
import platform

def obtener_specs_hardware():
    print("[Ejecutador] Registrando especificaciones del hardware...")
    specs = f"""ESPECIFICACIONES DE HARDWARE Y SISTEMA
Sistema Operativo: {platform.system()} {platform.release()} ({platform.version()})
Arquitectura: {platform.machine()}
Procesador: {platform.processor()}
Python Version: {platform.python_version()}
"""
    with open("Hardware_Specs.txt", "w", encoding="utf-8") as f:
        f.write(specs)
    print("[Ejecutador] Hardware_Specs.txt generado con éxito.")

def ejecutar_lenguajes():
    tareas = [
        ("C#", "C#", [["dotnet", "run"]]),
        ("C++", "C++", [
            ["g++", "Ordenamientos.cpp", "-o", "Ordenamientos"],
            [os.path.join(".", "Ordenamientos.exe" if platform.system() == "Windows" else "./Ordenamientos")]
        ]),
        ("Java", "Java", [
            ["javac", "Ordenamientos.java"],
            ["java", "Ordenamientos"]
        ]),
        ("JavaScript", "JavaScript", [["node", "Ordenamientos.js"]]),
        ("Python", "Python", [["python", "Ordenamientos.py"]])
    ]

    global_csv = "Resultado.csv"
    with open(global_csv, "w", encoding="utf-8") as f:
        f.write("Lenguaje,Tamano,Algoritmo,Estado,TiempoMs,Comparaciones,Intercambios\n")

    for lang, carpeta, comandos in tareas:
        print(f"\n--- Procesando {lang} ---")
        if not os.path.exists(carpeta):
            print(f"[Aviso] No se encontró la carpeta '{carpeta}'. Se omite.")
            continue

        try:
            exito = True
            for cmd in comandos:
                resultado = subprocess.run(cmd, cwd=carpeta, capture_output=True, text=True)
                if resultado.returncode != 0:
                    print(f"[Error] Falló la ejecución en {lang}: {resultado.stderr.strip()}")
                    exito = False
                    break
                else:
                    print(resultado.stdout.strip())

            if exito:
                csv_local = os.path.join(carpeta, "Resultados.csv")
                if os.path.exists(csv_local):
                    with open(csv_local, "r", encoding="utf-8") as f_local:
                        lineas = f_local.readlines()
                        if len(lineas) > 1:
                            with open(global_csv, "a", encoding="utf-8") as f_global:
                                for linea in lineas[1:]: # Omitir cabecera local
                                    f_global.write(f"{lang},{linea}")
                    print(f"[Éxito] Resultados de {lang} integrados a Resultado.csv.")
                else:
                    print(f"[Aviso] El lenguaje {lang} no generó un archivo Resultados.csv local.")

        except Exception as e:
            print(f"[Excepción] Error inesperado procesando {lang}: {e}")

def analizar_resultados():
    global_csv = "Resultado.csv"
    if not os.path.exists(global_csv):
        print("\nNo se pudo generar el archivo global Resultado.csv.")
        return

    mejor_tiempo = float('inf')
    lang_mas_rapido = ""
    algo_mas_rapido = ""

    with open(global_csv, "r", encoding="utf-8") as f:
        lineas = f.readlines()[1:]
        for linea in lineas:
            partes = linea.strip().split(',')
            if len(partes) >= 7:
                lang, tam, algo, estado, tiempo, comp, inter = partes[:7]
                try:
                    t = float(tiempo)
                    if t > 0 and t < mejor_tiempo:
                        mejor_tiempo = t
                        lang_mas_rapido = lang
                        algo_mas_rapido = algo
                except ValueError:
                    continue

    print("\n" + "="*40)
    print("¡ORDENAMIENTOS FINALIZADOS!")
    print(f"Lenguaje más rápido: {lang_mas_rapido} (con {mejor_tiempo:.3f} ms)")
    print(f"Algoritmo más rápido: {algo_mas_rapido}")
    print("="*40)

if __name__ == "__main__":
    obtener_specs_hardware()
    ejecutar_lenguajes()
    analizar_resultados()