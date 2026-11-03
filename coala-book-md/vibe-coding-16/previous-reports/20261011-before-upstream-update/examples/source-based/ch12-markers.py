import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, "ro", clip_on=False)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("hello")
ax.text(3, 5, "12/19")
ax.axis([0, 10, 0, 25])
fig.tight_layout()
plt.show()
