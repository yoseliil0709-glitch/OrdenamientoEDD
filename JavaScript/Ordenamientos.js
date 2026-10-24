class Metrics {
    constructor() {
        this.comp = 0;
        this.inter = 0;
    }
}

function generarArreglo(n) {
    let seed = 42;
    function random() {
        seed = (seed * 16807) % 2147483647;
        return (seed - 1) / 2147483646;
    }
    const arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(Math.floor(random() * 1000000) + 1);
    }
    return arr;
}

//Ordenamiento 1 BubbleSort
function bubbleSort(arr) {
    const m = new Metrics();
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            m.comp++;
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                m.inter++;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return m;
}

//Ordenamiento 2 SelectionSort
function selectionSort(arr) {
    const m = new Metrics();
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        let minIdx = i;
        for (let j = i + 1; j < n; j++) {
            m.comp++;
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        if (minIdx !== i) {
            [arr[minIdx], arr[i]] = [arr[i], arr[minIdx]];
            m.inter++;
        }
    }
    return m;
}

//Ordenamiento 3 InsertionSort
function insertionSort(arr) {
    const m = new Metrics();
    const n = arr.length;
    for (let i = 1; i < n; i++) {
        const key = arr[i];
        let j = i - 1;
        while (j >= 0) {
            m.comp++;
            if (arr[j] > key) {
                arr[j + 1] = arr[j];
                m.inter++;
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = key;
    }
    return m;
}

//Ordenamiento 4 QuickSort
function quickSort(arr) {
    const m = new Metrics();

    function partition(low, high) {
        const pivot = arr[high];
        let i = low - 1;
        for (let j = low; j < high; j++) {
            m.comp++;
            if (arr[j] < pivot) {
                i++;
                [arr[i], arr[j]] = [arr[j], arr[i]];
                m.inter++;
            }
        }
        [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
        m.inter++;
        return i + 1;
    }

    function _quickSort(low, high) {
        if (low < high) {
            const pi = partition(low, high);
            _quickSort(low, pi - 1);
            _quickSort(pi + 1, high);
        }
    }

    if (arr.length > 1) {
        _quickSort(0, arr.length - 1);
    }
    return m;
}

//Ordenamiento 5 MergeSort
function mergeSort(arr) {
    const m = new Metrics();

    function _mergeSort(l, r) {
        if (l < r) {
            const mid = Math.floor((l + r) / 2);
            _mergeSort(l, mid);
            _mergeSort(mid + 1, r);
            _merge(l, mid, r);
        }
    }

    function _merge(l, mid, r) {
        const n1 = mid - l + 1;
        const n2 = r - mid;
        const L = arr.slice(l, mid + 1);
        const R = arr.slice(mid + 1, r + 1);
        let i = 0;
        let j = 0;
        let k = l;
        while (i < n1 && j < n2) {
            m.comp++;
            if (L[i] <= R[j]) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            m.inter++;
            k++;
        }
        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
            m.inter++;
        }
        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
            m.inter++;
        }
    }

    if (arr.length > 1) {
        _mergeSort(0, arr.length - 1);
    }
    return m;
}

//Ordenamiento 6 HeapSort
function heapSort(arr) {
    const m = new Metrics();
    const n = arr.length;

    function heapify(n, i) {
        let largest = i;
        const l = 2 * i + 1;
        const r = 2 * i + 2;
        if (l < n) {
            m.comp++;
            if (arr[l] > arr[largest]) {
                largest = l;
            }
        }
        if (r < n) {
            m.comp++;
            if (arr[r] > arr[largest]) {
                largest = r;
            }
        }
        if (largest !== i) {
            [arr[i], arr[largest]] = [arr[largest], arr[i]];
            m.inter++;
            heapify(n, largest);
        }
    }

    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapify(n, i);
    }
    for (let i = n - 1; i > 0; i--) {
        [arr[0], arr[i]] = [arr[i], arr[0]];
        m.inter++;
        heapify(i, 0);
    }
    return m;
}

//Ordenamiento 7 ShellSort
function shellSort(arr) {
    const m = new Metrics();
    const n = arr.length;
    let gap = Math.floor(n / 2);
    while (gap > 0) {
        for (let i = gap; i < n; i++) {
            const temp = arr[i];
            let j = i;
            while (j >= gap) {
                m.comp++;
                if (arr[j - gap] > temp) {
                    arr[j] = arr[j - gap];
                    m.inter++;
                    j -= gap;
                } else {
                    break;
                }
            }
            arr[j] = temp;
        }
        gap = Math.floor(gap / 2);
    }
    return m;
}

//Ordenamiento 8 BucketSort
function bucketSort(arr) {
    const m = new Metrics();
    if (arr.length <= 1) return m;

    const minVal = Math.min(...arr);
    const maxVal = Math.max(...arr);
    const n = arr.length;

    const buckets = Array.from({ length: n }, () => []);

    for (let i = 0; i < n; i++) {
        m.comp++;
        let bi;
        if (maxVal === minVal) {
            bi = 0;
        } else {
            bi = Math.floor((arr[i] - minVal) * (n - 1) / (maxVal - minVal));
        }
        buckets[bi].push(arr[i]);
    }

    for (let b = 0; b < buckets.length; b++) {
        for (let i = 1; i < buckets[b].length; i++) {
            const key = buckets[b][i];
            let j = i - 1;
            while (j >= 0) {
                m.comp++;
                if (buckets[b][j] > key) {
                    buckets[b][j + 1] = buckets[b][j];
                    m.inter++;
                    j--;
                } else {
                    break;
                }
            }
            buckets[b][j + 1] = key;
        }
    }

    let idx = 0;
    for (let b = 0; b < buckets.length; b++) {
        for (const val of buckets[b]) {
            arr[idx] = val;
            m.inter++;
            idx++;
        }
    }
    return m;
}

//Ordenamiento 9 RadixSort
function radixSort(arr) {
    const m = new Metrics();
    if (arr.length <= 1) return m;

    const maxVal = Math.max(...arr);
    let exp = 1;
    while (Math.floor(maxVal / exp) > 0) {
        _countingSortRadix(arr, exp, m);
        exp *= 10;
    }
    return m;
}

function _countingSortRadix(arr, exp, m) {
    const n = arr.length;
    const output = new Array(n).fill(0);
    const count = new Array(10).fill(0);

    for (let i = 0; i < n; i++) {
        m.comp++;
        const index = Math.floor((arr[i] / exp) % 10);
        count[index]++;
    }

    for (let i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    let i = n - 1;
    while (i >= 0) {
        const index = Math.floor((arr[i] / exp) % 10);
        output[count[index] - 1] = arr[i];
        count[index]--;
        m.inter++;
        i--;
    }

    for (let i = 0; i < n; i++) {
        arr[i] = output[i];
        m.inter++;
    }
}

function main() {
    const tamanos = [100, 1000, 10000, 100000];
    const algoritmos = [
        ["Burbuja", bubbleSort],
        ["Seleccion", selectionSort],
        ["Insercion", insertionSort],
        ["QuickSort", quickSort],
        ["MergeSort", mergeSort],
        ["HeapSort", heapSort],
        ["ShellSort", shellSort],
        ["BucketSort", bucketSort],
        ["RadixSort", radixSort]
    ];
    
    const fs = require("fs");
    const archivoTxt = "ResultadosJavaScript.txt";
    let contenido = "Tamano\tAlgoritmo\tEstado\tTiempoMs\tComparaciones\tIntercambios\n";

    for (const n of tamanos) {
        const original = generarArreglo(n);

        const estados = [
            ["Aleatorio", original.slice()],
            ["Ordenado", original.slice().sort((a, b) => a - b)],
            ["Inverso", original.slice().sort((a, b) => a - b).reverse()]
        ];

        for (const [estado, arrBase] of estados) {
            for (const [nombre, func] of algoritmos) {
                const copia = arrBase.slice();
                const inicio = performance.now();
                const metrics = func(copia);
                const fin = performance.now();
                const tiempoMs = fin - inicio;

                contenido += `${n}\t${nombre}\t${estado}\t${tiempoMs.toFixed(3)}\t${metrics.comp}\t${metrics.inter}\n`;
                console.log(`Tamaño: ${n} | Algoritmo: ${nombre} | Estado: ${estado} | Tiempo: ${tiempoMs.toFixed(3)} ms`);
            }
        }
    }

    fs.writeFileSync(archivoTxt, contenido, "utf-8");
    console.log("Ordenamientos de JavaScript ejecutados correctamente");
}

main();