import matplotlib.pyplot as plt

a = [1, 2, 3, 4, 5]
b = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(a, b, "b-+", clip_on=False)
ax.axis([0, 10, 0, 25])
fig.tight_layout()
plt.show()
