import matplotlib.pyplot as plt

topics = ["one", "two", "three", "four", "five"]
value_a = [35, 80, 84, 83, 50]
value_b = [73, 80, 77, 40, 86]

def create_x(t, w, n, d):
    return [t * x + w * n for x in range(d)]

value_a_x = create_x(2, 0.8, 1, 5)
value_b_x = create_x(2, 0.8, 2, 5)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(value_a_x, value_a)
ax.bar(value_b_x, value_b)
middle_x = [(a + b) / 2
            for a, b in zip(value_a_x, value_b_x)]
ax.set_xticks(middle_x)
ax.set_xticklabels(topics)
fig.tight_layout()
plt.show()
