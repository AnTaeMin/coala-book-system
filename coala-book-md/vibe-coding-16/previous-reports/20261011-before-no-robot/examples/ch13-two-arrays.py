import matplotlib.pyplot as plt

a = [15, 25, 35, 45, 55]
b = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(a, b)
fig.tight_layout()
plt.show()
