import threading

result = None  # Global variable to store the sum (initialize to None)

def add_numbers():
    global result
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        result = num1 + num2
    except ValueError:
        print("Invalid input. Please enter integers only.")

def print_result():
    global result
    print("waiting for result")
    while result is None:  # Wait until the sum is calculated
        pass
    print("The sum of the numbers is:", result)
    

if __name__ == "__main__":
    # Create and start the thread for adding numbers
    add_thread = threading.Thread(target=add_numbers)
    add_thread.start()

    # Create and start the thread for printing the result (waits for result)
    print_thread = threading.Thread(target=print_result)
    print_thread.start()

    # Wait for both threads to finish before exiting the main program
    add_thread.join()
    print_thread.join()

    print("Program execution completed.")
