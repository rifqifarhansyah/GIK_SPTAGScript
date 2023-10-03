import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import statistics  # Import the statistics module

def measure(duration, num_clients):
    data = []

    def make_request(_):
        with open("array1.txt", "r") as array_file:
            line = array_file.readline()
        query_array = [float(x) for x in line.split()]
        # Buat list indeks acak antara 0-128000
        random_indices = random.sample(range(1280000), 128)
        # print(random_indices)
        queryIN = []
        # Ambil nilai dari array sesuai dengan indeks yang dipilih secara acak
        for i in random_indices:
            queryIN.append(query_array[i])
        # print(queryIN)

        jsonquery = {
            "Ls": 256,
            "query_id": 0,
            "query": queryIN,
            "k": 10
        }
        
        latencies = []  # List to store latency values
        start_time = time.time()
        end_time = start_time + duration
        while time.time() < end_time:
            startTimeLatency = time.time()
            response = requests.post('http://localhost:3000', json=jsonquery)
            data.append(response)
            endTimeLatency = time.time()
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

    with open('data1.txt', 'w') as file:
        for row in data:
            row_str = ' '.join(map(str, row))  # Mengonversi baris menjadi string
            file.write(row_str + "\n")  # Menulis baris ke dalam file

    return throughput, average_latency

duration = 60  # Duration in seconds
num_clients = 1
throughput, average_latency = measure(duration, num_clients)
print(f"Throughput: {throughput:.2f} queries per second")
print(f"Average Latency: {average_latency:.6f} seconds")
