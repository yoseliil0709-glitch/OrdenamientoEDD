const fs = require('fs');

function* seededRandom(seed) {
    let s = seed;
    while (true) {
        s = (s * 1103515245 + 12345) % 2147483648;
        yield s / 2147483648;
    }
}

class BenchmarkOrdenamiento {
    constructor() {
        this.comparaciones = 0;
        this.intercambios = 0;
    }

    reiniciarContadores() {
        this.comparaciones = 0;
        this.intercambios = 0;
    }

    //Ordenamiento Burbuja 1
    bubbleSort(a) {
        this.reiniciarContadores();
        let s = a.length;
        for (let i = 0; i < s; i++) {
            let isSwapped = false;
            for (let j = 0; j < s - i - 1; j++) {
                this.comparaciones++;
                if (a[j] > a[j + 1]) {
                    let temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                    this.intercambios++;
                    isSwapped = true;
                }
            }
            if (!isSwapped) break;
        }
    }

    //Ordenamiento HeapSort 2
    heapSort(arr) {
        this.reiniciarContadores();
        let n = arr.length;
        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            this._heapify(arr, n, i);
        }
        for (let i = n - 1; i > 0; i--) {
            let temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            this.intercambios++;
            this._heapify(arr, i, 0);
        }
    }

    _heapify(arr, n, i) {
        let largest = i;
        let left = 2 * i + 1;
        let right = 2 * i + 2;

        if (left < n) {
            this.comparaciones++;
            if (arr[left] > arr[largest]) largest = left;
        }
        if (right < n) {
            this.comparaciones++;
            if (arr[right] > arr[largest]) largest = right;
        }
        if (largest !== i) {
            let temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            this.intercambios++;
            this._heapify(arr, n, largest);
        }
    }

    //Ordenamiento Insercion 3
    insertionSort(a) {
        this.reiniciarContadores();
        for (let i = 1; i < a.length; i++) {
            let temp = a[i];
            let j = i - 1;
            this.comparaciones++;
            while (j >= 0 && temp < a[j]) {
                this.comparaciones++;
                a[j + 1] = a[j];
                this.intercambios++;
                j--;
            }
            a[j + 1] = temp;
        }
    }

    //Ordenamiento MergeSort 4
    mergeSort(a) {
        this.reiniciarContadores();
        this._mergeSortRec(a, 0, a.length - 1);
    }

    _mergeSortRec(a, l, r) {
        if (l < r) {
            let m = Math.floor((l + r) / 2);
            this._mergeSortRec(a, l, m);
            this._mergeSortRec(a, m + 1, r);
            this._merge(a, l, m, r);
        }
    }

    _merge(a, l, m, r) {
        let n1 = m - l + 1;
        let n2 = r - m;
        let L = new Array(n1);
        let R = new Array(n2);

        for (let i = 0; i < n1; i++) L[i] = a[l + i];
        for (let j = 0; j < n2; j++) R[j] = a[m + 1 + j];

        let i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            this.comparaciones++;
            if (L[i] <= R[j]) {
                a[k] = L[i];
                i++;
            } else {
                a[k] = R[j];
                j++;
            }
            this.intercambios++;
            k++;
        }
        while (i < n1) {
            a[k] = L[i];
            i++; k++;
            this.intercambios++;
        }
        while (j < n2) {
            a[k] = R[j];
            j++; k++;
            this.intercambios++;
        }
    }

    //Ordenamiento QuickSort 5
    quickSort(a) {
        this.reiniciarContadores();
        this._qckSortRec(a, 0, a.length - 1);
    }

    _qckSortRec(a, l, h) {
        if (l < h) {
            let pi = this._partition(a, l, h);
            this._qckSortRec(a, l, pi - 1);
            this._qckSortRec(a, pi + 1, h);
        }
    }

    _partition(a, l, h) {
        let pvt = a[h];
        let j = l - 1;
        for (let k = l; k < h; k++) {
            this.comparaciones++;
            if (a[k] < pvt) {
                j++;
                let temp = a[j];
                a[j] = a[k];
                a[k] = temp;
                this.intercambios++;
            }
        }
        let temp = a[j + 1];
        a[j + 1] = a[h];
        a[h] = temp;
        this.intercambios++;
        return j + 1;
    }

    //Ordenamiento Radix 6
    radixSort(arr) {
        this.reiniciarContadores();
        if (arr.length === 0) return;
        let max1 = Math.max(...arr);
        let exp = 1;
        while (Math.floor(max1 / exp) > 0) {
            this._countingSortRadix(arr, exp);
            exp *= 10;
        }
    }

    _countingSortRadix(arr, exp) {
        let s = arr.length;
        let outputArray = new Array(s).fill(0);
        let countArray = new Array(10).fill(0);

        for (let j = 0; j < s; j++) {
            let idx = Math.floor(arr[j] / exp) % 10;
            countArray[idx]++;
        }
        for (let i = 1; i < 10; i++) {
            countArray[i] += countArray[i - 1];
        }
        let j = s - 1;
        while (j >= 0) {
            let idx = Math.floor(arr[j] / exp) % 10;
            outputArray[countArray[idx] - 1] = arr[j];
            countArray[idx]--;
            this.intercambios++;
            j--;
        }
        for (let j = 0; j < s; j++) {
            arr[j] = outputArray[j];
        }
    }

    //Ordenamiento Seleccion 7
    selectionSort(a) {
        this.reiniciarContadores();
        for (let i = 0; i < a.length; i++) {
            let small = i;
            for (let j = i + 1; j < a.length; j++) {
                this.comparaciones++;
                if (a[small] > a[j]) {
                    small = j;
                }
            }
            if (small !== i) {
                let temp = a[i];
                a[i] = a[small];
                a[small] = temp;
                this.intercambios++;
            }
        }
    }

    //Ordenamiento ShellSort 8
    shellSort(imputArr) {
        this.reiniciarContadores();
        let size = imputArr.length;
        let gapSize = Math.floor(size / 2);

        while (gapSize > 0) {
            for (let j = gapSize; j < size; j++) {
                let val = imputArr[j];
                let k = j;

                while (k >= gapSize) {
                    this.comparaciones++;
                    if (imputArr[k - gapSize] > val) {
                        imputArr[k] = imputArr[k - gapSize];
                        this.intercambios++;
                        k = k - gapSize;
                    } else {
                        break;
                    }
                }
                imputArr[k] = val;
            }
            gapSize = Math.floor(gapSize / 2);
        }
    }
}

const tamanios = [100];
const resultados = [];

console.log("=== INICIANDO ORDENAMIENTOS EN JAVASCRIPT ===");

for (let tam of tamanios) {
    const rnd = seededRandom(42);
    const baseAleatoria = [];
    for (let i = 0; i < tam; i++) {
        baseAleatoria.push(Math.floor(rnd.next().value * 1000000));
    }

    const estados = {
        "Aleatorio": [...baseAleatoria],
        "Ordenado": [...baseAleatoria].sort((x, y) => x - y),
        "Inverso": [...baseAleatoria].sort((x, y) => x - y).reverse()
    };

    for (let [estado, arrOriginal] of Object.entries(estados)) {
        const algoritmos = {
            "Burbuja": (arr) => new BenchmarkOrdenamiento().bubbleSort(arr),
            "HeapSort": (arr) => new BenchmarkOrdenamiento().heapSort(arr),
            "Insercion": (arr) => new BenchmarkOrdenamiento().insertionSort(arr),
            "MergeSort": (arr) => new BenchmarkOrdenamiento().mergeSort(arr),
            "QuickSort": (arr) => new BenchmarkOrdenamiento().quickSort(arr),
            "RadixSort": (arr) => new BenchmarkOrdenamiento().radixSort(arr),
            "Seleccion": (arr) => new BenchmarkOrdenamiento().selectionSort(arr),
            "ShellSort": (arr) => new BenchmarkOrdenamiento().shellSort(arr)
        };

        for (let [nombreAlg, funcAlg] of Object.entries(algoritmos)) {
            
            if (tam >= 100000 && ["Burbuja", "Seleccion", "Insercion"].includes(nombreAlg)) {
                console.log(`Omitiendo ${nombreAlg} para tamaño ${tam} (complejidad O(n^2))`);
                continue;
            }

            let arrCopia = [...arrOriginal];
            let tester = new BenchmarkOrdenamiento();

            let inicio = process.hrtime.bigint();
            
            if (nombreAlg === "Burbuja") tester.bubbleSort(arrCopia);
            else if (nombreAlg === "HeapSort") tester.heapSort(arrCopia);
            else if (nombreAlg === "Insercion") tester.insertionSort(arrCopia);
            else if (nombreAlg === "MergeSort") tester.mergeSort(arrCopia);
            else if (nombreAlg === "QuickSort") tester.quickSort(arrCopia);
            else if (nombreAlg === "RadixSort") tester.radixSort(arrCopia);
            else if (nombreAlg === "Seleccion") tester.selectionSort(arrCopia);
            else if (nombreAlg === "ShellSort") tester.shellSort(arrCopia);

            let fin = process.hrtime.bigint();
            let tiempoMs = Number(fin - inicio) / 1_000_000;

            resultados.push({
                Lenguaje: "JavaScript",
                Algoritmo: nombreAlg,
                Tamano: tam,
                Estado: estado,
                TiempoMs: tiempoMs.toFixed(4),
                Comparaciones: tester.comparaciones,
                Intercambios: tester.intercambios
            });

            console.log(`-> Tamaño: ${tam} | Algoritmo: ${nombreAlg} | Estado: ${estado} | Tiempo: ${tiempoMs.toFixed(4)} ms`);
        }
    }
}

// Guardar en Resultado.csv
let csvContent = "Lenguaje,Algoritmo,Tamano,Estado,TiempoMs,Comparaciones,Intercambios\n";
resultados.forEach(row => {
    csvContent += `${row.Lenguaje},${row.Algoritmo},${row.Tamano},${row.Estado},${row.TiempoMs},${row.Comparaciones},${row.Intercambios}\n`;
});

fs.writeFileSync("Resultado.csv", csvContent, "utf8");
console.log("\n¡Pruebas de JavaScript finalizadas! Archivo 'Resultado.csv' generado con éxito.");