import matplotlib.pyplot as plt

topics = ["one", "two", "three", "four", "five"]
a = [35, 80, 84, 83, 50]
b = [73, 80, 77, 40, 86]
x = list(range(len(topics)))
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([v - 0.2 for v in x], a, 0.4, label="A")
ax.bar([v + 0.2 for v in x], b, 0.4, label="B")
ax.set_xticks(x)
ax.set_xticklabels(topics)
ax.set_ylabel("value")
ax.legend()
fig.tight_layout()
plt.show()
