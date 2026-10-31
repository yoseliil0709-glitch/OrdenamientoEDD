import os
import csv
from collections import defaultdict

ARCHIVOS = {
    "Python": ["Python/ResultadosPython.txt", "Python/ResultadoMillonPython.txt"],
    "JavaScript": ["JavaScript/ResultadoJavascript.txt", "JavaScript/ResultadoMillonJavaScript.txt"],
    "Java": ["Java/ResultadosJava.txt", "Java/ResultadosMillonJava.txt"],
    "C++": ["C++/ResultadosC++.txt", "C++/ResultadosMillonC++.txt"],
    "C#": ["C#/ResultadosC#.txt", "C#/MillonC#.txt"]
}

TAMANOS = [100, 1000, 10000, 100000, 1000000]
ESTADOS = ["Aleatorio", "Ordenado", "Inverso"]

HARDWARE_INFO = """ESPECIFICACIONES DE HARDWARE
Sistema Operativo: Windows 11
Procesador: Intel64 Family 6 Model 122 Stepping 8, GenuineIntel
Python Versión: 3.14.7
"""

def leer_archivo(ruta):
    datos = []
    if not os.path.exists(ruta):
        print(f"Archivo no encontrado: {ruta}")
        return datos
    
    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    if not lineas:
        return datos
    
    header = lineas[0].strip()
    if '\t' in header:
        sep = '\t'
    else:
        sep = None
    
    for linea in lineas[1:]:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(sep) if sep else linea.split()
        
        if len(partes) >= 6:
            try:
                registro = {
                    'tamaño': int(partes[0]),
                    'algoritmo': partes[1],
                    'estado': partes[2],
                    'tiempoenms': float(partes[3]),
                    'comparaciones': int(partes[4]),
                    'intercambios': int(partes[5])
                }
                datos.append(registro)
                print(f"  Archivo: {ruta} | Lineas leidas: {len(datos)} | Headers: {partes[:6]}")
                continue
    
    return datos


def cargar_todos_los_datos():
    todos = {}
    for lenguaje, archivos in ARCHIVOS.items():
        datos_lenguaje = []
        for nombre_archivo in archivos:
            print(f"  Leyendo: {nombre_archivo}")
            datos_lenguaje.extend(leer_archivo(nombre_archivo))
        todos[lenguaje] = datos_lenguaje
        print(f"  → {lenguaje}: {len(datos_lenguaje)} archivos")
    return todos


def generar_reporte_lenguaje(lenguaje, datos, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(f"REPORTE DE ORDENAMIENTOS{lenguaje}\n")
        f.write(HARDWARE_INFO + "\n")
        
        f.write(f"{'Lenguaje':<12}| {'Algoritmo':<12}| {'Tamaño':<8}| {'Estado':<10}| {'Tiempo(ms)':<12}| {'Comparac.':<12}| {'Intercambio':<12}\n")
        f.write("-" * 90 + "\n")
        
        for reg in sorted(datos, key=lambda x: (x['tamano'], x['estado'], x['tiempoenms'])):
            f.write(f"{reg['tamano']:<12}| {reg['algoritmo']:<12}| {reg['estado']:<10}| {reg['tiempoenms']:<12.4f}| {reg['comparaciones']:<12}| {reg['intercambios']:<12}\n")
        
        f.write("Algoritmo mas rapido por tamaño y estado\n")
        
        for tam in TAMANOS:
            for estado in ESTADOS:
                filtrados = [d for d in datos if d['tamano'] == tam and d['estado'] == estado]
                if filtrados:
                    mas_rapido = min(filtrados, key=lambda x: x['tiempoenms'])
                    f.write(f"Tamaño {tam:>7}, Estado {estado:<10} → Más rápido: {mas_rapido['algoritmo']} ({mas_rapido['tiempoenms']:.4f} ms)\n")
   
        f.write("Menor tiempo promedio total\n")
        
        tiempos_alg = defaultdict(list)
        for reg in datos:
            tiempos_alg[reg['algoritmo']].append(reg['tiempoenms'])
        
        ranking = sorted(tiempos_alg.items(), key=lambda x: sum(x[1]) / len(x[1]))
        for i, (alg, tiempos) in enumerate(ranking, 1):
            promedio = sum(tiempos) / len(tiempos)
            f.write(f"  {i}. {alg:<12} | Promedio: {promedio:.4f} ms | Total: {sum(tiempos):.4f} ms\n")
    
    print(f"Reporte generado: {archivo_salida}")


def generar_comparacion_lenguajes(todos_datos, archivo_salida="ComparacionLenguajes.txt"):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("Comparacion entre los lenguajes de programacion\n")
        f.write("=" * 70 + "\n\n")
        f.write(HARDWARE_INFO + "\n")
        
        f.write(f"{'Tamaño':<8}| {'Algoritmo':<12}| {'Estado':<10}| {'Python(ms)':<12}| {'JS(ms)':<12}| {'Java(ms)':<12}| {'C++(ms)':<12}| {'C#(ms)':<12}| {'Más rápido':<12}\n")
        f.write("-" * 120 + "\n")
        
        python_datos = {(d['tamano'], d['algoritmo'], d['estado']): d for d in todos_datos.get('Python', [])}
        js_datos = {(d['tamano'], d['algoritmo'], d['estado']): d for d in todos_datos.get('JavaScript', [])}
        java_datos = {(d['tamano'], d['algoritmo'], d['estado']): d for d in todos_datos.get('Java', [])}
        cpp_datos = {(d['tamano'], d['algoritmo'], d['estado']): d for d in todos_datos.get('C++', [])}
        cs_datos = {(d['tamano'], d['algoritmo'], d['estado']): d for d in todos_datos.get('C#', [])}
        
        todas_claves = sorted(set(list(python_datos.keys()) + list(js_datos.keys()) + list(java_datos.keys()) + list(cpp_datos.keys()) + list(cs_datos.keys())))
        
        for clave in todas_claves:
            tam, alg, estado = clave
            p = python_datos.get(clave)
            j = js_datos.get(clave)
            ja = java_datos.get(clave)
            c = cpp_datos.get(clave)
            cs = cs_datos.get(clave)
            
            p_str = f"{p['tiempoenms']:.4f}" if p else "N/A"
            j_str = f"{j['tiempoenms']:.4f}" if j else "N/A"
            ja_str = f"{ja['tiempoenms']:.4f}" if ja else "N/A"
            c_str = f"{c['tiempoenms']:.4f}" if c else "N/A"
            cs_str = f"{cs['tiempoenms']:.4f}" if cs else "N/A"
            
            tiempos = []
            if p: tiempos.append(('Python', p['tiempoenms']))
            if j: tiempos.append(('JavaScript', j['tiempoenms']))
            if ja: tiempos.append(('Java', ja['tiempoenms']))
            if c: tiempos.append(('C++', c['tiempoenms']))
            if cs: tiempos.append(('C#', cs['tiempoenms']))
            
            ganador = min(tiempos, key=lambda x: x[1])[0] if tiempos else "N/A"
            
            f.write(f"{tam:<8}| {alg:<12}| {estado:<10}| {p_str:<12}| {j_str:<12}| {ja_str:<12}| {c_str:<12}| {cs_str:<12}| {ganador:<12}\n")
        
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("Conclusiones\n")
        f.write("=" * 70 + "\n\n")
        
        for lenguaje, datos in todos_datos.items():
            if datos:
                total = sum(d['tiempoenms'] for d in datos)
                f.write(f"Tiempo TOTAL {lenguaje}: {total:.4f} ms\n")
        
        f.write("\nMejor Algoritmo segun el lenguaje\n\n")
        for lenguaje, datos in todos_datos.items():
            if datos:
                tiempos_alg = defaultdict(list)
                for reg in datos:
                    tiempos_alg[reg['algoritmo']].append(reg['tiempoenms'])
                mejor = min(tiempos_alg.items(), key=lambda x: sum(x[1]) / len(x[1]))
                f.write(f"  {lenguaje}: {mejor[0]} (promedio: {sum(mejor[1])/len(mejor[1]):.4f} ms)\n")
    
    print(f"Comparación lista: {archivo_salida}")


def main():
    print("Gestor de comparaciones")
    
    print("Cargando datos de archivos .txt...\n")
    todos_datos = cargar_todos_los_datos()
    
    print("\nGenerando reportes individuales por lenguaje...\n")
    for lenguaje, datos in todos_datos.items():
        if datos:
            archivo = f"Reporte_{lenguaje}.txt"
            generar_reporte_lenguaje(lenguaje, datos, archivo)
        else:
            print(f"Sin datos para {lenguaje}, saltando...")
    
    print("\nGenerando comparación entre lenguajes...\n")
    generar_comparacion_lenguajes(todos_datos)
    
    print("\nArchivos generados:")
    print("  - Reporte_Python.txt")
    print("  - Reporte_JavaScript.txt")
    print("  - Reporte_Java.txt")
    print("  - Reporte_C++.txt")
    print("  - Reporte_C#.txt")
    print("  - ComparacionLenguajes.txt")

if __name__ == "__main__":
    main()