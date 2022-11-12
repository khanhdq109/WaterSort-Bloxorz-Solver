from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt

time1 = [0.0464, 0.2140, 0.0700, 0.0591, 0.3280, 0.1458, 0.1424, 1.1973, 1.6775, 28.7510]
time2 = [1.5046, 49.1143, 26.1128, 122.8189, 362.2324, 350.1055, 439.2875, 20.7907, 32.22, 648.53]

mem1 = [30.1, 30.83, 30.11, 30.25, 31.22, 30.27, 30.55, 32.33, 32.19, 44.18]
mem2 = [54.55, 82.99, 78.33, 94.45, 161.20, 147.33, 195.45, 107.21, 79.98, 287.13]

plt.plot(mem1, label = 'BFS', color = 'b')
plt.plot(mem2, label = 'GA', color = 'r')
plt.legend()
plt.show()