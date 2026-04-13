from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.charts import render_donut_pair, render_mini_bar_chart
from app.components.filters import render_segmented_filter


def mesures_page() -> None:
    def content() -> None:
        render_segmented_filter(['Jour', 'Semaine', 'Mois'], active='Jour')
        render_donut_pair('GAZ', 64, 'Electricité', 90)
        render_mini_bar_chart()

    dashboard_layout(title='Mesures', content=content, show_back=True)