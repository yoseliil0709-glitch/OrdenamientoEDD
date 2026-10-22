using System;
using System.Diagnostics;
using System.IO;
using System.Linq;

class BenchmarkOrdenamientos
{
    public long comparaciones = 0;
    public long intercambios = 0;

    public void ReiniciarContadores()
    {
        comparaciones = 0;
        intercambios = 0;
    }

    //Ordenamiento Burbuja 1
    public void BubbleSort(int[] a)
    {
        ReiniciarContadores();
        int s = a.Length;
        for (int i = 0; i < s; i++)
        {
            bool isSwapped = false;
            for (int j = 0; j < s - i - 1; j++)
            {
                comparaciones++;
                if (a[j] > a[j + 1])
                {
                    int temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                    intercambios++;
                    isSwapped = true;
                }
            }
            if (!isSwapped) break;
        }
    }

    //Ordenamiento HeapSort 2
    public void HeapSort(int[] arr)
    {
        ReiniciarContadores();
        int n = arr.Length;
        for (int i = n / 2 - 1; i >= 0; i--)
            Heapify(arr, n, i);

        for (int i = n - 1; i > 0; i--)
        {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            intercambios++;
            Heapify(arr, i, 0);
        }
    }

    void Heapify(int[] arr, int n, int i)
    {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n)
        {
            comparaciones++;
            if (arr[left] > arr[largest]) largest = left;
        }
        if (right < n)
        {
            comparaciones++;
            if (arr[right] > arr[largest]) largest = right;
        }
        if (largest != i)
        {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            intercambios++;
            Heapify(arr, n, largest);
        }
    }

    //Ordenamiento Insercion 3
    public void InsertionSort(int[] a)
    {
        ReiniciarContadores();
        for (int i = 1; i < a.Length; i++)
        {
            int temp = a[i];
            int j = i - 1;
            comparaciones++;
            while (j >= 0 && temp < a[j])
            {
                comparaciones++;
                a[j + 1] = a[j];
                intercambios++;
                j = j - 1;
            }
            a[j + 1] = temp;
        }
    }

    //Ordenamiento MergeSort 4
    public void MergeSort(int[] a)
    {
        ReiniciarContadores();
        MergeSortRec(a, 0, a.Length - 1);
    }

    void MergeSortRec(int[] a, int l, int r)
    {
        if (l < r)
        {
            int m = (l + r) / 2;
            MergeSortRec(a, l, m);
            MergeSortRec(a, m + 1, r);
            Merge(a, l, m, r);
        }
    }

    void Merge(int[] a, int l, int m, int r)
    {
        int n1 = m - l + 1;
        int n2 = r - m;

        int[] L = new int[n1];
        int[] R = new int[n2];

        for (int i = 0; i < n1; i++) L[i] = a[l + i];
        for (int j = 0; j < n2; j++) R[j] = a[m + 1 + j];

        int i1 = 0, j1 = 0, k = l;

        while (i1 < n1 && j1 < n2)
        {
            comparaciones++;
            if (L[i1] <= R[j1])
            {
                a[k] = L[i1];
                i1++;
            }
            else
            {
                a[k] = R[j1];
                j1++;
            }
            intercambios++;
            k++;
        }

        while (i1 < n1)
        {
            a[k] = L[i1];
            i1++; k++;
            intercambios++;
        }

        while (j1 < n2)
        {
            a[k] = R[j1];
            j1++; k++;
            intercambios++;
        }
    }

    //Ordenamiento QuickSort 5
    public void QuickSort(int[] a)
    {
        ReiniciarContadores();
        QckSortRec(a, 0, a.Length - 1);
    }

    void QckSortRec(int[] a, int l, int h)
    {
        if (l < h)
        {
            int pi = Partition(a, l, h);
            QckSortRec(a, l, pi - 1);
            QckSortRec(a, pi + 1, h);
        }
    }

    int Partition(int[] a, int l, int h)
    {
        int pvt = a[h];
        int j = l - 1;
        for (int k = l; k < h; k++)
        {
            comparaciones++;
            if (a[k] < pvt)
            {
                j++;
                int temp = a[j];
                a[j] = a[k];
                a[k] = temp;
                intercambios++;
            }
        }
        int temp = a[j + 1];
        a[j + 1] = a[h];
        a[h] = temp;
        intercambios++;
        return j + 1;
    }

    //Ordenamiento Radix 6
    public void RadixSort(int[] arr)
    {
        ReiniciarContadores();
        if (arr.Length == 0) return;
        int max = arr.Max();
        for (int exp = 1; max / exp > 0; exp *= 10)
        {
            CountingSortRadix(arr, exp);
        }
    }

    void CountingSortRadix(int[] arr, int exp)
    {
        int s = arr.Length;
        int[] outputArray = new int[s];
        int[] countArray = new int[10];

        for (int j = 0; j < s; j++)
        {
            int idx = (arr[j] / exp) % 10;
            countArray[idx]++;
        }
        for (int i = 1; i < 10; i++)
        {
            countArray[i] += countArray[i - 1];
        }
        int j = s - 1;
        while (j >= 0)
        {
            int idx = (arr[j] / exp) % 10;
            outputArray[countArray[idx] - 1] = arr[j];
            countArray[idx]--;
            intercambios++;
            j--;
        }
        for (int k = 0; k < s; k++)
        {
            arr[k] = outputArray[k];
        }
    }

    //Ordenamiento Seleccion 7
    public void SelectionSort(int[] a)
    {
        ReiniciarContadores();
        for (int i = 0; i < a.Length; i++)
        {
            int small = i;
            for (int j = i + 1; j < a.Length; j++)
            {
                comparaciones++;
                if (a[small] > a[j])
                {
                    small = j;
                }
            }
            if (small != i)
            {
                int temp = a[i];
                a[i] = a[small];
                a[small] = temp;
                intercambios++;
            }
        }
    }

    //Ordenamiento ShellSort 8
    public void ShellSort(int[] imputArr)
    {
        ReiniciarContadores();
        int size = imputArr.Length;
        int gapSize = size / 2;

        while (gapSize > 0)
        {
            for (int j = gapSize; j < size; j++)
            {
                int val = imputArr[j];
                int k = j;

                while (k >= gapSize)
                {
                    comparaciones++;
                    if (imputArr[k - gapSize] > val)
                    {
                        imputArr[k] = imputArr[k - gapSize];
                        intercambios++;
                        k = k - gapSize;
                    }
                    else
                    {
                        break;
                    }
                }
                imputArr[k] = val;
            }
            gapSize = gapSize / 2;
        }
    }

    static void Main()
    {
        int[] tamanios = {100};
        string nombreArchivo = "Resultados.csv";

        using (StreamWriter sw = new StreamWriter(nombreArchivo))
        {
            sw.WriteLine("Lenguaje,Algoritmo,Tamano,Estado,TiempoMs,Comparaciones,Intercambios");
            Console.WriteLine("=== INICIANDO BENCHMARKING EN C# ===");

            foreach (int tam in tamanios)
            {
                Random rand = new Random(42); // Semilla fija 42
                int[] baseAleatoria = new int[tam];
                for (int i = 0; i < tam; i++)
                {
                    baseAleatoria[i] = rand.Next(0, 1000001);
                }

                int[] aleatorio = (int[])baseAleatoria.Clone();
                int[] ordenado = (int[])baseAleatoria.Clone();
                Array.Sort(ordenado);
                int[] inverso = (int[])ordenado.Clone();
                Array.Reverse(inverso);

                string[] algoritmos = { "BubbleSort", "HeapSort", "InsertionSort", "MergeSort", "QuickSort", "RadixSort", "SelectionSort", "ShellSort" };

                foreach (string nombreAlg in algoritmos)
                {
                    if (tam >= 100000 && (nombreAlg == "BubbleSort" || nombreAlg == "SelectionSort" || nombreAlg == "InsertionSort"))
                    {
                        Console.WriteLine($"Omitiendo {nombreAlg} para tamaño {tam} (complejidad O(n^2))");
                        continue;
                    }

                    EjecutarPrueba(sw, "Aleatorio", aleatorio, nombreAlg, tam);
                    EjecutarPrueba(sw, "Ordenado", ordenado, nombreAlg, tam);
                    EjecutarPrueba(sw, "Inverso", inverso, nombreAlg, tam);
                }
            }
        }
        Console.WriteLine($"\n¡Pruebas de C# finalizadas! Archivo '{nombreArchivo}' generado con éxito.");
    }

    static void EjecutarPrueba(StreamWriter sw, string estado, int[] original, string nombreAlg, int tam)
    {
        int[] arrCopia = (int[])original.Clone();
        BenchmarkOrdenamientos sorter = new BenchmarkOrdenamientos();

        Stopwatch stopwatch = Stopwatch.StartNew();

        switch (nombreAlg)
        {
            case "BubbleSort": sorter.BubbleSort(arrCopia); break;
            case "HeapSort": sorter.HeapSort(arrCopia); break;
            case "InsertionSort": sorter.InsertionSort(arrCopia); break;
            case "MergeSort": sorter.MergeSort(arrCopia); break;
            case "QuickSort": sorter.QuickSort(arrCopia); break;
            case "RadixSort": sorter.RadixSort(arrCopia); break;
            case "SelectionSort": sorter.SelectionSort(arrCopia); break;
            case "ShellSort": sorter.ShellSort(arrCopia); break;
        }

        stopwatch.Stop();
        double tiempoMs = stopwatch.Elapsed.TotalMilliseconds;

        sw.WriteLine($"C#,{nombreAlg},{tam},{estado},{tiempoMs:F4},{sorter.comparaciones},{sorter.intercambios}");
        Console.WriteLine($"-> Tamaño: {tam} | Algoritmo: {nombreAlg} | Estado: {estado} | Tiempo: {tiempoMs:F4} ms");
    }
}