# ui/hourly_view.py
import flet as ft
from assets import styles as S

class HourlyView:
    def __init__(self, page: ft.Page, city="Delhi", app_instance=None):
        self.page = page
        self.city = city
        self.app = app_instance
        self.hourly_data = []
        self._load_hourly_data()
    
    def _load_hourly_data(self):
        """Load hourly data - simulated since we have daily data"""
        if self.app and self.app.backend and self.app.backend.is_backend_available():
            try:
                # Get base data and simulate hourly variations
                base_data = self.app.backend.get_historical_aqi_data(self.city)
                base_aqi = base_data.get("aqi_value", 75)
                
                # Simulate hourly data with variations
                import random
                times = ["5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM"]
                self.hourly_data = []
                for i, time in enumerate(times):
                    variation = random.randint(-15, 15)
                    hourly_aqi = max(0, min(500, base_aqi + variation))
                    status = self._get_status_for_aqi(hourly_aqi)
                    self.hourly_data.append((time, hourly_aqi, status))
            except Exception as e:
                print(f"Error loading hourly data: {e}")
        
        # Fallback data if backend not available
        if not self.hourly_data:
            self.hourly_data = [("5 PM", 72, "Moderate"), ("6 PM", 69, "Moderate"),
                                ("7 PM", 58, "Moderate"), ("8 PM", 51, "Moderate"),
                                ("9 PM", 49, "Good"), ("10 PM", 45, "Good")]
    
    def _get_status_for_aqi(self, aqi):
        """Get status string for AQI value"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def _on_city_change(self, e):
        """Handle city selection change"""
        selected_city = e.control.value
        if selected_city and self.app:
            self.city = selected_city
            self._load_hourly_data()
            self.page.update()
    
    def _create_city_selector(self):
        """Create city selection dropdown"""
        if not self.app:
            return ft.Container()
        
        return ft.Dropdown(
            label="Select City",
            value=self.city,
            options=[ft.dropdown.Option(city) for city in self.app.available_cities],
            on_change=self._on_city_change,
            width=200,
        )

    def forecast_chip(self, time: str, aqi: int, status: str) -> ft.Container:
        color = S.GOOD if aqi <= 50 else S.MODERATE if aqi <= 100 else S.POOR
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(time, style=S.CAPTION),
                    ft.Text(str(aqi), style=S.H2),
                    S.aqi_badge(status, color),
                ],
                spacing=6,
                horizontal_alignment="center",
            ),
            padding=12,
            bgcolor=S.CARD_SOFT,
            border_radius=16,
            width=90,
        )

    def build(self) -> ft.Column:
        chips = [
            self.forecast_chip(t, a, s) for t, a, s in self.hourly_data
        ]
        track = ft.Row(chips, spacing=12, scroll="auto")

        # Backend status indicator
        backend_status = "✅ Backend Connected" if (self.app and self.app.backend and self.app.backend.is_backend_available()) else "⚠️ Using Fallback Data"
        
        # City selector
        city_selector = self._create_city_selector()
        
        details_btn = ft.Container(
            content=ft.Text("Backend Integration Active", style=S.BODY),
            bgcolor= "#99A9FF20",
            padding=ft.padding.symmetric(14, 18),
            alignment=ft.alignment.center,
            border_radius=14,
        )

        col = ft.Column(
            [
                ft.Text(f"Hourly AQI Forecast", style=S.TITLE),
                city_selector,
                ft.Text(f"City: {self.city}", style=S.H2),
                ft.Text(backend_status, style=S.CAPTION),
                S.card(ft.Column([ft.Text("Hourly forecast (Simulated from daily data)", style=S.H2),
                                  ft.Text("Updated from backend", style=S.CAPTION),
                                  track], spacing=12), padding=18),
                details_btn,
            ],
            spacing=16,
            expand=True,
            scroll="auto",
        )

        return ft.Container(
            content=ft.Column([
                col
            ],
            spacing=0,
            expand=True,
            ),
            padding=16,
            bgcolor=S.BG,
            expand=True,
        )
