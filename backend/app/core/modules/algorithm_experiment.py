"""
算法实验生成器 - 数据结构与算法实验项目
"""
from pathlib import Path
from typing import Dict, Any
from app.core.modules.base import BaseGenerator


class AlgorithmExperimentGenerator(BaseGenerator):
    """算法实验生成器"""
    
    def __init__(self):
        super().__init__()
        self.name = "算法实验项目"
    
    async def generate(self, config: Dict[str, Any], output_dir: Path, templates_dir: Path) -> Dict[str, Any]:
        try:
            language = config.get("language", "cpp")
            algorithms = config.get("algorithms", ["sort", "search"])
            
            if language == "cpp":
                self._generate_cpp_project(output_dir, config, algorithms)
            elif language == "python":
                self._generate_python_project(output_dir, config, algorithms)
            else:
                self._generate_java_project(output_dir, config, algorithms)
            
            self._generate_readme(output_dir, config, algorithms)
            self._generate_report(output_dir / "docs", config, algorithms)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _generate_cpp_project(self, output_dir: Path, config: Dict, algorithms: list):
        """生成C++算法项目"""
        src_dir = output_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # CMakeLists.txt
        self.write_file(output_dir / "CMakeLists.txt", f'''cmake_minimum_required(VERSION 3.10)
project({config.get("project_name", "AlgorithmExperiment")})
set(CMAKE_CXX_STANDARD 17)
add_executable(main src/main.cpp)
''')
        
        main_content = '''#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>

using namespace std;
using namespace chrono;

'''
        
        if "sort" in algorithms:
            main_content += '''
// ==================== 排序算法 ====================

// 冒泡排序 O(n^2)
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// 选择排序 O(n^2)
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        swap(arr[i], arr[minIdx]);
    }
}

// 插入排序 O(n^2)
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// 快速排序 O(n log n)
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// 归并排序 O(n log n)
void merge(vector<int>& arr, int l, int m, int r) {
    vector<int> left(arr.begin() + l, arr.begin() + m + 1);
    vector<int> right(arr.begin() + m + 1, arr.begin() + r + 1);
    int i = 0, j = 0, k = l;
    while (i < left.size() && j < right.size()) {
        arr[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
    }
    while (i < left.size()) arr[k++] = left[i++];
    while (j < right.size()) arr[k++] = right[j++];
}

void mergeSort(vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

void testSortAlgorithms() {
    cout << "\\n===== 排序算法性能测试 =====\\n" << endl;
    
    vector<int> sizes = {1000, 5000, 10000};
    
    for (int n : sizes) {
        cout << "数据规模: " << n << endl;
        
        // 生成随机数据
        vector<int> original(n);
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dis(1, 100000);
        for (int& x : original) x = dis(gen);
        
        // 测试各个算法
        vector<int> arr;
        
        // 冒泡排序
        arr = original;
        auto start = high_resolution_clock::now();
        bubbleSort(arr);
        auto end = high_resolution_clock::now();
        cout << "  冒泡排序: " << duration_cast<milliseconds>(end - start).count() << "ms" << endl;
        
        // 选择排序
        arr = original;
        start = high_resolution_clock::now();
        selectionSort(arr);
        end = high_resolution_clock::now();
        cout << "  选择排序: " << duration_cast<milliseconds>(end - start).count() << "ms" << endl;
        
        // 插入排序
        arr = original;
        start = high_resolution_clock::now();
        insertionSort(arr);
        end = high_resolution_clock::now();
        cout << "  插入排序: " << duration_cast<milliseconds>(end - start).count() << "ms" << endl;
        
        // 快速排序
        arr = original;
        start = high_resolution_clock::now();
        quickSort(arr, 0, arr.size() - 1);
        end = high_resolution_clock::now();
        cout << "  快速排序: " << duration_cast<milliseconds>(end - start).count() << "ms" << endl;
        
        // 归并排序
        arr = original;
        start = high_resolution_clock::now();
        mergeSort(arr, 0, arr.size() - 1);
        end = high_resolution_clock::now();
        cout << "  归并排序: " << duration_cast<milliseconds>(end - start).count() << "ms" << endl;
        
        cout << endl;
    }
}
'''
        
        if "search" in algorithms:
            main_content += '''
// ==================== 查找算法 ====================

// 顺序查找 O(n)
int linearSearch(const vector<int>& arr, int target) {
    for (int i = 0; i < arr.size(); i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}

// 二分查找 O(log n)
int binarySearch(const vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

void testSearchAlgorithms() {
    cout << "\\n===== 查找算法性能测试 =====\\n" << endl;
    
    int n = 100000;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) arr[i] = i;
    
    int target = 99999;
    
    auto start = high_resolution_clock::now();
    int idx1 = linearSearch(arr, target);
    auto end = high_resolution_clock::now();
    cout << "顺序查找: 找到索引 " << idx1 << ", 耗时 " << duration_cast<microseconds>(end - start).count() << "μs" << endl;
    
    start = high_resolution_clock::now();
    int idx2 = binarySearch(arr, target);
    end = high_resolution_clock::now();
    cout << "二分查找: 找到索引 " << idx2 << ", 耗时 " << duration_cast<microseconds>(end - start).count() << "μs" << endl;
}
'''
        
        if "graph" in algorithms:
            main_content += '''
// ==================== 图论算法 ====================

// 图的邻接表表示
class Graph {
public:
    int V;
    vector<vector<pair<int, int>>> adj; // {邻接点, 权重}
    
    Graph(int v) : V(v), adj(v) {}
    
    void addEdge(int u, int v, int w = 1) {
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    
    // BFS 广度优先搜索
    void BFS(int start) {
        vector<bool> visited(V, false);
        queue<int> q;
        
        visited[start] = true;
        q.push(start);
        
        cout << "BFS遍历: ";
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            cout << node << " ";
            
            for (auto& [next, w] : adj[node]) {
                if (!visited[next]) {
                    visited[next] = true;
                    q.push(next);
                }
            }
        }
        cout << endl;
    }
    
    // DFS 深度优先搜索
    void DFSUtil(int node, vector<bool>& visited) {
        visited[node] = true;
        cout << node << " ";
        for (auto& [next, w] : adj[node]) {
            if (!visited[next]) DFSUtil(next, visited);
        }
    }
    
    void DFS(int start) {
        vector<bool> visited(V, false);
        cout << "DFS遍历: ";
        DFSUtil(start, visited);
        cout << endl;
    }
    
    // Dijkstra 最短路径
    vector<int> dijkstra(int src) {
        vector<int> dist(V, INT_MAX);
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        
        dist[src] = 0;
        pq.push({0, src});
        
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            
            if (d > dist[u]) continue;
            
            for (auto& [v, w] : adj[u]) {
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }
        return dist;
    }
};

#include <queue>
#include <climits>

void testGraphAlgorithms() {
    cout << "\\n===== 图论算法测试 =====\\n" << endl;
    
    Graph g(6);
    g.addEdge(0, 1, 4);
    g.addEdge(0, 2, 2);
    g.addEdge(1, 2, 1);
    g.addEdge(1, 3, 5);
    g.addEdge(2, 3, 8);
    g.addEdge(2, 4, 10);
    g.addEdge(3, 4, 2);
    g.addEdge(3, 5, 6);
    g.addEdge(4, 5, 3);
    
    g.BFS(0);
    g.DFS(0);
    
    cout << "\\nDijkstra最短路径 (从节点0出发):" << endl;
    vector<int> dist = g.dijkstra(0);
    for (int i = 0; i < dist.size(); i++) {
        cout << "  到节点" << i << ": " << dist[i] << endl;
    }
}
'''
        
        if "dp" in algorithms:
            main_content += '''
// ==================== 动态规划 ====================

// 斐波那契数列
long long fibonacci(int n) {
    if (n <= 1) return n;
    vector<long long> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    return dp[n];
}

// 0-1背包问题
int knapsack(vector<int>& weights, vector<int>& values, int capacity) {
    int n = weights.size();
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));
    
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (weights[i-1] <= w) {
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1]);
            } else {
                dp[i][w] = dp[i-1][w];
            }
        }
    }
    return dp[n][capacity];
}

// 最长公共子序列
int LCS(const string& s1, const string& s2) {
    int m = s1.size(), n = s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    return dp[m][n];
}

void testDynamicProgramming() {
    cout << "\\n===== 动态规划测试 =====\\n" << endl;
    
    // 斐波那契
    cout << "斐波那契数列 F(40) = " << fibonacci(40) << endl;
    
    // 0-1背包
    vector<int> weights = {2, 3, 4, 5};
    vector<int> values = {3, 4, 5, 6};
    int capacity = 8;
    cout << "0-1背包 (容量=" << capacity << "): 最大价值 = " << knapsack(weights, values, capacity) << endl;
    
    // LCS
    string s1 = "ABCDGH", s2 = "AEDFHR";
    cout << "最长公共子序列 (\\\"" << s1 << "\\\", \\\"" << s2 << "\\\"): " << LCS(s1, s2) << endl;
}
'''
        
        # main函数
        main_content += '''
int main() {
    cout << "======================================" << endl;
    cout << "        数据结构与算法实验" << endl;
    cout << "======================================" << endl;
'''
        
        if "sort" in algorithms:
            main_content += '    testSortAlgorithms();\n'
        if "search" in algorithms:
            main_content += '    testSearchAlgorithms();\n'
        if "graph" in algorithms:
            main_content += '    testGraphAlgorithms();\n'
        if "dp" in algorithms:
            main_content += '    testDynamicProgramming();\n'
        
        main_content += '''
    cout << "\\n所有测试完成!" << endl;
    return 0;
}
'''
        
        self.write_file(src_dir / "main.cpp", main_content)
    
    def _generate_python_project(self, output_dir: Path, config: Dict, algorithms: list):
        """生成Python算法项目"""
        src_dir = output_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据结构与算法实验 - Python版本
"""
import time
import random
from typing import List, Optional

'''
        
        if "sort" in algorithms:
            content += '''
# ==================== 排序算法 ====================

def bubble_sort(arr: List[int]) -> List[int]:
    """冒泡排序 O(n^2)"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr: List[int]) -> List[int]:
    """选择排序 O(n^2)"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr: List[int]) -> List[int]:
    """插入排序 O(n^2)"""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def quick_sort(arr: List[int]) -> List[int]:
    """快速排序 O(n log n)"""
    if len(arr) <= 1:
        return arr.copy()
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr: List[int]) -> List[int]:
    """归并排序 O(n log n)"""
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def test_sort_algorithms():
    print("\\n===== 排序算法性能测试 =====\\n")
    
    for n in [1000, 5000, 10000]:
        print(f"数据规模: {n}")
        original = [random.randint(1, 100000) for _ in range(n)]
        
        for name, func in [("冒泡排序", bubble_sort), ("选择排序", selection_sort), 
                           ("插入排序", insertion_sort), ("快速排序", quick_sort), 
                           ("归并排序", merge_sort)]:
            start = time.perf_counter()
            func(original)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"  {name}: {elapsed:.2f}ms")
        print()

'''
        
        if "search" in algorithms:
            content += '''
# ==================== 查找算法 ====================

def linear_search(arr: List[int], target: int) -> int:
    """顺序查找 O(n)"""
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1

def binary_search(arr: List[int], target: int) -> int:
    """二分查找 O(log n)"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def test_search_algorithms():
    print("\\n===== 查找算法性能测试 =====\\n")
    
    n = 100000
    arr = list(range(n))
    target = n - 1
    
    start = time.perf_counter()
    idx1 = linear_search(arr, target)
    elapsed1 = (time.perf_counter() - start) * 1000000
    print(f"顺序查找: 找到索引 {idx1}, 耗时 {elapsed1:.2f}μs")
    
    start = time.perf_counter()
    idx2 = binary_search(arr, target)
    elapsed2 = (time.perf_counter() - start) * 1000000
    print(f"二分查找: 找到索引 {idx2}, 耗时 {elapsed2:.2f}μs")

'''
        
        if "dp" in algorithms:
            content += '''
# ==================== 动态规划 ====================

def fibonacci(n: int) -> int:
    """斐波那契数列"""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """0-1背包问题"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]

def lcs(s1: str, s2: str) -> int:
    """最长公共子序列"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def test_dynamic_programming():
    print("\\n===== 动态规划测试 =====\\n")
    
    print(f"斐波那契数列 F(40) = {fibonacci(40)}")
    
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    print(f"0-1背包 (容量={capacity}): 最大价值 = {knapsack(weights, values, capacity)}")
    
    s1, s2 = "ABCDGH", "AEDFHR"
    print(f'最长公共子序列 ("{s1}", "{s2}"): {lcs(s1, s2)}')

'''
        
        content += '''
if __name__ == "__main__":
    print("======================================")
    print("        数据结构与算法实验")
    print("======================================")
'''
        
        if "sort" in algorithms:
            content += '    test_sort_algorithms()\n'
        if "search" in algorithms:
            content += '    test_search_algorithms()\n'
        if "dp" in algorithms:
            content += '    test_dynamic_programming()\n'
        
        content += '    print("\\n所有测试完成!")\n'
        
        self.write_file(src_dir / "main.py", content)
        self.write_file(output_dir / "requirements.txt", "# 无额外依赖\n")
    
    def _generate_java_project(self, output_dir: Path, config: Dict, algorithms: list):
        """生成Java算法项目"""
        src_dir = output_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        self.write_file(src_dir / "Main.java", '''public class Main {
    public static void main(String[] args) {
        System.out.println("数据结构与算法实验 - Java版本");
        // TODO: 实现算法
    }
}
''')
    
    def _generate_readme(self, output_dir: Path, config: Dict, algorithms: list):
        algo_names = {"sort": "排序算法", "search": "查找算法", "graph": "图论算法", "dp": "动态规划"}
        algo_list = ", ".join([algo_names.get(a, a) for a in algorithms])
        
        self.write_file(output_dir / "README.md", f'''# {config.get("project_name_cn", "算法实验项目")}

## 项目简介
数据结构与算法实验项目，包含：{algo_list}

## 运行方式

### C++版本
```bash
mkdir build && cd build
cmake ..
make
./main
```

### Python版本
```bash
python src/main.py
```

## 作者
{config.get("author", "Student")}
''')
    
    def _generate_report(self, docs_dir: Path, config: Dict, algorithms: list):
        docs_dir.mkdir(exist_ok=True)
        algo_names = {"sort": "排序算法", "search": "查找算法", "graph": "图论算法", "dp": "动态规划"}
        
        content = f'''# {config.get("project_name_cn", "算法实验项目")} 实验报告

## 一、实验目的
掌握常用数据结构与算法的实现与性能分析。

## 二、实验环境
- 编程语言：{config.get("language", "C++")}
- 编译器/解释器：GCC / Python 3.x

## 三、实验内容

'''
        
        if "sort" in algorithms:
            content += '''### 3.1 排序算法
实现了以下排序算法：
- 冒泡排序 O(n²)
- 选择排序 O(n²)
- 插入排序 O(n²)
- 快速排序 O(n log n)
- 归并排序 O(n log n)

'''
        
        if "search" in algorithms:
            content += '''### 3.2 查找算法
实现了以下查找算法：
- 顺序查找 O(n)
- 二分查找 O(log n)

'''
        
        if "dp" in algorithms:
            content += '''### 3.3 动态规划
实现了以下动态规划问题：
- 斐波那契数列
- 0-1背包问题
- 最长公共子序列(LCS)

'''
        
        content += f'''## 四、实验结果
运行程序后可看到各算法的性能对比结果。

## 五、实验总结
通过本次实验，深入理解了各种算法的实现原理和时间复杂度。

## 作者：{config.get("author", "Student")}
'''
        
        self.write_file(docs_dir / "实验报告.md", content)
