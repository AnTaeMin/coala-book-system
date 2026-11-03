import flet_charts as fch
import matplotlib.pyplot as plt

fig_cht1, ax_cht1 = plt.subplots()
cht1 = fch.MatplotlibChart(
    expand=True, figure=fig_cht1)
