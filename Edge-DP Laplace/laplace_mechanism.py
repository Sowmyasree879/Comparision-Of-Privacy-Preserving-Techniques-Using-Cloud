import numpy as np

def laplace_mechanism(data, sensitivity, epsilon):
    scale = sensitivity / epsilon
    noise = np.random.laplace(scale=scale, size=len(data))
    privatized_data = data + noise
    return privatized_data
