ax_cht1.clear()
x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25]
ax_cht1.plot(x, y, "ro", clip_on=False)
ax_cht1.set_xlabel("x")
ax_cht1.set_ylabel("y")
ax_cht1.set_title("hello")
ax_cht1.text(3, 5, "12/19")
ax_cht1.axis([0, 10, 0, 25])
