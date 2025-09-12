# main.py
import flet as ft
from assets import styles as S
from ui import HomeView, HourlyView, HistoricalView, CompareView
from services import backend_service

class AQIApp:
    def __init__(self):
        self.current_city = "Delhi"
        self.available_cities = []
        self.aqi_data = {}
        self.backend = backend_service
        self.page = None
        self.content = None
        self.nav = None
        self.views = {}
        self.city_dropdown = None
        
    def initialize_data(self):
        """Initialize app data from backend"""
        try:
            self.available_cities = self.backend.get_available_cities()
            if self.available_cities:
                self.current_city = self.available_cities[0]
            self.load_city_data()
        except Exception as e:
            print(f"Error initializing data: {e}")
            self.available_cities = ["Delhi", "Mumbai", "Kolkata"]
            self.current_city = "Delhi"
    
    def load_city_data(self):
        """Load data for current city"""
        try:
            self.aqi_data = self.backend.get_realtime_aqi_data(self.current_city)
        except Exception as e:
            print(f"Error loading city data: {e}")
            self.aqi_data = {"city": self.current_city, "aqi_value": 0, "status": "Unknown"}
    
    def change_city(self, city_name):
        """Change current city and refresh data"""
        self.current_city = city_name
        self.load_city_data()
        self.refresh_current_view()
    
    def refresh_current_view(self):
        """Refresh the currently displayed view"""
        current_index = self.nav.selected_index if self.nav else 0
        self.create_views()
        self.show_view(current_index)
    
    def create_views(self):
        """Create all views with current data and app instance"""
        self.views = {
            "home": HomeView(
                page=self.page,
                city=self.current_city,
                aqi_data=self.aqi_data,
                app_instance=self
            ),
            "hourly": HourlyView(
                page=self.page,
                city=self.current_city,
                app_instance=self
            ),
            "historical": HistoricalView(
                page=self.page,
                city=self.current_city,
                app_instance=self
            ),
            "compare": CompareView(
                page=self.page,
                app_instance=self
            )
        }
    
    def show_view(self, index: int):
        """Show the view at the given index"""
        view_names = ["home", "hourly", "historical", "compare"]
        if 0 <= index < len(view_names):
            self.content.content = self.views[view_names[index]].build()
            self.page.update()

def main(page: ft.Page):
    # Window / theme
    page.title = "Air Quality Index Analyzer - Backend Connected"
    page.bgcolor = S.BG
    page.theme_mode = "dark"
    page.window_width = 430
    page.window_height = 860
    page.padding = 0

    # Create app instance
    app = AQIApp()
    app.page = page
    
    # Initialize data
    app.initialize_data()
    
    # Content container
    app.content = ft.Container(expand=True)
    
    # Create views
    app.create_views()
    
    # Bottom navigation
    app.nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ACCESS_TIME, label="Hourly"),
            ft.NavigationBarDestination(icon=ft.Icons.INSIGHTS, label="History"),
            ft.NavigationBarDestination(icon=ft.Icons.COMPARE_ARROWS, label="Compare"),
        ],
        selected_index=0,
        on_change=lambda e: app.show_view(e.control.selected_index),
    )
    
    # Initial view
    app.show_view(0)
    
    # Add to page
    page.add(app.content, app.nav)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
