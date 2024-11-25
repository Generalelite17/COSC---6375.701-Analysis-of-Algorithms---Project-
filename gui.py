import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Sorting import merge_sort, heap_sort, quick_sort, insertion_sort, radix_sort
import random
import time
from concurrent.futures import ThreadPoolExecutor


# Set TCL and TK libraries to avoid errors with Tkinter on some systems
os.environ['TCL_LIBRARY'] = r"C:\Users\emman\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"  # Adjust to your path
os.environ['TK_LIBRARY'] = r"C:\Users\emman\AppData\Local\Programs\Python\Python313\tcl\tk8.6"   # Adjust to your path

root = tk.Tk()
root.title("Sorting Algorithm Time Calculator")  # Set the window title

# Create the canvas and scrollbar for the entire GUI
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

# Create a frame that will hold all the content (widgets) inside the canvas
canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# Link scrollbar to the canvas
canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)

# Grid the canvas and scrollbar into the main window
canvas.grid(row=0, column=0, sticky="nsew")  # Canvas in the first column, expands in all directions
scrollbar.grid(row=0, column=1, sticky="ns")  # Scrollbar in the second column, fills vertically

# Configure grid to expand with window resizing
#main_window.grid_columnconfigure(0, weight=1)  # Make the first column (canvas) expandable
#main_window.grid_rowconfigure(0, weight=1)     # Make the first row (canvas) expandable



# Function to test sorting algorithms and record the time
def test_sorting_algorithm(sort_function, arr):
    start_time = time.time()
    sort_function(arr)
    end_time = time.time()
    return end_time - start_time

# Function to generate random array
def generate_random_array(size, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(size)]

def plot_times(times, canvas_frame):
    # Clear previous plot in the frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    algorithms = list(times.keys())
    execution_times = list(times.values())

    # Plot data
    ax.bar(algorithms, execution_times, color='skyblue')
    ax.set_xlabel("Sorting Algorithms")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title("Comparison of Sorting Algorithms")

    # Create a new frame for the plot (keep it separate from the result text)
    plot_frame = tk.Frame(canvas_frame)  # Create a new frame to hold the plot
    plot_frame.grid(row=0, column=0, sticky="nsew")  # Position it separately

    # Create the canvas and attach the plot to it
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  # Attach the plot to the canvas_frame
    canvas.draw()  # Render the plot

    # Add the plot to the Tkinter window
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")  # Positioning the widget in canvas_frame

    # Update the canvas to ensure proper layout
    canvas.get_tk_widget().update_idletasks()

    # Now apply the scrollregion to the canvas (not the frame)
    canvas.get_tk_widget().config(scrollregion=canvas.get_tk_widget().bbox("all"))



# Function to start sorting based on user choice
def sort_choice(choice, arr, result_text_widget):
    #result_text_widget.delete(1.0, tk.END)  # Clear previous results

    # Display the array before sorting
    #result_text_widget.insert(tk.END, f"Original Array: {arr}\n")

    if choice == 1:
        result_text_widget.insert(tk.END, "\nRunning MergeSort...\n")
        elapsed_time = test_sorting_algorithm(merge_sort, arr)
        result_text_widget.insert(tk.END, f"MergeSort took {elapsed_time:.6f} seconds.\n")
        sorted_arr = merge_sort(arr)
        result_text_widget.insert(tk.END, f"Sorted Array: {sorted_arr}\n")

    elif choice == 2:
        result_text_widget.insert(tk.END, "\nRunning HeapSort...\n")
        elapsed_time = test_sorting_algorithm(heap_sort, arr)
        result_text_widget.insert(tk.END, f"HeapSort took {elapsed_time:.6f} seconds.\n")
        sorted_arr = heap_sort(arr)
        result_text_widget.insert(tk.END, f"Sorted Array: {sorted_arr}\n")

    elif choice == 3:
        result_text_widget.insert(tk.END, "\nRunning QuickSort...\n")
        elapsed_time = test_sorting_algorithm(quick_sort, arr)
        result_text_widget.insert(tk.END, f"QuickSort took {elapsed_time:.6f} seconds.\n")
        sorted_arr = quick_sort(arr)
        result_text_widget.insert(tk.END, f"Sorted Array: {sorted_arr}\n")

    elif choice == 4:
        result_text_widget.insert(tk.END, "\nRunning Insertion Sort...\n")
        elapsed_time = test_sorting_algorithm(insertion_sort, arr)
        result_text_widget.insert(tk.END, f"Insertion Sort took {elapsed_time:.6f} seconds.\n")
        sorted_arr = insertion_sort(arr)
        result_text_widget.insert(tk.END, f"Sorted Array: {sorted_arr}\n")

    elif choice == 5:
        result_text_widget.insert(tk.END, "\nRunning Radix Sort...\n")
        elapsed_time = test_sorting_algorithm(radix_sort, arr)
        result_text_widget.insert(tk.END, f"Radix Sort took {elapsed_time:.6f} seconds.\n")
        sorted_arr = radix_sort(arr)
        result_text_widget.insert(tk.END, f"Sorted Array: {sorted_arr}\n")

    elif choice == 6:
        result_text_widget.insert(tk.END, "\nSorting with all...\n")

        with ThreadPoolExecutor() as executor:
            futures = {
                "MergeSort": executor.submit(test_sorting_algorithm, merge_sort, arr.copy()),
                "HeapSort": executor.submit(test_sorting_algorithm, heap_sort, arr.copy()),
                "QuickSort": executor.submit(test_sorting_algorithm, quick_sort, arr.copy()),
                "Insertion Sort": executor.submit(test_sorting_algorithm, insertion_sort, arr.copy()),
                "Radix Sort": executor.submit(test_sorting_algorithm, radix_sort, arr.copy())
            }

            times = {}
            for algorithm, future in futures.items():
                elapsed_time = future.result()
                times[algorithm] = elapsed_time

            sorted_algorithms = sorted(times.items(), key=lambda x: x[1])

            result_text_widget.insert(tk.END, "\nSorting methods and their completion times (quickest to slowest):\n")
            for algorithm, elapsed_time in sorted_algorithms:
                result_text_widget.insert(tk.END, f"{algorithm} took {elapsed_time:.6f} seconds.\n")

            sorted_arr = merge_sort(arr.copy())
            result_text_widget.insert(tk.END, f"\nSorted Array: {sorted_arr}\n")
            # Call the plot_times function and pass the parent frame (e.g., 'canvas_frame')
            plot_times(times, canvas_frame)
    else:
        result_text_widget.insert(tk.END, "Invalid choice. Please select a valid option.\n")



# Now, inside your functions, you can use `grid()` to show the appropriate widgets
def on_input_choice(event=None):
    user_input_choice = input_choice_entry.get()

    if user_input_choice == '1':
        # Show widgets for custom array input
        input_array_label.grid(row=8, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        input_array_entry.grid(row=9, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        # Hide random array widgets
        array_size_label.grid_forget()
        array_size_entry.grid_forget()
        array_range_label.grid_forget()
        array_range_entry.grid_forget()

    elif user_input_choice == '2':
        # Show widgets for random array generation
        array_size_label.grid(row=8, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        array_size_entry.grid(row=9, column=0, columnspan=3, padx=10, pady=5)
        array_range_label.grid(row=10, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        array_range_entry.grid(row=11, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        # Hide custom array widgets
        input_array_label.grid_forget()
        input_array_entry.grid_forget()

    else:
        result_text_widget.insert(tk.END, "Please choose either 1 or 2.\n")


# Define choice, arr, and result_text_widget at a higher scope (outside of functions)
choice = None
arr = []
result_text_widget = None  # You'll define this in the UI

def on_sort():
    global choice, arr, result_text_widget  # Declare these as global inside the function

    # Retrieve the user's choice for sorting algorithm
    choice = choice_entry.get()

    # Validate user input (check if it's a valid number between 1 and 6)
    if choice in ['1', '2', '3', '4', '5', '6']:
        try:
            choice = int(choice)  # Convert choice to an integer

            # Show input choice related widgets
            input_choice_label.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
            input_choice_entry.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
            input_choice_button.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

            # Assuming arr is already populated at this point or will be from input
            arr = []  # Ensure arr is set to the correct array (either user input or random)


        except ValueError:
            result_text_widget.insert(tk.END, "Invalid input. Please enter a number between 1 and 6.\n")

    else:
        result_text_widget.insert(tk.END, "Please enter a valid number between 1 and 6.\n")

def on_reset():
    # Reset inputs and results
    choice_entry.delete(0, tk.END)  # Clear the text in choice_entry
    input_choice_entry.delete(0, tk.END)
    input_array_entry.delete(0, tk.END)
    array_size_entry.delete(0, tk.END)
    array_range_entry.delete(0, tk.END)
    result_text_widget.delete(1.0, tk.END)

    # Show only the initial widgets again
    choice_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
    choice_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
    sort_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
    new_button.config(state="disabled")  # Enable the "Sort Array" button

    # Hide other widgets
    input_choice_label.grid_forget()
    input_choice_entry.grid_forget()
    input_choice_button.grid_forget()

    # Hide array input widgets
    input_array_label.grid_forget()
    input_array_entry.grid_forget()
    array_size_label.grid_forget()
    array_size_entry.grid_forget()
    array_range_label.grid_forget()
    array_range_entry.grid_forget()

    # Destroy the widgets inside the canvas_frame (which contains the plot)
    for widget in canvas_frame.winfo_children():
        widget.destroy()


def handle_array_generation():
    """
    Handles both user-provided and automatically generated arrays.
    If the user has entered a custom array, use that; otherwise, generate a random array.
    """
    global arr  # Make sure arr is accessible and modified globally

    user_array = input_array_entry.get().strip()
    if user_array:
        try:
            arr = list(map(int, user_array.split()))
            result_text_widget.insert(tk.END, f"Custom Array: {arr}\n")
            new_button.config(state=tk.NORMAL)  # Enable the "Sort Array" button
        except ValueError:
            result_text_widget.insert(tk.END, "Invalid array format. Please enter numbers separated by spaces.\n")
    else:
        size = array_size_entry.get().strip()
        range_values = array_range_entry.get().strip()
        if not size or not range_values:
            result_text_widget.insert(tk.END, "Please enter size and range values to generate a random array.\n")
            return

        try:
            size = int(size)
            min_val, max_val = map(int, range_values.split())
            if size <= 0 or min_val >= max_val:
                result_text_widget.insert(tk.END, "Invalid size or range values.\n")
                return

            arr = [random.randint(min_val, max_val) for _ in range(size)]
            result_text_widget.insert(tk.END, f"Generated Array: {arr}\n")
            new_button.config(state=tk.NORMAL)  # Enable the "Sort Array" button
        except ValueError:
            result_text_widget.insert(tk.END, "Invalid size or range format. Ensure size is an integer and range is two numbers.\n")

# Widgets for main input (initial setup)
choice_label = tk.Label(root,text="Choose a sorting algorithm:\n1. MergeSort\n2. HeapSort\n3. QuickSort\n4. Insertion Sort\n5. Radix Sort\n6. All")
choice_entry = tk.Entry(root)
sort_button = tk.Button(root, text="Next", command=on_sort)


# Widgets for array input options (initial setup)
input_choice_label = tk.Label(root, text="Do you want to (1) input your own array or (2) generate a random array?")
input_choice_entry = tk.Entry(root)
input_choice_button = tk.Button(root, text="Proceed", command=on_input_choice, state="active")

# Create a frame to hold the Reset and Generate buttons
button_frame = tk.Frame(root)
button_frame.grid(row=12, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

# Configure columns of button_frame to expand equally, ensuring even distribution
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Add buttons to the frame
reset_button = tk.Button(button_frame, text="Reset", command=on_reset)
reset_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

generated_array_button = tk.Button(button_frame, text="Generate Array", command=handle_array_generation)
generated_array_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Update the "Sort Array" button to start as disabled
new_button = tk.Button(button_frame, text="Sort Array", command=lambda: sort_choice(choice, arr, result_text_widget), state=tk.DISABLED)
new_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")  # Place it in the grid

# Widgets for custom array input (initial setup)
input_array_label = tk.Label(root, text="Enter your array (space-separated):")
input_array_entry = tk.Entry(root)

# Widgets for generating a random array (initial setup)
array_size_label = tk.Label(root, text="Enter the array size:")
array_size_entry = tk.Entry(root)

array_range_label = tk.Label(root, text="Enter the minimum and maximum values (separated by space):")
array_range_entry = tk.Entry(root)

# When the program starts, you can show the initial widgets like:
choice_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
choice_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
sort_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

# Make sure columns 0, 1, and 2 expand to center the widgets
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Result output widget (Text widget for displaying results)
result_text_widget = tk.Text(root, height=20, width=60)
result_text_widget.grid(row=13, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

# Create the scrollbar for the text widget (placed on the right side)
scrollbar = tk.Scrollbar(root, orient="vertical", command=result_text_widget.yview)
scrollbar.grid(row=13, column=2, sticky="ns", padx=10, pady=10)  # Placed on the right side

# Configure the Text widget to update the scrollbar when it scrolls
result_text_widget.config(yscrollcommand=scrollbar.set)

# Optionally, allow the grid to expand as needed for the text widget
root.grid_rowconfigure(13, weight=1)
root.grid_columnconfigure(0, weight=1)  # Allow the result_text_widget column to expand
root.grid_columnconfigure(1, weight=0)  # Keep the middle column fixed
root.grid_columnconfigure(2, weight=0)  # Keep the scrollbar column fixed

# Create a frame to hold the plot (canvas_frame)
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=14, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)  # Use grid to make the frame stretchable

# Inside canvas_frame, add the plot (plot_frame)
plot_frame = tk.Frame(canvas_frame)  # Make a new frame to contain the plot
plot_frame.grid(row=0, column=0, sticky="nsew")  # Position plot inside this frame

# Allow the result widget's row and column to grow and adjust canvas_frame as well
root.grid_rowconfigure(13, weight=1)
root.grid_rowconfigure(14, weight=3)  # Adjust weight for the plot frame to allow more space
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)

root.mainloop()
