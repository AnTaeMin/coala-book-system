import numpy as np
import matplotlib.pyplot as plt

np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(len(x)) * 50
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, c="red", alpha=0.5, label="random")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend(loc="upper left")
ax.set_title("random")
fig.tight_layout()
plt.show()
