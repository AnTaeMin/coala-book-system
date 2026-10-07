import matplotlib.pyplot as plt

values = [1, 2, 4, 8, 16, 32, 64, 128]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(len(values)), values)
ax.set_xlabel("index")
ax.set_ylabel("value")
fig.tight_layout()
plt.show()
