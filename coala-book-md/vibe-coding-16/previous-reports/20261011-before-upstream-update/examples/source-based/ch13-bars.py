import matplotlib.pyplot as plt

a = [1, 2, 4, 8, 16, 32, 64, 128]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(len(a)), a)
fig.tight_layout()
plt.show()
