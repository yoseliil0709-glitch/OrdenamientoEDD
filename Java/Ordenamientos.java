import java.io.*;
import java.util.*;

public class Ordenamientos {

    static class Metrics {
        long comp = 0;
        long inter = 0;
    }

    interface SortFunction {
        Metrics sort(int[] arr);
    }

    static Random rng = new Random(42);

    static int[] generarArreglo(int n) {
        rng.setSeed(42);
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = rng.nextInt(1000000) + 1;
        }
        return arr;
    }

    //Ordenamiento 1 BubbleSort
    static Metrics bubbleSort(int[] arr) {
        Metrics m = new Metrics();
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                m.comp++;
                if (arr[j] > arr[j + 1]) {
                    int tmp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = tmp;
                    m.inter++;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
        return m;
    }

    //Ordenamiento 2 SelectionSort
    static Metrics selectionSort(int[] arr) {
        Metrics m = new Metrics();
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                m.comp++;
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            if (minIdx != i) {
                int tmp = arr[minIdx]; arr[minIdx] = arr[i]; arr[i] = tmp;
                m.inter++;
            }
        }
        return m;
    }

    //Ordenamiento 3 InsertionSort
    static Metrics insertionSort(int[] arr) {
        Metrics m = new Metrics();
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
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
    static Metrics quickSort(int[] arr) {
        Metrics m = new Metrics();
        _quickSort(arr, 0, arr.length - 1, m);
        return m;
    }

    static void _quickSort(int[] arr, int low, int high, Metrics m) {
        if (low < high) {
            int pi = partition(arr, low, high, m);
            _quickSort(arr, low, pi - 1, m);
            _quickSort(arr, pi + 1, high, m);
        }
    }

    static int partition(int[] arr, int low, int high, Metrics m) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            m.comp++;
            if (arr[j] < pivot) {
                i++;
                int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
                m.inter++;
            }
        }
        int tmp = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = tmp;
        m.inter++;
        return i + 1;
    }

    //Ordenamiento 5 MergeSort
    static Metrics mergeSort(int[] arr) {
        Metrics m = new Metrics();
        _mergeSort(arr, 0, arr.length - 1, m);
        return m;
    }

    static void _mergeSort(int[] arr, int l, int r, Metrics m) {
        if (l < r) {
            int mid = (l + r) / 2;
            _mergeSort(arr, l, mid, m);
            _mergeSort(arr, mid + 1, r, m);
            _merge(arr, l, mid, r, m);
        }
    }

    static void _merge(int[] arr, int l, int mid, int r, Metrics m) {
        int n1 = mid - l + 1;
        int n2 = r - mid;
        int[] L = Arrays.copyOfRange(arr, l, mid + 1);
        int[] R = Arrays.copyOfRange(arr, mid + 1, r + 1);
        int i = 0, j = 0, k = l;
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

    //Ordenamiento 6 HeapSort
    static Metrics heapSort(int[] arr) {
        Metrics m = new Metrics();
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i, m);
        }
        for (int i = n - 1; i > 0; i--) {
            int tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;
            m.inter++;
            heapify(arr, i, 0, m);
        }
        return m;
    }

    static void heapify(int[] arr, int n, int i, Metrics m) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        if (l < n) {
            m.comp++;
            if (arr[l] > arr[largest]) largest = l;
        }
        if (r < n) {
            m.comp++;
            if (arr[r] > arr[largest]) largest = r;
        }
        if (largest != i) {
            int tmp = arr[i]; arr[i] = arr[largest]; arr[largest] = tmp;
            m.inter++;
            heapify(arr, n, largest, m);
        }
    }

    //Ordenamiento 7 ShellSort
    static Metrics shellSort(int[] arr) {
        Metrics m = new Metrics();
        int n = arr.length;
        int gap = n / 2;
        while (gap > 0) {
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j = i;
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
            gap /= 2;
        }
        return m;
    }

    //Ordenamiento 8 BucketSort
    static Metrics bucketSort(int[] arr) {
        Metrics m = new Metrics();
        if (arr.length <= 1) return m;

        int minVal = Arrays.stream(arr).min().getAsInt();
        int maxVal = Arrays.stream(arr).max().getAsInt();
        int n = arr.length;

        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i < n; i++) buckets.add(new ArrayList<>());

        for (int i = 0; i < n; i++) {
            m.comp++;
            int bi;
            if (maxVal == minVal) {
                bi = 0;
            } else {
                bi = (int) ((long)(arr[i] - minVal) * (n - 1) / (maxVal - minVal));
            }
            buckets.get(bi).add(arr[i]);
        }

        for (List<Integer> b : buckets) {
            for (int i = 1; i < b.size(); i++) {
                int key = b.get(i);
                int j = i - 1;
                while (j >= 0) {
                    m.comp++;
                    if (b.get(j) > key) {
                        b.set(j + 1, b.get(j));
                        m.inter++;
                        j--;
                    } else {
                        break;
                    }
                }
                b.set(j + 1, key);
            }
        }

        int idx = 0;
        for (List<Integer> b : buckets) {
            for (int val : b) {
                arr[idx] = val;
                m.inter++;
                idx++;
            }
        }
        return m;
    }

    //Ordenamiento 9 RadixSort
    static Metrics radixSort(int[] arr) {
        Metrics m = new Metrics();
        if (arr.length <= 1) return m;

        int maxVal = Arrays.stream(arr).max().getAsInt();
        int exp = 1;
        while (maxVal / exp > 0) {
            countingSortRadix(arr, exp, m);
            exp *= 10;
        }
        return m;
    }

    static void countingSortRadix(int[] arr, int exp, Metrics m) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];

        for (int i = 0; i < n; i++) {
            m.comp++;
            int index = (arr[i] / exp) % 10;
            count[index]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        int i = n - 1;
        while (i >= 0) {
            int index = (arr[i] / exp) % 10;
            output[count[index] - 1] = arr[i];
            count[index]--;
            m.inter++;
            i--;
        }

        for (i = 0; i < n; i++) {
            arr[i] = output[i];
            m.inter++;
        }
    }

    public static void main(String[] args) throws IOException {
        int[] tamanos = {100, 1000, 10000, 100000};

        String[] nombres = {"Burbuja", "Seleccion", "Insercion", "QuickSort",
                            "MergeSort", "HeapSort", "ShellSort", "BucketSort", "RadixSort"};
        SortFunction[] funciones = {
            Ordenamientos::bubbleSort,
            Ordenamientos::selectionSort,
            Ordenamientos::insertionSort,
            Ordenamientos::quickSort,
            Ordenamientos::mergeSort,
            Ordenamientos::heapSort,
            Ordenamientos::shellSort,
            Ordenamientos::bucketSort,
            Ordenamientos::radixSort
        };

        String archivoTxt = "ResultadosJava.txt";
        try (PrintWriter f = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(archivoTxt), "UTF-8"))) {

            f.println("Tamano\tAlgoritmo\tEstado\tTiempoMs\tComparaciones\tIntercambios");

            for (int n : tamanos) {
                int[] original = generarArreglo(n);

                int[] aleatorio = original.clone();

                int[] ordenado = original.clone();
                Arrays.sort(ordenado);

                int[] inverso = ordenado.clone();
                for (int a = 0, b = inverso.length - 1; a < b; a++, b--) {
                    int tmp = inverso[a]; inverso[a] = inverso[b]; inverso[b] = tmp;
                }

                String[] estados = {"Aleatorio", "Ordenado", "Inverso"};
                int[][] arraysBase = {aleatorio, ordenado, inverso};

                for (int e = 0; e < estados.length; e++) {
                    String estado = estados[e];
                    int[] arrBase = arraysBase[e];

                    for (int algo = 0; algo < funciones.length; algo++) {
                        String nombre = nombres[algo];
                        SortFunction func = funciones[algo];

                        int[] copia = arrBase.clone();
                        long inicio = System.nanoTime();
                        Metrics metrics = func.sort(copia);
                        long fin = System.nanoTime();
                        double tiempoMs = (fin - inicio) / 1_000_000.0;

                        String linea = String.format("%d\t%s\t%s\t%.3f\t%d\t%d",
                                n, nombre, estado, tiempoMs, metrics.comp, metrics.inter);
                        f.println(linea);
                        System.out.printf("Tamaño: %d | Algoritmo: %s | Estado: %s | Tiempo: %.3f ms%n",
                                n, nombre, estado, tiempoMs);
                    }
                }
            }
        }
        System.out.println("Ordenamientos de Java ejecutados correctamente");
    }
}