import matplotlib.pyplot as plt

x = [15, 25, 35, 45, 55]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.tight_layout()
plt.show()
