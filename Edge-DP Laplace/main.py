import json
import time
import numpy as np
import matplotlib.pyplot as plt
import psutil  # for monitoring CPU usage

from sensor_cloud_system import SensorCloudSystem 

# Laplace Mechanism for differential privacy
def laplace_mechanism(data, sensitivity, epsilon):
    def add_laplace_noise(val):
        # Add Laplace noise to numerical values
        if isinstance(val, (int, float)):
            return val + np.random.laplace(0, sensitivity / epsilon)
        else:
            return val

    privatized_data = np.vectorize(add_laplace_noise)(data)
    return privatized_data.tolist()

# Compute accuracy between original and privatized data
def compute_accuracy(original, privatized, threshold=0.1):
    assert len(original) == len(privatized), "Data lengths do not match"

    correct_count = 0

    for orig_val, priv_val in zip(original, privatized):
        if isinstance(orig_val, (int, float)):
            if abs(orig_val - priv_val) <= threshold:
                correct_count += 1
        else:
            if orig_val == priv_val:
                correct_count += 1

    accuracy = correct_count / len(original) * 100
    return accuracy

# Process sensitive JSON file
def process_sensitive_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON in {file_path}.")
        return None

# Plot computation time for each test case
def plot_computation_time(test_cases, computation_times):
    plt.figure(figsize=(10, 5))
    plt.plot(test_cases, computation_times, marker='o', color='blue', label='Computation Time')
    plt.xlabel('Test Case')
    plt.ylabel('Computation Time (seconds)')
    plt.title('Computation Time for Each Test Case')
    for i, txt in enumerate(computation_times):
        plt.annotate(f'{txt:.2f} sec', (test_cases[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.legend()
    plt.show()

# Plot accuracy for each test case
def plot_accuracy(test_cases, accuracies):
    plt.figure(figsize=(10, 5))
    plt.bar(test_cases, accuracies, color=plt.cm.viridis(np.linspace(0, 1, len(test_cases))))
    plt.xlabel('Test Case')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy for Each Test Case')
    plt.show()

# Plot CPU usage for each test case
def plot_resource_utilization(test_cases, cpu_percentages):
    plt.figure(figsize=(10, 5))
    plt.plot(test_cases, cpu_percentages, marker='o', color='red', label='CPU Usage')
    plt.xlabel('Test Case')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage for Each Test Case')
    for i, txt in enumerate(cpu_percentages):
        plt.annotate(f'{txt:.2f}%', (test_cases[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.legend()
    plt.show()

# Main function
def main():
    num_test_cases = 5
    results = []

    # Load sensitive data from JSON file
    data = process_sensitive_json("data.json")
    if data is None:
        return

    test_cases = range(1, num_test_cases + 1)
    computation_times = []
    accuracies = []
    cpu_percentages = []

    for i in test_cases:
        sensor_data_i = data.copy()

        sensitivity = 1.0
        epsilon = 0.5

        # Measure computation time
        start_time = time.time()

        # Apply Laplace mechanism for differential privacy
        sensor_cloud_system = SensorCloudSystem(sensor_data_i, sensitivity, epsilon)
        privatized_data = laplace_mechanism(sensor_data_i, sensitivity, epsilon)

        end_time = time.time()
        computation_time = end_time - start_time

        # Compute accuracy between original and privatized data
        accuracy = compute_accuracy(sensor_data_i, privatized_data)

        # Record results for the current test case
        results.append({
            "original": sensor_data_i,
            "privatized": privatized_data,
            "computation_time": computation_time,
            "accuracy": accuracy
        })

        # Store computation time and accuracy for plotting
        computation_times.append(computation_time)
        accuracies.append(accuracy)

        # Monitor CPU usage
        cpu_percent = psutil.cpu_percent()
        cpu_percentages.append(cpu_percent)

        # Print results to the terminal
        print(f"Test Case {i}:")
        print("Original Sensor Data:", sensor_data_i)
        print("Privatized Sensor Data:", privatized_data)
        print("Computation Time:", computation_time, "seconds")
        print("Accuracy:", accuracy, "%")
        print("CPU Usage:", cpu_percent, "%\n")

    # Save results to a JSON file
    with open("output.txt", 'w', encoding='utf-8') as output_file:
        json.dump(results, output_file, indent=4)

    # Plot computation time, accuracy, and CPU usage
    plot_computation_time(test_cases, computation_times)
    plot_accuracy(test_cases, accuracies)
    plot_resource_utilization(test_cases, cpu_percentages)

    print("Results printed to terminal and saved to output.txt")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
