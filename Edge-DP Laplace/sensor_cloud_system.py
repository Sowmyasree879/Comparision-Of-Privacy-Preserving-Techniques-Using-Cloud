# Import the laplace_mechanism function from the laplace_mechanism module
from laplace_mechanism import laplace_mechanism

# Class representing a Sensor Cloud System for differential privacy
class SensorCloudSystem:
    def __init__(self, sensor_data, sensitivity, epsilon):
        # Initialize the SensorCloudSystem with sensor data, sensitivity, and privacy parameter (epsilon)
        self.sensor_data = sensor_data
        self.sensitivity = sensitivity
        self.epsilon = epsilon

    def privatize_sensor_data(self):
        # Use the laplace_mechanism function to privatize the sensor data
        privatized_data = laplace_mechanism(self.sensor_data, self.sensitivity, self.epsilon)

        # Return the privatized sensor data
        return privatized_data
