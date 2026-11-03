import numpy as np
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

ax_cht1.clear()
np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(20) * 50
ax_cht1.scatter(x, y, c="red", alpha=0.5, label="random")
ax_cht1.set_xlabel("X축 제목" if font_name else "X axis")
ax_cht1.set_ylabel("Y축 제목" if font_name else "Y axis")
ax_cht1.legend(loc="upper left")
ax_cht1.set_title("random")
