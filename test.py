import time
import ntcore

# Initialize the NTCore network table instance
ntcore.NetworkTableInstance.startDSClient()

# Create a FloatArrayTopic with the desired name
array_topic = ntcore.FloatArrayTopic(ntcore.NetworkTableInstance.getTable("test"))

# Main loop to publish the array periodically
while True:
    try:
        # Example data: [1, 3.14, 2.718, 0.123]
        data_to_publish = [7, 1.23, 0.123, 0.0123]

        # Publish the array
        array_topic.publish().send(data_to_publish)

        print(f"Published: {data_to_publish}")

        # Wait for some time before publishing again
        time.sleep(1)

    except KeyboardInterrupt:
        # Break the loop if Ctrl+C is pressed
        break

# Clean up after the loop
nt_instance.stopDSClient()
nt_instance.stopClient()
