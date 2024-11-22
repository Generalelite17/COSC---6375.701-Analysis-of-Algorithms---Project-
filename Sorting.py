# Imported packages
import random
import time
import sys
import re
from concurrent.futures import ThreadPoolExecutor

# MergeSort
def merge_sort(arr):
    if len(arr) > 1:
        # Divides the array into two halves
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Sorts the left and right halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Sets the indices for the while conditions
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
    # Assigns the parent-child relationships
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Creates the heap data structure
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

# HeapSort
def heap_sort(arr):
    # Sets the size of the array to be built
    n = len(arr)

    # Assigns heap elements to create the sorted array
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

# QuickSort
def quick_sort(arr):
    # Returns the trivial case
    if len(arr) <= 1:
        return arr

    # Chooses the center element to partition around
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Insertion Sort
def insertion_sort(arr):
    # Iterates through the array for potential swaps
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Radix Sort helper function
def counting_sort(arr, exp, scale_factor):
    # Initializes arrays
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Stores count of occurrences
    for i in range(n):
        # Get the digit at the current exp place, using scale_factor to shift decimal places
        index = int(arr[i] * scale_factor // exp) % 10
        count[index] += 1

    # Changes count[i] to contain the actual position of the digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Builds the output array
    i = n - 1
    while i >= 0:
        # Gets the digit at the current exp place
        index = int(arr[i] * scale_factor // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    # Copies the output array to arr[], so that arr[] contains sorted numbers
    for i in range(n):
        arr[i] = output[i]

# Radix Sort
def radix_sort(arr):
    # Separates positive and negative numbers
    negative_numbers = [num for num in arr if num < 0]
    positive_numbers = [num for num in arr if num >= 0]

    # Helper function to sort numbers
    def sort_numbers(nums):
        if not nums:
            return nums

        # Finds the maximum value (absolute value) to determine the number of digits
        max_val = max(nums, key=lambda x: abs(x))

        # Finds the scaling factor (based on decimal places)
        scale_factor = 10 ** max(len(str(abs(x)).split('.')[1]) if '.' in str(abs(x)) else 0 for x in nums)

        # Applies counting sort for every digit
        exp = 1
        while max_val * scale_factor // exp > 1:
            counting_sort(nums, exp, scale_factor)
            exp *= 10

        return nums

    # Sorts the positive numbers as they are
    sorted_positive = sort_numbers(positive_numbers)

    # Sorts the negative numbers by first converting them to positive for sorting
    sorted_negative = sort_numbers([-num for num in negative_numbers])

    # Restores the negative signs on sorted negative numbers
    sorted_negative = [-num for num in sorted_negative]

    # Reverses the sorted negative array to get the largest negative values first
    sorted_negative.reverse()

    # Concatenates the negative and positive numbers
    return sorted_negative + sorted_positive

# Function to test the sorting algorithms
def test_sorting_algorithm(sort_function, arr):
    start_time = time.perf_counter()
    sort_function(arr)
    end_time = time.perf_counter()
    return end_time - start_time

# Main program
def main():
    # Asks user if they want to input their own array or generate a random array
    array_choice = input("Which type of array would you like?"
                         "\n(1) generate a random array of integers"
                         "\n(2) generate a random array of decimals"
                         "\n(3) input your own array"
                         "\n"
                         "\n(Enter 1,2, or 3): ")

    # Array of integers
    if array_choice == '1':
        # Inputs size for random array and range of values (min and max values)
        size_and_range = input("Enter the array size, minimum value, and maximum value, separated by spaces: ")

        # Splits input into size and range values
        try:
            size, min_val, max_val = map(int, size_and_range.split())
            if min_val > max_val:
                print("Invalid range! The min_value must be less than or equal to the max_value.")
            if size < 0 or not size.is_integer():
                print("Invalid array size! The array size must be a nonnegative integer.")
            if min_val > max_val or size < 0 or not size.is_integer():
                sys.exit(1)

            # Generates the random array with specified size and range
            arr = [random.randint(min_val, max_val) for _ in range(int(size))]
        except ValueError:
            print("Invalid input! Please enter the size and range as integers separated by spaces.")
            sys.exit(1)

    # Array of decimals
    elif array_choice == '2':
        # Inputs size for random array and range of values (min and max values)
        size_and_range = input("Enter the array size, minimum value, and maximum value, separated by spaces: ")

        # Splits input into size and range values
        try:
            size, min_val, max_val = map(float, size_and_range.split())
            if min_val > max_val:
                print("Invalid range! The min_value must be less than or equal to the max_value.")
            if size < 0 or not size.is_integer():
                print("Invalid array size! The array size must be a nonnegative integer.")
            if min_val > max_val or size < 0 or not size.is_integer():
                sys.exit(1)

            # Generates the random array with specified size and range
            arr = []
            for _ in range(int(size)):
                decimal_places = random.randint(0, 5)  # Random decimal places between 0 and 5
                random_value = random.uniform(min_val, max_val)
                rounded_value = round(random_value, decimal_places)  # Round to the chosen number of decimal places
                arr.append(rounded_value)
        except ValueError:
            print("Invalid input! Please enter the size and range as numbers separated by spaces.")
            sys.exit(1)

    # Custom array
    elif array_choice == '3':
        # Inputs custom array and ignores commas, special characters, and letters
        arr_input = input("Enter the elements of the array, separated by spaces or commas: ")

        # Replaces commas with spaces, then removes all non-numeric characters (letters, symbols, etc.)
        arr_input_cleaned = re.sub(r'[^0-9.,\s-]', '', arr_input)

        # Splits the cleaned string by spaces and converts to float to allow decimals
        arr = list(map(float, arr_input_cleaned.split()))

    # For values other than 1, 2, or 3
    else:
        print("Invalid choice!")
        sys.exit(1)

    # Print statements for algorithm selection
    print("Choose a sorting algorithm:")
    print("0. Recommended")
    print("1. MergeSort")
    print("2. HeapSort")
    print("3. QuickSort")
    print("4. Insertion Sort")
    print("5. Radix Sort")
    print("6. All")
    print()
    choice = int(input("Enter the number of the algorithm you want to use: "))

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
            sorted_arrays = {}
            for algorithm, future in futures.items():
                elapsed_time = future.result()
                times[algorithm] = elapsed_time

                # Stores the sorted arrays
                if algorithm == "MergeSort":
                    sorted_arrays[algorithm] = merge_sort(arr.copy())
                elif algorithm == "HeapSort":
                    sorted_arrays[algorithm] = heap_sort(arr.copy())
                elif algorithm == "QuickSort":
                    sorted_arrays[algorithm] = quick_sort(arr.copy())
                elif algorithm == "Insertion Sort":
                    sorted_arrays[algorithm] = insertion_sort(arr.copy())
                elif algorithm == "Radix Sort":
                    sorted_arrays[algorithm] = radix_sort(arr.copy())

            # Sorts the sorting algorithms based on their completion times (from quickest to slowest)
            sorted_algorithms = sorted(times.items(), key=lambda x: x[1])

            # Prints the sorted times and corresponding algorithms
            print("\nSorting methods and their completion times (quickest to slowest):")
            for algorithm, elapsed_time in sorted_algorithms:
                print(f"{algorithm} took {elapsed_time:.6f} seconds.")

            # Prints the sorted array from any algorithm (use one of the sorted arrays)
            chosen_algorithm = sorted_algorithms[0][0]  # Get the fastest algorithm
            print(f"\nSorted array using {chosen_algorithm}:")
            print(sorted_arrays[chosen_algorithm])

    else:
        sorted_arr = arr
        # Selects the chosen algorithm
        if choice == 0:
            algorithm_name = "MergeSort"
            sort_function = merge_sort
            sorted_arr = merge_sort(arr)
        elif choice == 1:
            algorithm_name = "MergeSort"
            sort_function = merge_sort
            sorted_arr = merge_sort(arr)
        elif choice == 2:
            algorithm_name = "HeapSort"
            sort_function = heap_sort
            sorted_arr = heap_sort(arr)
        elif choice == 3:
            algorithm_name = "QuickSort"
            sort_function = quick_sort
            sorted_arr = quick_sort(arr)
        elif choice == 4:
            algorithm_name = "Insertion Sort"
            sort_function = insertion_sort
            sorted_arr = insertion_sort(arr)
        elif choice == 5:
            algorithm_name = "Radix Sort"
            sort_function = radix_sort
            sorted_arr = radix_sort(arr)
        else:
            print("Invalid choice!")
            sys.exit(1)

        # Tells the user which algorithm was chosen
        print(f"\nSorting with {algorithm_name}...")

        # Measures and displays the time taken to sort
        elapsed_time = test_sorting_algorithm(sort_function, arr)
        print(f"\nTime taken: {elapsed_time:.6f} seconds.")

        # Prints the sorted array
        print("\nSorted array:")
        print(sorted_arr)

if __name__ == "__main__":
    main()
