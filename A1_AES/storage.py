import os

def store_encrypted_data(file_name, encrypted_data):
    with open(file_name, 'w') as file:
        file.write(encrypted_data)

def read_encrypted_data(file_name):
    with open(file_name, 'r') as file:
        return file.read()
