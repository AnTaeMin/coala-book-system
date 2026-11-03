import flet as ft
import flet_charts as fch
import matplotlib.pyplot as plt


def main(page: ft.Page):
    page.title = "My App"
    page.padding = 0

    # >>> COALA FLET GUI MANAGED BLOCK START >>>
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)

    page.add(
        ft.Stack(
            controls=[
                ft.Container(content=cht1, left=20, top=20, width=300, height=240),
            ],
            width=page.width,
            height=page.height,
        )
    )
    # <<< COALA FLET GUI MANAGED BLOCK END <<<


ft.run(main)
