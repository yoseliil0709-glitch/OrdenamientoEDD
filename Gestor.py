import os
import glob
import platform

def obtener_specs_hardware():
    specs = {
        "Sistema Operativo": f"{platform.system()} {platform.release()}",
        "Arquitectura": platform.machine(),
        "Procesador": platform.processor() or "Desconocido",
        "Python Versión": platform.python_version()
    }
    return specs

def leer_resultados_txt():
    registros = []

    patrones = ["*Resultados*.txt", "*Resultado*.txt", "*/*.txt"]
    
    archivos_encontrados = set()
    for patron in patrones:
        for archivo in glob.glob(patron, recursive=True):
            if not any(x in archivo for x in ["Hardware", "Reporte", "Comparativo"]):
                archivos_encontrados.add(archivo)

    print(f"[Gestor] Archivos de resultados detectados: {list(archivos_encontrados)}")

    for archivo in archivos_encontrados:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                if not lineas:
                    continue
                
                nombre_lower = archivo.lower()
                if "python" in nombre_lower:
                    lenguaje = "Python"
                elif "javascript" in nombre_lower or "js" in nombre_lower:
                    lenguaje = "JavaScript"
                elif "java" in nombre_lower:
                    lenguaje = "Java"
                elif "cpp" in nombre_lower or "c++" in nombre_lower:
                    lenguaje = "C++"
                elif "cs" in nombre_lower or "c#" in nombre_lower:
                    lenguaje = "C#"
                else:
                    lenguaje = "Desconocido"

                inicio = 0
                if "Tamano" in lineas[0] or "Lenguaje" in lineas[0] or "Algoritmo" in lineas[0]:
                    inicio = 1

                for linea in lineas[inicio:]:
                    partes = linea.strip().split("\t")
                    if len(partes) < 6:
                        partes = linea.strip().split(",")  # Por si acaso usan comas

                    if len(partes) >= 6:
                        try:
                            if len(partes) >= 7 and not partes[0].isdigit():
                                lenguaje = partes[0]
                                algoritmo = partes[1]
                                tamano = int(partes[2])
                                estado = partes[3]
                                tiempo = float(partes[4])
                                comparaciones = int(partes[5])
                                intercambios = int(partes[6])
                            else:
                                algoritmo = partes[1]
                                tamano = int(partes[0])
                                estado = partes[2]
                                tiempo = float(partes[3])
                                comparaciones = int(partes[4])
                                intercambios = int(partes[5])

                            registros.append({
                                "lenguaje": lenguaje,
                                "algoritmo": algoritmo,
                                "tamano": tamano,
                                "estado": estado,
                                "tiempo": tiempo,
                                "comparaciones": comparaciones,
                                "intercambios": intercambios,
                                "archivo_fuente": archivo
                            })
                        except ValueError:
                            continue
        except Exception as e:
            print(f"[Advertencia] Error al procesar el archivo {archivo}: {e}")

    return registros

def main():
    print("       GESTOR COMPARATIVO DE LOS ORDENAMIENTOS   ")

    specs = obtener_specs_hardware()
    archivo_specs = "Hardware_Specs.txt"
    if not os.path.exists(archivo_specs):
        with open(archivo_specs, "w", encoding="utf-8") as f:
            f.write("=== ESPECIFICACIONES DE HARDWARE ===\n")
            for k, v in specs.items():
                f.write(f"{k}: {v}\n")

    registros = leer_resultados_txt()
    if not registros:
        print("[Error] No se encontraron datos válidos en los archivos .txt de los lenguajes.")
        return

    print(f"[Gestor] Se procesaron correctamente {len(registros)} registros de pruebas.")

    validos = [r for r in registros if r["tiempo"] > 0]
    if not validos:
        print("[Error] No hay registros de tiempo válidos para comparar.")
        return

    mas_rapido_global = min(validos, key=lambda x: x["tiempo"])

    tiempos_por_lenguaje = {}
    for r in validos:
        l = r["lenguaje"]
        tiempos_por_lenguaje.setdefault(l, []).append(r["tiempo"])
    
    promedio_lenguajes = {l: sum(t) / len(t) for l, t in tiempos_por_lenguaje.items()}
    lenguaje_ganador = min(promedio_lenguajes, key=promedio_lenguajes.get)

    tiempos_por_algoritmo = {}
    for r in validos:
        alg = r["algoritmo"]
        tiempos_por_algoritmo.setdefault(alg, []).append(r["tiempo"])

    promedio_algoritmos = {alg: sum(t) / len(t) for alg, t in tiempos_por_algoritmo.items()}
    algoritmo_ganador = min(promedio_algoritmos, key=promedio_algoritmos.get)

    nombre_reporte = "Reporte_Comparativo.txt"
    with open(nombre_reporte, "w", encoding="utf-8") as f:
        
        f.write("                     REPORTE FINAL DE LOS ORDENAMIENTOS                   \n")

        
        f.write("--- 1. ESPECIFICACIONES DE HARDWARE ---\n")
        for k, v in specs.items():
            f.write(f"  - {k}: {v}\n")
        f.write("\n" + "="*88 + "\n\n")

        f.write("2. RESULTADOS Y GANADORES DEL LOS ORDENAMIENTOS\n")
        f.write(f"Ejecución Individual Más Rápida:\n")
        f.write(f"     -> Lenguaje: {mas_rapido_global['lenguaje']} | Algoritmo: {mas_rapido_global['algoritmo']} | Tamaño: {mas_rapido_global['tamano']} | Estado: {mas_rapido_global['estado']} | Tiempo: {mas_rapido_global['tiempo']:.4f} ms\n\n")
        
        f.write(f"Lenguaje Más Rápido (En promedio general):\n")
        f.write(f"     -> {lenguaje_ganador} (Promedio: {promedio_lenguajes[lenguaje_ganador]:.4f} ms)\n\n")

        f.write(f"Algoritmo Más Rápido (En promedio general):\n")
        f.write(f"     -> {algoritmo_ganador} (Promedio: {promedio_algoritmos[algoritmo_ganador]:.4f} ms)\n\n")
        
        f.write("="*88 + "\n\n")
        f.write("3. DETALLES DE REGISTROS\n")
        f.write(f"{'Lenguaje':<12} | {'Algoritmo':<12} | {'Tamaño':<10} | {'Estado':<12} | {'Tiempo (ms)':<15} | {'Comparaciones':<15} | {'Intercambios':<15}\n")
        f.write("-" * 105 + "\n")
        
        for r in registros:
            f.write(f"{r['lenguaje']:<12} | {r['algoritmo']:<12} | {str(r['tamano']):<10} | {r['estado']:<12} | {str(r['tiempo']):<15} | {str(r['comparaciones']):<15} | {str(r['intercambios']):<15}\n")

    print(f"\n[¡Éxito!] Se ha generado el archivo '{nombre_reporte}' con toda la comparativa.")
    print(f"Ganador general - Lenguaje más rápido: {lenguaje_ganador}")
    print(f"Ganador general - Algoritmo más rápido: {algoritmo_ganador}")

if __name__ == "__main__":
    main()