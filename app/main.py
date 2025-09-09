# main.py
import flet as ft
from assets import styles as S
from ui import HomeView, HourlyView, HistoricalView, CompareView

def main(page: ft.Page):
    # Window / theme
    page.title = "Air Quality Index Analyzer"
    page.bgcolor = S.BG
    page.theme_mode = "dark"
    page.window_width = 430
    page.window_height = 860
    page.padding = 0

    # Content container (we switch views inside this)
    content = ft.Container(expand=True)

    # Instantiate views (UI-only, static data)
    home = HomeView(page, city="Gandhinagar, Gujarat", aqi_value=74, status="Poor").build()
    hourly = HourlyView(page).build()
    historical = HistoricalView(page).build()
    compare = CompareView(page).build()

    def show(index: int):
        if index == 0:
            content.content = home
        elif index == 1:
            content.content = hourly
        elif index == 2:
            content.content = historical
        else:
            content.content = compare
        page.update()

    # Bottom navigation (desktop app window)
    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ACCESS_TIME, label="Hourly"),
            ft.NavigationBarDestination(icon=ft.Icons.INSIGHTS, label="History"),
            ft.NavigationBarDestination(icon=ft.Icons.COMPARE_ARROWS, label="Compare"),
        ],
        selected_index=0,
        on_change=lambda e: show(e.control.selected_index),
    )

    # Initial view
    show(0)
    page.add(content, nav)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
