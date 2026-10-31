using System;
using System.Collections.Generic;
using System.IO;
using System.Diagnostics;
using System.Linq;

class Program {
    public class Metrics {
        public long comp = 0;
        public long inter = 0;
    }
    public static List<int> generar_arreglo(int n) {
        Random rng = new Random(42);
        List<int> arr = new List<int>(n);
        for (int i = 0; i < n; ++i) {
            arr.Add(rng.Next(1, 1000001));
        }
        return arr;
    }

    //Ordenamiento 1 BubbleSort
    public static Metrics bubble_sort(List<int> arr) {
        Metrics m = new Metrics();
        int n = arr.Count;
        for (int i = 0; i < n - 1; ++i) {
            bool swapped = false;
            for (int j = 0; j < n - i - 1; ++j) {
                m.comp++;
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    m.inter++;
                    swapped = true;
                }
            }
            if (!swapped) {
                break;
            }
        }
        return m;
    }

    //Ordenamiento 2 SelectionSort
    public static Metrics selection_sort(List<int> arr) {
        Metrics m = new Metrics();
        int n = arr.Count;
        for (int i = 0; i < n - 1; ++i) {
            int min_idx = i;
            for (int j = i + 1; j < n; ++j) {
                m.comp++;
                if (arr[j] < arr[min_idx]) {
                    min_idx = j;
                }
            }
            if (min_idx != i) {
                int temp = arr[min_idx];
                arr[min_idx] = arr[i];
                arr[i] = temp;
                m.inter++;
            }
        }
        return m;
    }

    //Ordenamiento 3 InsertionSort
    public static Metrics insertion_sort(List<int> arr) {
        Metrics m = new Metrics();
        int n = arr.Count;
        for (int i = 1; i < n; ++i) {
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
    public static Metrics quick_sort(List<int> arr) {
        Metrics m = new Metrics();
        
        Action<int, int> _quick_sort = null;
        _quick_sort = (low, high) => {
            if (low < high) {
                Func<int, int, int> partition = (l, h) => {
                    int pivot = arr[h];
                    int i = l - 1;
                    for (int j = l; j < h; ++j) {
                        m.comp++;
                        if (arr[j] < pivot) {
                            i++;
                            int temp = arr[i];
                            arr[i] = arr[j];
                            arr[j] = temp;
                            m.inter++;
                        }
                    }
                    int temp2 = arr[i + 1];
                    arr[i + 1] = arr[h];
                    arr[h] = temp2;
                    m.inter++;
                    return i + 1;
                };

                int pi = partition(low, high);
                _quick_sort(low, pi - 1);
                _quick_sort(pi + 1, high);
            }
        };

        if (arr.Count > 1) {
            _quick_sort(0, arr.Count - 1);
        }
        return m;
    }

    //Ordenamiento 5 MergeSort
    public static Metrics merge_sort(List<int> arr) {
        Metrics m = new Metrics();

        Action<int, int, int> _merge = (l, mid, r) => {
            int n1 = mid - l + 1;
            int n2 = r - mid;
            List<int> L = arr.GetRange(l, n1);
            List<int> R = arr.GetRange(mid + 1, n2);
            int i = 0, j = 0;
            int k = l;
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
        };

        Action<int, int> _merge_sort = null;
        _merge_sort = (l, r) => {
            if (l < r) {
                int mid = l + (r - l) / 2;
                _merge_sort(l, mid);
                _merge_sort(mid + 1, r);
                _merge(l, mid, r);
            }
        };

        if (arr.Count > 1) {
            _merge_sort(0, arr.Count - 1);
        }
        return m;
    }

    //Ordenamiento 6 HeapSort
    public static Metrics heap_sort(List<int> arr) {
        Metrics m = new Metrics();
        int n = arr.Count;

        Action<int, int> heapify = null;
        heapify = (n_sz, i) => {
            int largest = i;
            int l = 2 * i + 1;
            int r = 2 * i + 2;
            if (l < n_sz) {
                m.comp++;
                if (arr[l] > arr[largest]) {
                    largest = l;
                }
            }
            if (r < n_sz) {
                m.comp++;
                if (arr[r] > arr[largest]) {
                    largest = r;
                }
            }
            if (largest != i) {
                int temp = arr[i];
                arr[i] = arr[largest];
                arr[largest] = temp;
                m.inter++;
                heapify(n_sz, largest);
            }
        };

        for (int i = n / 2 - 1; i >= 0; --i) {
            heapify(n, i);
        }
        for (int i = n - 1; i > 0; --i) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            m.inter++;
            heapify(i, 0);
        }
        return m;
    }

    //Ordenamiento 7 ShellSort
    public static Metrics shell_sort(List<int> arr) {
        Metrics m = new Metrics();
        int n = arr.Count;
        int gap = n / 2;
        while (gap > 0) {
            for (int i = gap; i < n; ++i) {
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
    public static Metrics bucket_sort(List<int> arr) {
        Metrics m = new Metrics();
        if (arr.Count <= 1) {
            return m;
        }
        
        int min_val = arr.Min();
        int max_val = arr.Max();
        int n = arr.Count;
        
        List<List<int>> buckets = new List<List<int>>(n);
        for (int i = 0; i < n; i++) {
            buckets.Add(new List<int>());
        }
        
        for (int i = 0; i < n; ++i) {
            m.comp++;
            int bi = 0;
            if (max_val == min_val) {
                bi = 0;
            } else {
                bi = (int)((long)(arr[i] - min_val) * (n - 1) / (max_val - min_val));
            }
            if (bi >= n) bi = n - 1;
            buckets[bi].Add(arr[i]);
        }

        foreach (var b in buckets) {
            for (int i = 1; i < b.Count; ++i) {
                int key = b[i];
                int j = i - 1;
                while (j >= 0) {
                    m.comp++;
                    if (b[j] > key) {
                        b[j + 1] = b[j];
                        m.inter++;
                        j--;
                    } else {
                        break;
                    }
                }
                b[j + 1] = key;
            }
        }
                
        int idx = 0;
        foreach (var b in buckets) {
            foreach (int val in b) {
                arr[idx] = val;
                m.inter++;
                idx++;
            }
        }
                
        return m;
    }

    public static void _counting_sort_radix(List<int> arr, int exp, Metrics m) {
        int n = arr.Count;
        List<int> output = new List<int>(new int[n]);
        List<int> count = new List<int>(new int[10]);
        
        for (int i = 0; i < n; ++i) {
            m.comp++;
            int index = (arr[i] / exp) % 10;
            count[index]++;
        }
            
        for (int i = 1; i < 10; ++i) {
            count[i] += count[i - 1];
        }
            
        int i_idx = n - 1;
        while (i_idx >= 0) {
            int index = (arr[i_idx] / exp) % 10;
            output[count[index] - 1] = arr[i_idx];
            count[index]--;
            m.inter++;
            i_idx--;
        }
            
        for (int k = 0; k < n; ++k) {
            arr[k] = output[k];
            m.inter++;
        }
    }

    //Ordenamiento 9 RadixSort
    public static Metrics radix_sort(List<int> arr) {
        Metrics m = new Metrics();
        if (arr.Count <= 1) {
            return m;
        }
            
        int max_val = arr.Max();
        int exp = 1;
        while (max_val / exp > 0) {
            _counting_sort_radix(arr, exp, m);
            exp *= 10;
        }
        return m;
    }

    public static void Main(string[] args) {
        List<int> tamanos = new List<int> {1000000};
        List<Tuple<string, Func<List<int>, Metrics>>> algoritmos = new List<Tuple<string, Func<List<int>, Metrics>>> {
            Tuple.Create("Burbuja", (Func<List<int>, Metrics>)bubble_sort),
            Tuple.Create("Seleccion", selection_sort),
            Tuple.Create("Insercion", insertion_sort),
            Tuple.Create("QuickSort", quick_sort),
            Tuple.Create("MergeSort", merge_sort),
            Tuple.Create("HeapSort", heap_sort),
            Tuple.Create("ShellSort", shell_sort),
            Tuple.Create("BucketSort", bucket_sort),
            Tuple.Create("RadixSort", radix_sort)
        };

        string archivo_txt = "ResultadoMillonC#.txt";
        using (StreamWriter f = new StreamWriter(archivo_txt, false, System.Text.Encoding.UTF8)) {
            f.WriteLine("Tamano\tAlgoritmo\tEstado\tTiempoMs\tComparaciones\tIntercambios");

            foreach (int n in tamanos) {
                List<int> original = generar_arreglo(n);

                List<int> ord = new List<int>(original);
                ord.Sort();
                List<int> rev = new List<int>(ord);
                rev.Reverse();

                List<Tuple<string, List<int>>> estados = new List<Tuple<string, List<int>>> {
                    Tuple.Create("Aleatorio", original),
                    Tuple.Create("Ordenado", ord),
                    Tuple.Create("Inverso", rev)
                };

                foreach (var estado_pair in estados) {
                    string estado = estado_pair.Item1;
                    List<int> arr_base = estado_pair.Item2;

                    foreach (var alg_pair in algoritmos) {
                        string nombre = alg_pair.Item1;
                        var func = alg_pair.Item2;

                        List<int> copia = new List<int>(arr_base);
                        Stopwatch stopwatch = Stopwatch.StartNew();
                        Metrics metrics = func(copia);
                        stopwatch.Stop();
                        double tiempo_ms = stopwatch.Elapsed.TotalMilliseconds;

                        f.WriteLine($"{n}\t{nombre}\t{estado}\t{tiempo_ms}\t{metrics.comp}\t{metrics.inter}");
                        Console.WriteLine($"Tamaño: {n} | Algoritmo: {nombre} | Estado: {estado} | Tiempo: {tiempo_ms} ms");
                    }
                }
            }
        }

        Console.WriteLine("Ordenamientos ejecutados correctamente");
    }
}