# Importing neccesary libraries
import os
import json
import time
from app import app
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from prettytable import PrettyTable
import matplotlib.pyplot as plt

# Function to set the encryption key
def set_encryption_key(key):
    os.environ['ENCRYPTION_KEY'] = key

# Simulate the serverless function to encrypt data
def simulate_serverless_function(data_to_encrypt):
    with app.test_client() as client:
        start_time = time.time()
        response = client.post('/encrypt', json={'data': data_to_encrypt})
        end_time = time.time()
        elapsed_time = end_time - start_time
        return response, elapsed_time

# Function to decrypt the encrypted data
def decrypt_data(encrypted_data, key, iv):
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv=base64.b64decode(iv))
    decrypted_text = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size).decode('utf-8')
    return decrypted_text

# Function to process sensitive information from a JSON file
def process_sensitive_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to print the table and save output to a file
def print_and_save_table(table, data, encrypted_data, decrypted_data, output_file, pseudo_metrics):
    # Print the table in the terminal
    print(table)

    # Save the output to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"Original Data:\n{data}\n\nEncrypted Data:\n{encrypted_data}\n\nDecrypted Data:\n{decrypted_data}\n\nPseudo Metrics:\n{pseudo_metrics}")

# Function to measure accuracy, scalability, and computation time
def evaluate_performance(original_data, encrypted_data, decrypted_data, elapsed_time, file_sizes):
    accuracy = original_data == decrypted_data
    scalability = {"file_sizes": file_sizes, "encryption_times": [], "decryption_times": []}

    for size in file_sizes:
        simulated_data = "A" * size  # Simulating data of the specified size
        _, encryption_time = simulate_serverless_function(simulated_data)
        decryption_start_time = time.time()
        decrypt_data(encrypted_data, os.environ['ENCRYPTION_KEY'], response.get_json()['iv'])
        decryption_end_time = time.time()
        decryption_time = decryption_end_time - decryption_start_time

        scalability["encryption_times"].append(encryption_time)
        scalability["decryption_times"].append(decryption_time)

    return accuracy, scalability, elapsed_time

# Function to visualize performance metrics
def visualize_performance(accuracy, scalability, elapsed_time):
    # Visualization of accuracy
    plt.bar(['Accuracy'], [accuracy * 100])
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy')
    plt.ylim([0, 100])  # Set y-axis limit to 0-100 for percentage
    plt.show()

    # Visualization of scalability
    plt.plot(scalability["file_sizes"], scalability["encryption_times"], label='Encryption Time')
    plt.plot(scalability["file_sizes"], scalability["decryption_times"], label='Decryption Time')
    plt.xlabel('File Size (Bytes)')
    plt.ylabel('Time (s)')
    plt.title('Scalability')
    plt.legend()
    plt.show()

    # Visualization of elapsed time
    plt.bar(['Elapsed Time'], [elapsed_time])
    plt.ylabel('Time (s)')
    plt.title('Elapsed Time')
    plt.show()

    # Print other performance metrics
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Elapsed Time: {elapsed_time} seconds")

if __name__ == '__main__':
    # Set the encryption key
    encryption_key = 'd0a28d47da3fdce44448c19f160bc8b5d594f846f212b3889d1c71413989deea'
    set_encryption_key(encryption_key)
    print(f"Encryption Key: {encryption_key}")

    # Read sensitive data from JSON file
    sensitive_data = process_sensitive_json('smsCorpus_zh_2015.03.09.json')

    # Convert the JSON data to a string for encryption
    sensitive_data_str = json.dumps(sensitive_data)

    # Simulate using the serverless function to encrypt data
    response, elapsed_time = simulate_serverless_function(sensitive_data_str)
    
    # Process the result
    encrypted_data = response.get_json()['encrypted_data']
    iv = response.get_json()['iv']
    decrypted_data = decrypt_data(encrypted_data, encryption_key, iv)

    # Pseudo Metrics
    original_length = len(sensitive_data_str)
    encrypted_length = len(encrypted_data)
    decrypted_length = len(decrypted_data)

    pseudo_metrics = f"Original Length: {original_length}\nEncrypted Length: {encrypted_length}\nDecrypted Length: {decrypted_length}"

    # Evaluate and visualize performance metrics
    file_sizes = [1024, 2048, 4096]  # Specify file sizes for scalability testing
    accuracy, scalability, elapsed_time = evaluate_performance(sensitive_data_str, encrypted_data, decrypted_data, elapsed_time, file_sizes)
    visualize_performance(accuracy, scalability, elapsed_time)

    # Display the results in a table
    table = PrettyTable()
    table.field_names = ["Data", "Encrypted Data", "Decrypted Data"]

    # Add the row to the table
    table.add_row([sensitive_data_str[:30] + '...', encrypted_data[:30] + '...', decrypted_data[:30] + '...'])

    # Print the table in the terminal and save output to a file
    print_and_save_table(table, sensitive_data_str, encrypted_data, decrypted_data, 'output.txt', pseudo_metrics)
