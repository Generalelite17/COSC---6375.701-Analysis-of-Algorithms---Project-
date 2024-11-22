import random
import time
import sys

# MergeSort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr

# HeapSort
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# QuickSort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Radix Sort
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

# Function to test the sorting algorithms
def test_sorting_algorithm(sort_function, arr):
    start_time = time.time()
    sort_function(arr)
    end_time = time.time()
    return end_time - start_time

# Main program
def main():
    print("Choose a sorting algorithm:")
    print("1. MergeSort")
    print("2. HeapSort")
    print("3. QuickSort")
    print("4. Insertion Sort")
    print("5. Radix Sort")

    choice = int(input("Enter the number of the algorithm you want to use: "))
    size = int(input("Enter the size of the array to sort: "))

    # Generate random array
    arr = [random.randint(0, 100000) for _ in range(size)]

    # Print the unsorted array
    print("\nUnsorted array:")
    print(arr)

    # Select the chosen algorithm
    if choice == 1:
        algorithm_name = "MergeSort"
        sort_function = merge_sort
    elif choice == 2:
        algorithm_name = "HeapSort"
        sort_function = heap_sort
    elif choice == 3:
        algorithm_name = "QuickSort"
        sort_function = quick_sort
    elif choice == 4:
        algorithm_name = "Insertion Sort"
        sort_function = insertion_sort
    elif choice == 5:
        algorithm_name = "Radix Sort"
        sort_function = radix_sort
    else:
        print("Invalid choice!")
        sys.exit(1)

    # Measure and display the time taken to sort
    print(f"\nSorting with {algorithm_name}...")
    elapsed_time = test_sorting_algorithm(sort_function, arr)

    # Print the sorted array
    print("\nSorted array:")
    print(arr)

    # Print the time taken
    print(f"\nTime taken: {elapsed_time:.6f} seconds.")

if __name__ == "__main__":
    main()
