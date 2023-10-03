import matplotlib.pyplot as plt

throughput = [1614.47,2994.25,3603.54,3859.19,5184.23,7835.76]
latency = [99.83,99.41,99.07,98.23,95.45,80.24]

# Plotting
plt.figure(figsize=(8, 6))

# Plotting lines connecting the points
plt.plot(throughput, latency, label='num_client: 1..50', color='r')

# Plotting scatter points with triangle marker
plt.scatter(throughput, latency, marker='^', color='r')

# Adding triangle markers to each point
for i in range(len(throughput)):
    plt.scatter(throughput[i], latency[i], marker='^', color='r')

# Set the axes limits to start from 0
plt.xlim(0)
plt.ylim(0)

plt.xlabel('Throughput (query/second)')
plt.ylabel('Recall (microsecond)')
plt.title('Throughput vs Recall')
plt.legend()

plt.grid(True)
plt.show()
