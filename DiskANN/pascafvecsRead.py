import matplotlib.pyplot as plt

throughput = [28.83,55.73,81.62,101.73,125.12,143.75,160.55,173.90,188.98,191.27,204.58,189.78,221.48,221.90,226.75,229.52,238.12,240.12,241.70,218.23,258.45,256.18,248.33]
latency = [0.034680,0.035834,0.036746,0.039255,0.039912 ,0.041669,0.043510,0.045865,0.047306,0.051935,0.053460,0.062926,0.058293,0.062286,0.065174,0.068597,0.070552 ,0.073661,0.077948,0.089952,0.112238,0.146904,0.179352]

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
plt.ylabel('Latency (second)')
plt.title('Throughput vs Latency (Duration 60 s)')
plt.legend()

plt.grid(True)
plt.show()
