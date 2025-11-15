import flet as ft
from ui.home_view import HomeView
from ui.compare_view import CompareView
from ui.historical_view import HistoricalView
from assets import styles as S

def main(page: ft.Page):
    # Configure page
    page.title = "AQI Monitor Pro - Professional Air Quality Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = S.BG
    page.padding = 0
    page.window.width = 1400
    page.window.height = 900
    page.window.min_width = 800
    page.window.min_height = 600
    
    # Custom theme
    page.theme = ft.Theme(
        color_scheme_seed=S.PRIMARY,
        use_material3=True,
    )
    
    # Initialize views
    def get_view(route):
        if route == "/":
            return HomeView(page)
        elif route == "/compare":
            return CompareView(page)
        elif route == "/historical":
            return HistoricalView(page)
        else:
            return HomeView(page)
    
    def route_change(e):
        """Handle route changes"""
        page.views.clear()
        page.views.append(get_view(page.route))
        page.update()
    
    def view_pop(e):
        """Handle back navigation"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Start with home view
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)