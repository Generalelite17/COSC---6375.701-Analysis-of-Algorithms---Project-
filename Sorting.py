# Imported packages
import random
import time
import sys
import re
from concurrent.futures import ThreadPoolExecutor

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

# HeapSort helper function
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

# HeapSort
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

# Radix Sort helper function
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

# Radix Sort
def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

# Function to test the sorting algorithms
def test_sorting_algorithm(sort_function, arr):
    start_time = time.perf_counter()
    sort_function(arr)
    end_time = time.perf_counter()
    return end_time - start_time

# Main program
def main():
    print("Choose a sorting algorithm:")
    print("1. MergeSort")
    print("2. HeapSort")
    print("3. QuickSort")
    print("4. Insertion Sort")
    print("5. Radix Sort")
    print("6. All")
    print()
    choice = int(input("Enter the number of the algorithm you want to use: "))

    # Asks user if they want to input their own array or generate a random array
    array_choice = input("Do you want to (1) input your own array or (2) generate a random array? (Enter 1 or 2): ")

    if array_choice == '1':
        # Inputs custom array and ignores commas, special characters, and letters
        arr_input = input("Enter the elements of the array, separated by spaces or commas: ")

        # Replaces commas with spaces, then removes all non-numeric characters (letters, symbols, etc.)
        arr_input_cleaned = re.sub(r'[^0-9\s]', '', arr_input)

        # Splits the cleaned string by spaces and converts to integers
        arr = list(map(int, arr_input_cleaned.split()))

    elif array_choice == '2':
        # Inputs size for random array and range of values (min and max integers)
        size_and_range = input("Enter the array size, minimum value, and maximum value, separated by spaces: ")

        # Splits input into size and range values
        try:
            size, min_val, max_val = map(int, size_and_range.split())
            if min_val > max_val:
                print("Invalid range! The min_value must be less than or equal to the max_value.")
            # Generates the random array with specified size and range
            if size < 0:
                print("Invalid array size! The array size must be nonnegative.")
            if min_val > max_val or size < 0:
                sys.exit(1)
            arr = [random.randint(min_val, max_val) for _ in range(size)]
        except ValueError:
            print("Invalid input! Please enter the size and range as integers separated by spaces.")
            sys.exit(1)

    else:
        print("Invalid choice!")
        sys.exit(1)

    # Prints the unsorted array
    print("\nUnsorted array:")
    print(arr)

    if choice == 6:
        # Runs all algorithms in parallel using ThreadPoolExecutor
        print("\nSorting with all...")

        with ThreadPoolExecutor() as executor:
            # Prepares the tasks for each sorting algorithm
            futures = {
                "MergeSort": executor.submit(test_sorting_algorithm, merge_sort, arr.copy()),
                "HeapSort": executor.submit(test_sorting_algorithm, heap_sort, arr.copy()),
                "QuickSort": executor.submit(test_sorting_algorithm, quick_sort, arr.copy()),
                "Insertion Sort": executor.submit(test_sorting_algorithm, insertion_sort, arr.copy()),
                "Radix Sort": executor.submit(test_sorting_algorithm, radix_sort, arr.copy())
            }

            # Collects results and times in a dictionary
            times = {}
            for algorithm, future in futures.items():
                elapsed_time = future.result()
                times[algorithm] = elapsed_time

            # Sorts the sorting algorithms based on their completion times (from quickest to slowest)
            sorted_algorithms = sorted(times.items(), key=lambda x: x[1])

            # Prints the sorted times and corresponding algorithms
            print("\nSorting methods and their completion times (quickest to slowest):")
            for algorithm, elapsed_time in sorted_algorithms:
                print(f"{algorithm} took {elapsed_time:.6f} seconds.")

            # After all sorting algorithms are complete, prints the sorted array (from any algorithm)
            sorted_arr = merge_sort(arr.copy())  # You can use any sorted result here
            print("\nSorted array:")
            print(sorted_arr)

    else:
        # Selects the chosen algorithm
        if choice == 1:
            algorithm_name = "MergeSort"
            sort_function = merge_sort
        elif choice == 2:
            algorithm_name = "HeapSort"
            sort_function = heap_sort
        elif choice == 3:
            algorithm_name = "QuickSort"
            sort_function = quick_sort
            sorted_arr = quick_sort(arr)  # Capture the sorted result from QuickSort
        elif choice == 4:
            algorithm_name = "Insertion Sort"
            sort_function = insertion_sort
        elif choice == 5:
            algorithm_name = "Radix Sort"
            sort_function = radix_sort
        else:
            print("Invalid choice!")
            sys.exit(1)

        # Measures and displays the time taken to sort
        print(f"\nSorting with {algorithm_name}...")

        # For QuickSort, we already captured the sorted array in 'sorted_arr'
        if choice != 3:
            elapsed_time = test_sorting_algorithm(sort_function, arr)
            print(f"\nTime taken: {elapsed_time:.6f} seconds.")
            sorted_arr = arr  # For all other algorithms, 'arr' is modified in place
        else:
            elapsed_time = test_sorting_algorithm(sort_function, arr)
            print(f"\nTime taken: {elapsed_time:.6f} seconds.")

        # Prints the sorted array
        print("\nSorted array:")
        print(sorted_arr)  # noqa: specific-warning-code

if __name__ == "__main__":
    main()
