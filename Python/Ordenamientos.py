import random
import time
import sys

sys.setrecursionlimit(2000000)

class Metrics:
    def __init__(self):
        self.comp = 0
        self.inter = 0

def generar_arreglo(n):
    random.seed(42)
    return [random.randint(1, 1000000) for _ in range(n)]

#Ordenamiento 1 BubbleSort
def bubble_sort(arr):
    m = Metrics()
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            m.comp += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                m.inter += 1
                swapped = True
        if not swapped:
            break
    return m

#Ordenamiento 2 SelectionSort
def selection_sort(arr):
    m = Metrics()
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            m.comp += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[min_idx], arr[i] = arr[i], arr[min_idx]
            m.inter += 1
    return m

#Ordenamiento 3 InsertionSort
def insertion_sort(arr):
    m = Metrics()
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            m.comp += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                m.inter += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return m

#Ordenamiento 4 QuickSort
def quick_sort(arr):
    m = Metrics()
    def _quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)
    
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            m.comp += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                m.inter += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        m.inter += 1
        return i + 1

    if len(arr) > 1:
        _quick_sort(0, len(arr) - 1)
    return m

#Ordenamiento 5 MergeSort
def merge_sort(arr):
    m = Metrics()
    def _merge_sort(l, r):
        if l < r:
            mid = (l + r) // 2
            _merge_sort(l, mid)
            _merge_sort(mid + 1, r)
            _merge(l, mid, r)

    def _merge(l, mid, r):
        n1 = mid - l + 1
        n2 = r - mid
        L = arr[l:mid + 1]
        R = arr[mid + 1:r + 1]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            m.comp += 1
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            m.inter += 1
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            m.inter += 1
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            m.inter += 1

    if len(arr) > 1:
        _merge_sort(0, len(arr) - 1)
    return m

#Ordenamiento 6 HeapSort
def heap_sort(arr):
    m = Metrics()
    n = len(arr)

    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            m.comp += 1
            if arr[l] > arr[largest]:
                largest = l
        if r < n:
            m.comp += 1
            if arr[r] > arr[largest]:
                largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            m.inter += 1
            heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        m.inter += 1
        heapify(i, 0)
    return m

#Ordenamiento 7 ShellSort
def shell_sort(arr):
    m = Metrics()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap:
                m.comp += 1
                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    m.inter += 1
                    j -= gap
                else:
                    break
            arr[j] = temp
        gap //= 2
    return m

#Ordenamiento 8 BucketSort
def bucket_sort(arr):
    m = Metrics()
    if len(arr) <= 1:
        return m
    
    min_val = min(arr)
    max_val = max(arr)
    n = len(arr)
    
    buckets = [[] for _ in range(n)]
    
    for i in range(n):
        m.comp += 1
        if max_val == min_val:
            bi = 0
        else:
            bi = int((arr[i] - min_val) * (n - 1) / (max_val - min_val))
        buckets[bi].append(arr[i])

    for b in buckets:
        for i in range(1, len(b)):
            key = b[i]
            j = i - 1
            while j >= 0:
                m.comp += 1
                if b[j] > key:
                    b[j + 1] = b[j]
                    m.inter += 1
                    j -= 1
                else:
                    break
            b[j + 1] = key
            
    idx = 0
    for b in buckets:
        for val in b:
            arr[idx] = val
            m.inter += 1
            idx += 1
            
    return m

#Ordenamiento 9 RadixSort
def radix_sort(arr):
    m = Metrics()
    if len(arr) <= 1:
        return m
        
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        _counting_sort_radix(arr, exp, m)
        exp *= 10
    return m

def _counting_sort_radix(arr, exp, m):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        m.comp += 1
        index = (arr[i] // exp) % 10
        count[index] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        m.inter += 1
        i -= 1
        
    for i in range(n):
        arr[i] = output[i]
        m.inter += 1

def main():
    tamanos = [100, 1000, 10000, 100000]
    algoritmos = [
        ("Burbuja", bubble_sort),
        ("Seleccion", selection_sort),
        ("Insercion", insertion_sort),
        ("QuickSort", quick_sort),
        ("MergeSort", merge_sort),
        ("HeapSort", heap_sort),
        ("ShellSort", shell_sort),
        ("BucketSort", bucket_sort),
        ("RadixSort", radix_sort)
    ]

    archivo_txt = "ResultadosPython.txt"
    with open(archivo_txt, "w", encoding="utf-8") as f:
        f.write("Tamano\tAlgoritmo\tEstado\tTiempoMs\tComparaciones\tIntercambios\n")

        for n in tamanos:
            original = generar_arreglo(n)

            estados = [
                ("Aleatorio", original.copy()),
                ("Ordenado", sorted(original.copy())),
                ("Inverso", sorted(original.copy(), reverse=True))
            ]

            for estado, arr_base in estados:
                for nombre, func in algoritmos:
                    copia = arr_base.copy()
                    inicio = time.perf_counter()
                    metrics = func(copia)
                    fin = time.perf_counter()
                    tiempo_ms = (fin - inicio) * 1000.0

                    linea = f"{n}\t{nombre}\t{estado}\t{tiempo_ms:.3f}\t{metrics.comp}\t{metrics.inter}\n"
                    f.write(linea)
                    print(f"Tamaño: {n} | Algoritmo: {nombre} | Estado: {estado} | Tiempo: {tiempo_ms:.3f} ms")

    print("Ordenamientos de Python ejecutados correctamente")

if __name__ == "__main__":
    main()