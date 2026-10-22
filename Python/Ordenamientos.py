import csv
import random
import time
import sys

sys.setrecursionlimit(2000000)

class BenchmarkOrdenamiento:
    def __init__(self):
        self.comparaciones = 0
        self.intercambios = 0

    def reiniciar_contadores(self):
        self.comparaciones = 0
        self.intercambios = 0

    # Ordenamiento Insercion 1
    def insertion_sort(self, a):
        self.reiniciar_contadores()
        for i in range(1, len(a)):
            temp = a[i]
            j = i - 1
            self.comparaciones += 1
            while j >= 0 and temp < a[j]:
                self.comparaciones += 1
                a[j + 1] = a[j]
                self.intercambios += 1
                j = j - 1
            a[j + 1] = temp

    # Ordenamiento Seleccion 2
    def selection_sort(self, a):
        self.reiniciar_contadores()
        n = len(a)
        for i in range(n):
            small = i
            for j in range(i + 1, n):
                self.comparaciones += 1
                if a[small] > a[j]:
                    small = j
            if small != i:
                a[i], a[small] = a[small], a[i]
                self.intercambios += 1

    # Ordenamiento Burbuja 3
    def bubble_sort(self, a):
        self.reiniciar_contadores()
        n = len(a)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparaciones += 1
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    self.intercambios += 1
                    swapped = True
            if not swapped:
                break

    # Ordenamiento MergeSort 4
    def merge_sort(self, a):
        self.reiniciar_contadores()
        self._merge_sort_rec(a, 0, len(a) - 1)

    def _merge_sort_rec(self, a, l, r):
        if l < r:
            m = (l + r) // 2
            self._merge_sort_rec(a, l, m)
            self._merge_sort_rec(a, m + 1, r)
            self._merge(a, l, m, r)

    def _merge(self, a, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = [a[l + i] for i in range(n1)]
        R = [a[m + 1 + j] for j in range(n2)]

        i = 0
        j = 0
        k = l
        while i < n1 and j < n2:
            self.comparaciones += 1
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            self.intercambios += 1
            k += 1

        while i < n1:
            a[k] = L[i]
            i += 1
            k += 1
            self.intercambios += 1

        while j < n2:
            a[k] = R[j]
            j += 1
            k += 1
            self.intercambios += 1

    # Ordenamiento QuickSort 5
    def quick_sort(self, a):
        self.reiniciar_contadores()
        self._quick_sort_rec(a, 0, len(a) - 1)

    def _quick_sort_rec(self, a, l, h):
        if l < h:
            pi = self._partition(a, l, h)
            self._quick_sort_rec(a, l, pi - 1)
            self._quick_sort_rec(a, pi + 1, h)

    def _partition(self, a, l, h):
        pvt = a[h]
        j = l - 1
        for k in range(l, h):
            self.comparaciones += 1
            if a[k] < pvt:
                j += 1
                a[j], a[k] = a[k], a[j]
                self.intercambios += 1
        a[j + 1], a[h] = a[h], a[j + 1]
        self.intercambios += 1
        return j + 1

    # Ordenamiento ShellSort 6
    def shell_sort(self, a):
        self.reiniciar_contadores()
        size = len(a)
        gapSize = size // 2
        while gapSize > 0:
            for j in range(gapSize, size):
                val = a[j]
                k = j
                while k >= gapSize:
                    self.comparaciones += 1
                    if a[k - gapSize] > val:
                        a[k] = a[k - gapSize]
                        self.intercambios += 1
                        k -= gapSize
                    else:
                        break
                a[k] = val
            gapSize //= 2

    # Ordenamiento Radix 7
    def radix_sort(self, a):
        self.reiniciar_contadores()
        if not a:
            return
        max1 = max(a)
        exp = 1
        while max1 // exp > 0:
            self._counting_sort_radix(a, exp)
            exp *= 10

    def _counting_sort_radix(self, arr, exp):
        s = len(arr)
        outputArray = [0] * s
        countArray = [0] * 10

        for j in range(s):
            idx = (arr[j] // exp) % 10
            countArray[idx] += 1

        for i in range(1, 10):
            countArray[i] += countArray[i - 1]

        j = s - 1
        while j >= 0:
            idx = (arr[j] // exp) % 10
            outputArray[countArray[idx] - 1] = arr[j]
            countArray[idx] -= 1
            self.intercambios += 1
            j -= 1

        for j in range(s):
            arr[j] = outputArray[j]

    # Ordenamiento HeapSort 8
    def heap_sort(self, a):
        self.reiniciar_contadores()
        n = len(a)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(a, n, i)
        for i in range(n - 1, 0, -1):
            a[0], a[i] = a[i], a[0]
            self.intercambios += 1
            self._heapify(a, i, 0)

    def _heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            self.comparaciones += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            self.comparaciones += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.intercambios += 1
            self._heapify(arr, n, largest)


if __name__ == "__main__":
    tamanios = [100]
    
    algoritmos = {
        "Insercion": BenchmarkOrdenamiento().insertion_sort,
        "Seleccion": BenchmarkOrdenamiento().selection_sort,
        "Burbuja": BenchmarkOrdenamiento().bubble_sort,
        "MergeSort": BenchmarkOrdenamiento().merge_sort,
        "QuickSort": BenchmarkOrdenamiento().quick_sort,
        "ShellSort": BenchmarkOrdenamiento().shell_sort,
        "RadixSort": BenchmarkOrdenamiento().radix_sort,
        "HeapSort": BenchmarkOrdenamiento().heap_sort,
    }

    resultados = []
    print("=== INICIANDO ORDENAMIENTOS EN PYTHON ===")

    for tam in tamanios:
        random.seed(42)
        base_aleatoria = [random.randint(0, 1000000) for _ in range(tam)]

        estados = {
            "Aleatorio": list(base_aleatoria),
            "Ordenado": sorted(list(base_aleatoria)),
            "Inverso": sorted(list(base_aleatoria), reverse=True)
        }

        for estado, arr_original in estados.items():
            for nombre_alg, func_alg in algoritmos.items():
                
                #Opcional
                if tam >= 100000 and nombre_alg in ["Burbuja", "Seleccion", "Insercion"]:
                    print(f"Omitiendo {nombre_alg} para tamaño {tam} (demasiado lento por complejidad O(n^2))")
                    continue

                arr_copia = list(arr_original)
                tester = BenchmarkOrdenamiento()
                
                #Tiempo de ejecucion
                inicio = time.perf_counter()
                
                if nombre_alg == "Insercion": tester.insertion_sort(arr_copia)
                elif nombre_alg == "Seleccion": tester.selection_sort(arr_copia)
                elif nombre_alg == "Burbuja": tester.bubble_sort(arr_copia)
                elif nombre_alg == "MergeSort": tester.merge_sort(arr_copia)
                elif nombre_alg == "QuickSort": tester.quick_sort(arr_copia)
                elif nombre_alg == "ShellSort": tester.shell_sort(arr_copia)
                elif nombre_alg == "RadixSort": tester.radix_sort(arr_copia)
                elif nombre_alg == "HeapSort": tester.heap_sort(arr_copia)
                
                fin = time.perf_counter()
                tiempo_ms = (fin - inicio) * 1000.0

                resultados.append({
                    "Lenguaje": "Python",
                    "Algoritmo": nombre_alg,
                    "Tamano": tam,
                    "Estado": estado,
                    "TiempoMs": round(tiempo_ms, 4),
                    "Comparaciones": tester.comparaciones,
                    "Intercambios": tester.intercambios
                })
                print(f"-> Tamaño: {tam} | Algoritmo: {nombre_alg} | Estado: {estado} | Tiempo: {tiempo_ms:.4f} ms")

    #Guardar los resultado de la ejecucion
    Resul = "Resultados.csv"
    with open(Resul, mode="w", newline="", encoding="utf-8") as archivo_csv:
        fieldnames = ["Lenguaje", "Algoritmo", "Tamano", "Estado", "TiempoMs", "Comparaciones", "Intercambios"]
        writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"\n¡Pruebas de Python finalizadas! Archivo '{Resul}' generado con éxito.")
