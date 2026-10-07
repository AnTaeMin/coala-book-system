import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3, 4, 5])
ax.set_xlabel("index")
ax.set_ylabel("value")
fig.tight_layout()
plt.show()
