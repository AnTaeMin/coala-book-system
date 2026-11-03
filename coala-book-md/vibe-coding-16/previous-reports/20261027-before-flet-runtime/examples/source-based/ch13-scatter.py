import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

fonts = {f.name for f in
         font_manager.fontManager.ttflist}
families = ("Malgun Gothic", "AppleGothic",
            "Noto Sans CJK KR", "Noto Sans KR",
            "NanumGothic", "Wanted Sans")
font_name = next((f for f in families
                  if f in fonts), None)
if font_name:
    plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(20) * 50
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, c="red", alpha=0.5, label="random")
ax.set_xlabel("X축 제목" if font_name else "X axis")
ax.set_ylabel("Y축 제목" if font_name else "Y axis")
ax.legend(loc="upper left")
ax.set_title("random")
fig.tight_layout()
plt.show()
