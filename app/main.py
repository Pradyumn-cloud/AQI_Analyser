import flet as ft
from ui.home_view import HomeView
from ui.historical_view import HistoricalView
from ui.compare_view import CompareView

def main(page: ft.Page):
    """
    Main function to initialize the Flet application.
    """
    page.title = "AQI Analyser"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        """
        Handles routing between different views in the application.
        """
        page.views.clear()
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/historical":
            page.views.append(HistoricalView(page))
        elif page.route == "/compare":
            page.views.append(CompareView(page))
        page.update()

    def view_pop(view):
        """
        Handles popping a view from the stack and navigating back.
        """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")