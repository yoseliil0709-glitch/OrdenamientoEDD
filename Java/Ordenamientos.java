import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Random;

public class Ordenamientos {
    long comparaciones = 0;
    long intercambios = 0;

    void reiniciarContadores() {
        comparaciones = 0;
        intercambios = 0;
    }

    //Ordenamiento Burbuja 1
    public void bubbleSort(int[] a) {
        reiniciarContadores();
        int s = a.length;
        for (int i = 0; i < s; i++) {
            boolean isSwapped = false;
            for (int j = 0; j < s - i - 1; j++) {
                comparaciones++;
                if (a[j] > a[j + 1]) {
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
    public void heapSort(int[] arr) {
        reiniciarContadores();
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            intercambios++;
            heapify(arr, i, 0);
        }
    }

    void heapify(int[] arr, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n) {
            comparaciones++;
            if (arr[left] > arr[largest]) largest = left;
        }
        if (right < n) {
            comparaciones++;
            if (arr[right] > arr[largest]) largest = right;
        }
        if (largest != i) {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;
            intercambios++;
            heapify(arr, n, largest);
        }
    }

    //Ordenamiento Insercion 3
    public void insertionSort(int[] a) {
        reiniciarContadores();
        for (int i = 1; i < a.length; i++) {
            int temp = a[i];
            int j = i - 1;
            comparaciones++;
            while (j >= 0 && temp < a[j]) {
                comparaciones++;
                a[j + 1] = a[j];
                intercambios++;
                j--;
            }
            a[j + 1] = temp;
        }
    }

    //Ordenamiento MergeSort 4
    public void mergeSort(int[] a) {
        reiniciarContadores();
        mergeSortRec(a, 0, a.length - 1);
    }

    void mergeSortRec(int[] a, int l, int r) {
        if (l < r) {
            int m = (l + r) / 2;
            mergeSortRec(a, l, m);
            mergeSortRec(a, m + 1, r);
            merge(a, l, m, r);
        }
    }

    void merge(int[] a, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        int[] L = new int[n1];
        int[] R = new int[n2];

        for (int i = 0; i < n1; i++) L[i] = a[l + i];
        for (int j = 0; j < n2; j++) R[j] = a[m + 1 + j];

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            comparaciones++;
            if (L[i] <= R[j]) {
                a[k] = L[i];
                i++;
            } else {
                a[k] = R[j];
                j++;
            }
            intercambios++;
            k++;
        }
        while (i < n1) {
            a[k] = L[i];
            i++; k++;
            intercambios++;
        }
        while (j < n2) {
            a[k] = R[j];
            j++; k++;
            intercambios++;
        }
    }

    //Ordenamiento QuickSort 5
    public void quickSort(int[] a) {
        reiniciarContadores();
        qckSortRec(a, 0, a.length - 1);
    }

    void qckSortRec(int[] a, int l, int h) {
        if (l < h) {
            int pi = partition(a, l, h);
            qckSortRec(a, l, pi - 1);
            qckSortRec(a, pi + 1, h);
        }
    }

    int partition(int[] a, int l, int h) {
        int pvt = a[h];
        int j = l - 1;
        for (int k = l; k < h; k++) {
            comparaciones++;
            if (a[k] < pvt) {
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
    public void radixSort(int[] arr) {
        reiniciarContadores();
        if (arr.length == 0) return;
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) max = arr[i];
        }
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortRadix(arr, exp);
        }
    }

    void countingSortRadix(int[] arr, int exp) {
        int s = arr.length;
        int[] outputArray = new int[s];
        int[] countArray = new int[10];

        for (int j = 0; j < s; j++) {
            int idx = (arr[j] / exp) % 10;
            countArray[idx]++;
        }
        for (int i = 1; i < 10; i++) {
            countArray[i] += countArray[i - 1];
        }
        int j = s - 1;
        while (j >= 0) {
            int idx = (arr[j] / exp) % 10;
            outputArray[countArray[idx] - 1] = arr[j];
            countArray[idx]--;
            intercambios++;
            j--;
        }
        for (int k = 0; k < s; k++) {
            arr[k] = outputArray[k];
        }
    }

    //Ordenamiento por Seleccion 7
    public void selectionSort(int[] a) {
        reiniciarContadores();
        for (int i = 0; i < a.length; i++) {
            int small = i;
            for (int j = i + 1; j < a.length; j++) {
                comparaciones++;
                if (a[small] > a[j]) {
                    small = j;
                }
            }
            if (small != i) {
                int temp = a[i];
                a[i] = a[small];
                a[small] = temp;
                intercambios++;
            }
        }
    }

    //Ordenamiento ShellSort 8
    public void shellSort(int[] imputArr) {
        reiniciarContadores();
        int size = imputArr.length;
        int gapSize = size / 2;

        while (gapSize > 0) {
            for (int j = gapSize; j < size; j++) {
                int val = imputArr[j];
                int k = j;

                while (k >= gapSize) {
                    comparaciones++;
                    if (imputArr[k - gapSize] > val) {
                        imputArr[k] = imputArr[k - gapSize];
                        intercambios++;
                        k = k - gapSize;
                    } else {
                        break;
                    }
                }
                imputArr[k] = val;
            }
            gapSize = gapSize / 2;
        }
    }

    public static void main(String[] args) {
        int[] tamanios = {100};
        
        try (PrintWriter pw = new PrintWriter(new FileWriter("Resultados.csv"))) {
            pw.println("Lenguaje,Algoritmo,Tamano,Estado,TiempoMs,Comparaciones,Intercambios");

            System.out.println("=== INICIANDO BENCHMARKING EN JAVA ===");

            for (int tam : tamanios) {
                Random rand = new Random(42);
                int[] baseAleatoria = new int[tam];
                for (int i = 0; i < tam; i++) {
                    baseAleatoria[i] = rand.nextInt(1000001);
                }

                //Los 3 vectores
                int[] aleatorio = baseAleatoria.clone();
                
                int[] ordenado = baseAleatoria.clone();
                Arrays.sort(ordenado);
                
                int[] inverso = ordenado.clone();
                for (int i = 0; i < inverso.length / 2; i++) {
                    int temp = inverso[i];
                    inverso[i] = inverso[inverso.length - 1 - i];
                    inverso[inverso.length - 1 - i] = temp;
                }

                String[] nombres = {"Burbuja", "HeapSort", "Insercion", "MergeSort", "QuickSort", "RadixSort", "Seleccion", "ShellSort"};

                for (String nombreAlg : nombres) {
                    if (tam >= 100000 && (nombreAlg.equals("Burbuja") || nombreAlg.equals("Seleccion") || nombreAlg.equals("Insercion"))) {
                        System.out.println("Omitiendo " + nombreAlg + " para tamaño " + tam + " (complejidad O(n^2))");
                        continue;
                    }

                    probarAlgoritmo(pw, "Aleatorio", aleatorio, nombreAlg, tam);
                    probarAlgoritmo(pw, "Ordenado", ordenado, nombreAlg, tam);
                    probarAlgoritmo(pw, "Inverso", inverso, nombreAlg, tam);
                }
            }
            System.out.println("\n¡Pruebas de Java finalizadas! Archivo 'Resultados.csv' generado con éxito.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void probarAlgoritmo(PrintWriter pw, String estado, int[] original, String nombreAlg, int tam) {
        int[] arrCopia = original.clone();
        Ordenamientos sorter = new Ordenamientos();

        long inicio = System.nanoTime();

        switch (nombreAlg) {
            case "Burbuja": sorter.bubbleSort(arrCopia); break;
            case "HeapSort": sorter.heapSort(arrCopia); break;
            case "Insercion": sorter.insertionSort(arrCopia); break;
            case "MergeSort": sorter.mergeSort(arrCopia); break;
            case "QuickSort": sorter.quickSort(arrCopia); break;
            case "RadixSort": sorter.radixSort(arrCopia); break;
            case "Seleccion": sorter.selectionSort(arrCopia); break;
            case "ShellSort": sorter.shellSort(arrCopia); break;
        }

        long fin = System.nanoTime();
        double tiempoMs = (fin - inicio) / 1_000_000.0;

        pw.printf("Java,%s,%d,%s,%.4f,%d,%d\n", nombreAlg, tam, estado, tiempoMs, sorter.comparaciones, sorter.intercambios);
        System.out.printf("-> Tamaño: %d | Algoritmo: %s | Estado: %s | Tiempo: %.4f ms\n", tam, nombreAlg, estado, tiempoMs);
    }
}