#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <fstream>

using namespace std;

class BenchmarkOrdenamientos {
public:
    long long comparaciones = 0;
    long long intercambios = 0;

    void reiniciarContadores() {
        comparaciones = 0;
        intercambios = 0;
    }

    //Ordenamiento Burbuja 1
    void bubbleSort(int a[], int s) {
        reiniciarContadores();
        for (int i = 0; i < s; i++) {
            bool isSwapped = false;
            for (int j = 0; j < s - i - 1; j++) {
                comparaciones++;
                if (a[j] > a[j+1]) {
                    int temp = a[j];
                    a[j] = a[j+1];
                    a[j+1] = temp;
                    intercambios++;
                    isSwapped = true;
                }
            }
            if (!isSwapped) break;
        }
    }

    //Ordenamiento HeapSort 2
    void heapSort(int arr[], int n) {
        reiniciarContadores();
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

    void heapify(int arr[], int n, int i) {
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
    void insertionSort(int a[], int n) {
        reiniciarContadores();
        for (int i = 1; i < n; i++) {
            int temp = a[i];
            int j = i - 1;
            comparaciones++;
            while (j >= 0 && temp < a[j]) {
                comparaciones++;
                a[j+1] = a[j];
                intercambios++;
                j = j - 1;
            }
            a[j+1] = temp;
        }
    }

    //Ordenamiento MergeSort 4
    void mergeSort(int a[], int l, int r) {
        reiniciarContadores();
        mergeSortRec(a, l, r);
    }

    void mergeSortRec(int a[], int l, int r) {
        if (l < r) {
            int m = (l + r) / 2;
            mergeSortRec(a, l, m);
            mergeSortRec(a, m + 1, r);
            merge(a, l, m, r);
        }
    }

    void merge(int a[], int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;

        vector<int> L(n1);
        vector<int> R(n2);

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
    void quickSort(int a[], int l, int h) {
        reiniciarContadores();
        qckSortRec(a, l, h);
    }

    void qckSortRec(int a[], int l, int h) {
        if (l < h) {
            int pi = partition(a, l, h);
            qckSortRec(a, l, pi - 1);
            qckSortRec(a, pi + 1, h);
        }
    }

    int partition(int a[], int l, int h) {
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
    void radixSort(int arr[], int n) {
        reiniciarContadores();
        if (n <= 0) return;
        int maxVal = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] > maxVal) maxVal = arr[i];
        }
        for (int exp = 1; maxVal / exp > 0; exp *= 10) {
            countingSortRadix(arr, n, exp);
        }
    }

    void countingSortRadix(int arr[], int n, int exp) {
        vector<int> outputArray(n);
        int countArray[10] = {0};

        for (int j = 0; j < n; j++) {
            int idx = (arr[j] / exp) % 10;
            countArray[idx]++;
        }
        for (int i = 1; i < 10; i++) {
            countArray[i] += countArray[i - 1];
        }
        int j = n - 1;
        while (j >= 0) {
            int idx = (arr[j] / exp) % 10;
            outputArray[countArray[idx] - 1] = arr[j];
            countArray[idx]--;
            intercambios++;
            j--;
        }
        for (int k = 0; k < n; k++) {
            arr[k] = outputArray[k];
        }
    }

    //Ordenamiento Seleccion 7
    void selectionSort(int a[], int n) {
        reiniciarContadores();
        for (int i = 0; i < n; i++) {
            int small = i;
            for (int j = i + 1; j < n; j++) {
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
    void shellSort(int imputArr[], int size) {
        reiniciarContadores();
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
};

void ejecutarPrueba(ofstream& archivoCsv, string nombreAlg, string estado, vector<int>& original, int tam) {
    vector<int> arrCopia = original;
    BenchmarkOrdenamientos sorter;

    auto inicio = chrono::high_resolution_clock::now();

    if (nombreAlg == "Burbuja") sorter.bubbleSort(arrCopia.data(), tam);
    else if (nombreAlg == "HeapSort") sorter.heapSort(arrCopia.data(), tam);
    else if (nombreAlg == "Insercion") sorter.insertionSort(arrCopia.data(), tam);
    else if (nombreAlg == "MergeSort") sorter.mergeSort(arrCopia.data(), 0, tam - 1);
    else if (nombreAlg == "QuickSort") sorter.quickSort(arrCopia.data(), 0, tam - 1);
    else if (nombreAlg == "RadixSort") sorter.radixSort(arrCopia.data(), tam);
    else if (nombreAlg == "Seleccion") sorter.selectionSort(arrCopia.data(), tam);
    else if (nombreAlg == "ShellSort") sorter.shellSort(arrCopia.data(), tam);

    auto fin = chrono::high_resolution_clock::now();
    chrono::duration<double, milli> duracion = fin - inicio;

    archivoCsv << "C++," << nombreAlg << "," << tam << "," << estado << "," 
               << duracion.count() << "," << sorter.comparaciones << "," << sorter.intercambios << "\n";

    cout << "-> Tamaño: " << tam << " | Algoritmo: " << nombreAlg << " | Estado: " << estado 
         << " | Tiempo: " << duracion.count() << " ms" << endl;
}

int main() {
    vector<int> tamanios = {100};
    ofstream archivoCsv("Resultado.csv");

    if (!archivoCsv.is_open()) {
        cout << "Error al abrir el archivo CSV para escritura." << endl;
        return 1;
    }

    archivoCsv << "Lenguaje,Algoritmo,Tamano,Estado,TiempoMs,Comparaciones,Intercambios\n";

    cout << "=== INICIANDO ORDENAMIENTOS EN C++ ===" << endl;

    for (int tam : tamanios) {
        mt19937 generator(42); // Semilla fija 42
        uniform_int_distribution<int> distribution(0, 1000000);

        vector<int> baseAleatoria(tam);
        for (int i = 0; i < tam; ++i) {
            baseAleatoria[i] = distribution(generator);
        }

        vector<int> aleatorio = baseAleatoria;
        vector<int> ordenado = baseAleatoria;
        sort(ordenado.begin(), ordenado.end());
        vector<int> inverso = ordenado;
        reverse(inverso.begin(), inverso.end());

        vector<string> nombres = {"Burbuja", "HeapSort", "Insercion", "MergeSort", "QuickSort", "RadixSort", "Seleccion", "ShellSort"};

        for (string nombreAlg : nombres) {
            if (tam >= 100000 && (nombreAlg == "Burbuja" || nombreAlg == "Seleccion" || nombreAlg == "Insercion")) {
                cout << "Omitiendo " << nombreAlg << " para tamaño " << tam << " (complejidad O(n^2))" << endl;
                continue;
            }

            ejecutarPrueba(archivoCsv, nombreAlg, "Aleatorio", aleatorio, tam);
            ejecutarPrueba(archivoCsv, nombreAlg, "Ordenado", ordenado, tam);
            ejecutarPrueba(archivoCsv, nombreAlg, "Inverso", inverso, tam);
        }
    }

    archivoCsv.close();
    cout << "\n¡Pruebas de C++ finalizadas! Archivo 'Resultado.csv' generado con éxito." << endl;
    return 0;
}