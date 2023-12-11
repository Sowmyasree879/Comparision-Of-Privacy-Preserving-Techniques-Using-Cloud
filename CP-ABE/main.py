from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import os
import psutil
import matplotlib.pyplot as plt

# Function to encrypt data using AES
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt data using AES
def decrypt_data(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return decrypted_data.decode('utf-8')

# Number of test cases
num_test_cases = 1000

# Open the input file for reading
with open("input.txt", "r") as input_file:
    # Read the input data from the file
    input_data = input_file.read().strip()

# Lists to store data for plotting
test_case_numbers = list(range(1, num_test_cases + 1))
accuracy_values = []
computation_time_values = []

correct_decryption_count = 0

# Measure start time
start_time = time.time()

for i in range(num_test_cases):
    # Generate a random key for AES encryption
    aes_key = get_random_bytes(16)

    # Encrypt the data using AES
    encrypted_data = encrypt_data(input_data, aes_key)

    # Decrypt the data using the same key
    decrypted_data = decrypt_data(encrypted_data, aes_key)

    # Check if the decryption is correct
    if decrypted_data == input_data:
        correct_decryption_count += 1

    # Calculate accuracy for each test case
    accuracy_values.append(correct_decryption_count / (i + 1))

    # Print the output to the terminal
    print(f"Test Case {i + 1}:\nOriginal Data: {input_data}\nEncrypted Data: {encrypted_data}\nDecrypted Data: {decrypted_data}\n")

    # Write the output to the file

# Measure end time
end_time = time.time()
elapsed_time = end_time - start_time

# Calculate overall accuracy
accuracy = correct_decryption_count / num_test_cases

# Print accuracy metrics and computation time
print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")
print(f"Total Computation Time: {elapsed_time:.2f} seconds")

# Write accuracy metrics and computation time to the file

# Get CPU time using psutil
cpu_time = psutil.Process(os.getpid()).cpu_times().user
print(f"CPU Time: {cpu_time:.2f} seconds")

# Write CPU time to the file

# Plotting accuracy graph
plt.figure(figsize=(10, 5))
plt.plot(test_case_numbers, accuracy_values, label='Accuracy', color='blue')
plt.xlabel('Test Case Number')
plt.ylabel('Accuracy')
plt.title('Accuracy vs Test Case Number')
plt.legend()
plt.savefig('accuracy_graph.png')
plt.show()

# Plotting computation time graph
plt.figure(figsize=(10, 5))
plt.bar(['Computation Time'], [elapsed_time], color='green')
plt.ylabel('Time (seconds)')
plt.title('Total Computation Time')
plt.savefig('computation_time_graph.png')
plt.show()

# Plotting resource utilization graph
plt.figure(figsize=(10, 5))
plt.bar(['CPU Time'], [cpu_time], color='orange')
plt.ylabel('Time (seconds)')
plt.title('CPU Time (Resource Utilization)')
plt.savefig('resource_utilization_graph.png')
plt.show()
