import SPTAGClient
import time
import time
import random
from concurrent.futures import ThreadPoolExecutor
import statistics  # Import the statistics module
import numpy as np

# connect to the server
client = SPTAGClient.AnnClient('0.0.0.0', '8000')
while not client.IsConnected():
    time.sleep(1)

k = 10
vector_dimension = 128

def measure(duration, num_clients):
    data = []

    def make_request(_):
        latencies = []  # List to store latency values
        start_time = time.time()
        end_time = start_time + duration
        while time.time() < end_time:
            q = np.random.rand(vector_dimension).astype(np.float32)
            startTimeLatency = time.time()
            response = client.Search(q, k, 'Float', False) # AnnClient.Search(query_vector, knn, data_type, with_metadata)
            endTimeLatency = time.time()
            data.append(response)
            latency_per_response = endTimeLatency - startTimeLatency
            latencies.append(latency_per_response)  # Append latency to the list
            print(f"Latency: {latency_per_response:.6f}")
        
        # Write latencies to a text file
        with open("latencies.txt", "a") as file:
            for latency in latencies:
                file.write(f"{latency:.6f}\n")
                
        return latencies  # Return latencies list for average calculation

    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        latency_lists = list(executor.map(make_request, range(num_clients)))
        print(latency_lists)
        print(f"panjang latency_lists: {len(latency_lists)}")

    total_latencies = [latency for latency_list in latency_lists for latency in latency_list]
    total_requests = len(total_latencies)
    print(f"total latencies: {len(total_latencies)}")
    print(f"total request: {total_requests}")
    average_latency = sum(total_latencies) / len(total_latencies)
    throughput = total_requests / duration
    
    # Calculate and print the standard deviation
    latency_std_dev = statistics.stdev(total_latencies)
    print(f"Standard Deviation of Latency: {latency_std_dev:.6f}")

    with open('data.txt', 'w') as file:
        for row in data:
            row_str = ' '.join(map(str, row))  # Mengonversi baris menjadi string
            file.write(row_str + " ")  # Menulis baris ke dalam file

    return throughput, average_latency

duration = 60  # Duration in seconds
num_clients = 1
throughput, average_latency = measure(duration, num_clients)
print(f"Throughput: {throughput:.2f} queries per second")
print(f"Average Latency: {average_latency:.6f} seconds")
