import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_names = {font.name for font in
              font_manager.fontManager.ttflist}
for name in ("Malgun Gothic", "AppleGothic",
             "Noto Sans CJK KR", "NanumGothic"):
    if name in font_names:
        plt.rcParams["font.family"] = name
        break
else:
    raise RuntimeError("Install a Korean font, then rerun.")
plt.rcParams["axes.unicode_minus"] = False

np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(20) * 50
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, c="red", alpha=0.5, label="random")
ax.set_xlabel("X축 제목")
ax.set_ylabel("Y축 제목")
ax.legend(loc="upper left")
ax.set_title("random")
fig.tight_layout()
plt.show()
