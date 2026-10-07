import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, "b-+", clip_on=False)
ax.axis([0, 10, 0, 25])
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.tight_layout()
plt.show()
