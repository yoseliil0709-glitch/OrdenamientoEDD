#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <chrono>
#include <random>
#include <algorithm>
#include <functional>

struct Metrics {
    long long comp = 0;
    long long inter = 0;
};

std::vector<int> generar_arreglo(int n) {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(1, 1000000);
    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        arr[i] = dist(rng);
    }
    return arr;
}

//Ordenamiento 1 BubbleSort
Metrics bubble_sort(std::vector<int>& arr) {
    Metrics m;
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            m.comp++;
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
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
Metrics selection_sort(std::vector<int>& arr) {
    Metrics m;
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        int min_idx = i;
        for (int j = i + 1; j < n; ++j) {
            m.comp++;
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            std::swap(arr[min_idx], arr[i]);
            m.inter++;
        }
    }
    return m;
}

//Ordenamiento 3 InsertionSort
Metrics insertion_sort(std::vector<int>& arr) {
    Metrics m;
    int n = arr.size();
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
Metrics quick_sort(std::vector<int>& arr) {
    Metrics m;
    
    std::function<void(int, int)> _quick_sort = [&](int low, int high) {
        if (low < high) {
            auto partition = [&](int l, int h) {
                int pivot = arr[h];
                int i = l - 1;
                for (int j = l; j < h; ++j) {
                    m.comp++;
                    if (arr[j] < pivot) {
                        i++;
                        std::swap(arr[i], arr[j]);
                        m.inter++;
                    }
                }
                std::swap(arr[i + 1], arr[h]);
                m.inter++;
                return i + 1;
            };

            int pi = partition(low, high);
            _quick_sort(low, pi - 1);
            _quick_sort(pi + 1, high);
        }
    };

    if (arr.size() > 1) {
        _quick_sort(0, arr.size() - 1);
    }
    return m;
}

//Ordenamiento 5 MergeSort
Metrics merge_sort(std::vector<int>& arr) {
    Metrics m;

    auto _merge = [&](int l, int mid, int r) {
        int n1 = mid - l + 1;
        int n2 = r - mid;
        std::vector<int> L(arr.begin() + l, arr.begin() + mid + 1);
        std::vector<int> R(arr.begin() + mid + 1, arr.begin() + r + 1);
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

    std::function<void(int, int)> _merge_sort = [&](int l, int r) {
        if (l < r) {
            int mid = l + (r - l) / 2;
            _merge_sort(l, mid);
            _merge_sort(mid + 1, r);
            _merge(l, mid, r);
        }
    };

    if (arr.size() > 1) {
        _merge_sort(0, arr.size() - 1);
    }
    return m;
}

//Ordenamiento 6 HeapSort
Metrics heap_sort(std::vector<int>& arr) {
    Metrics m;
    int n = arr.size();

    std::function<void(int, int)> heapify = [&](int n_sz, int i) {
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
            std::swap(arr[i], arr[largest]);
            m.inter++;
            heapify(n_sz, largest);
        }
    };

    for (int i = n / 2 - 1; i >= 0; --i) {
        heapify(n, i);
    }
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        m.inter++;
        heapify(i, 0);
    }
    return m;
}

//Ordenamiento 7 ShellSort
Metrics shell_sort(std::vector<int>& arr) {
    Metrics m;
    int n = arr.size();
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
Metrics bucket_sort(std::vector<int>& arr) {
    Metrics m;
    if (arr.size() <= 1) {
        return m;
    }
    
    int min_val = *std::min_element(arr.begin(), arr.end());
    int max_val = *std::max_element(arr.begin(), arr.end());
    int n = arr.size();
    
    std::vector<std::vector<int>> buckets(n);
    
    for (int i = 0; i < n; ++i) {
        m.comp++;
        int bi = 0;
        if (max_val == min_val) {
            bi = 0;
        } else {
            bi = (int)((long long)(arr[i] - min_val) * (n - 1) / (max_val - min_val));
        }
        if (bi >= n) bi = n - 1;
        buckets[bi].push_back(arr[i]);
    }

    for (auto& b : buckets) {
        for (size_t i = 1; i < b.size(); ++i) {
            int key = b[i];
            int j = (int)i - 1;
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
    for (const auto& b : buckets) {
        for (int val : b) {
            arr[idx] = val;
            m.inter++;
            idx++;
        }
    }
            
    return m;
}

void _counting_sort_radix(std::vector<int>& arr, int exp, Metrics& m) {
    int n = arr.size();
    std::vector<int> output(n, 0);
    std::vector<int> count(10, 0);
    
    for (int i = 0; i < n; ++i) {
        m.comp++;
        int index = (arr[i] / exp) % 10;
        count[index]++;
    }
        
    for (int i = 1; i < 10; ++i) {
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
        
    for (int k = 0; k < n; ++k) {
        arr[k] = output[k];
        m.inter++;
    }
}

//Ordenamiento 9 RadixSort
Metrics radix_sort(std::vector<int>& arr) {
    Metrics m;
    if (arr.size() <= 1) {
        return m;
    }
        
    int max_val = *std::max_element(arr.begin(), arr.end());
    int exp = 1;
    while (max_val / exp > 0) {
        _counting_sort_radix(arr, exp, m);
        exp *= 10;
    }
    return m;
}

int main() {
    std::vector<int> tamanos = {100, 1000, 10000, 100000};
    std::vector<std::pair<std::string, std::function<Metrics(std::vector<int>&)>>> algoritmos = {
        {"Burbuja", bubble_sort},
        {"Seleccion", selection_sort},
        {"Insercion", insertion_sort},
        {"QuickSort", quick_sort},
        {"MergeSort", merge_sort},
        {"HeapSort", heap_sort},
        {"ShellSort", shell_sort},
        {"BucketSort", bucket_sort},
        {"RadixSort", radix_sort}
    };

    std::string archivo_txt = "ResultadosC++.txt";
    std::ofstream f(archivo_txt);
    if (f.is_open()) {
        f << "Tamano\tAlgoritmo\tEstado\tTiempoMs\tComparaciones\tIntercambios\n";

        for (int n : tamanos) {
            std::vector<int> original = generar_arreglo(n);

            std::vector<int> ord = original;
            std::sort(ord.begin(), ord.end());
            std::vector<int> rev = ord;
            std::reverse(rev.begin(), rev.end());

            std::vector<std::pair<std::string, std::vector<int>>> estados = {
                {"Aleatorio", original},
                {"Ordenado", ord},
                {"Inverso", rev}
            };

            for (auto& estado_pair : estados) {
                std::string estado = estado_pair.first;
                std::vector<int> arr_base = estado_pair.second;

                for (auto& alg_pair : algoritmos) {
                    std::string nombre = alg_pair.first;
                    auto func = alg_pair.second;

                    std::vector<int> copia = arr_base;
                    auto inicio = std::chrono::high_resolution_clock::now();
                    Metrics metrics = func(copia);
                    auto fin = std::chrono::high_resolution_clock::now();
                    std::chrono::duration<double, std::milli> duracion = fin - inicio;
                    double tiempo_ms = duracion.count();

                    f << n << "\t" << nombre << "\t" << estado << "\t" << tiempo_ms << "\t" << metrics.comp << "\t" << metrics.inter << "\n";
                    std::cout << "Tamaño: " << n << " | Algoritmo: " << nombre << " | Estado: " << estado << " | Tiempo: " << tiempo_ms << " ms\n";
                }
            }
        }
        f.close();
    }

    std::cout << "Ordenamientos ejecutados correctamente\n";
    return 0;
}