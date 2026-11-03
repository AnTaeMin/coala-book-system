import numpy as np

ax_cht1.clear()
np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(20) * 50
ax_cht1.scatter(x, y, c="red", alpha=0.5, label="random")
ax_cht1.set_xlabel("X axis")
ax_cht1.set_ylabel("Y axis")
ax_cht1.legend(loc="upper left")
ax_cht1.set_title("random")
