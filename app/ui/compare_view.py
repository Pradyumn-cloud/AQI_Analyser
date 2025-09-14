# ui/compare_view.py
import flet as ft
from assets import styles as S

class CompareView(ft.View):
    def __init__(self, page: ft.Page, app_instance=None):
        super().__init__(
            route="/compare",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START
        )
        self.page = page
        self.app = app_instance
        self.available_cities = []
        self.selected_city_a = "Delhi"
        
        # Basic controls for compare view
        self.controls = [
            ft.Container(height=50),
            ft.Text("Compare Cities AQI", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("City comparison view is under construction", size=16),
            ft.Container(height=50),
            ft.ElevatedButton("Back to Home", on_click=lambda _: self.page.go("/")),
        ]
        self.selected_city_b = "Mumbai"
        self.comparison_data = None
        self.city_a_data = {}
        self.city_b_data = {}
        self._load_available_cities()
        self._load_comparison_data()
    
    def _load_available_cities(self):
        """Load available cities from app"""
        if self.app and self.app.available_cities:
            self.available_cities = self.app.available_cities
            if len(self.available_cities) >= 2:
                self.selected_city_a = self.available_cities[0]
                self.selected_city_b = self.available_cities[1]
        else:
            self.available_cities = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore"]
    
    def _load_comparison_data(self):
        """Load data for both selected cities"""
        if self.app and self.app.backend:
            try:
                self.city_a_data = self.app.backend.get_historical_aqi_data(self.selected_city_a)
                self.city_b_data = self.app.backend.get_historical_aqi_data(self.selected_city_b)
                self.comparison_data = self.app.backend.compare_cities([self.selected_city_a, self.selected_city_b])
            except Exception as e:
                print(f"Error loading comparison data: {e}")
    
    def _on_city_a_change(self, e):
        """Handle city A selection change"""
        self.selected_city_a = e.control.value
        self._load_comparison_data()
        self.page.update()
    
    def _on_city_b_change(self, e):
        """Handle city B selection change"""
        self.selected_city_b = e.control.value
        self._load_comparison_data()
        self.page.update()

    def city_card(self, city: str, aqi: int, status: str = "Unknown") -> ft.Container:
        color = S.GOOD if aqi <= 50 else S.MODERATE if aqi <= 100 else S.POOR
        return S.card(
            ft.Column(
                [
                    ft.Text(city, style=S.H2),
                    ft.Text(str(aqi), style=S.H1),
                    S.aqi_badge(status, color),
                    ft.Text(f"Backend Data", style=S.CAPTION),
                ],
                spacing=8,
            ),
            padding=18,
            expand=True,
        )

    def build(self) -> ft.Column:
        # City selection dropdowns
        pickers = ft.Row(
            [
                ft.Dropdown(
                    label="City A",
                    options=[ft.dropdown.Option(c) for c in self.available_cities],
                    value=self.selected_city_a,
                    width=200,
                    on_change=self._on_city_a_change,
                ),
                ft.Dropdown(
                    label="City B",
                    options=[ft.dropdown.Option(c) for c in self.available_cities],
                    value=self.selected_city_b,
                    width=200,
                    on_change=self._on_city_b_change,
                ),
            ],
            spacing=12,
        )

        # City comparison cards with real data
        comps = ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs":12,"md":6}, 
                    content=self.city_card(
                        self.selected_city_a, 
                        self.city_a_data.get("aqi_value", 0),
                        self.city_a_data.get("status", "Unknown")
                    )
                ),
                ft.Container(
                    col={"xs":12,"md":6}, 
                    content=self.city_card(
                        self.selected_city_b, 
                        self.city_b_data.get("aqi_value", 0),
                        self.city_b_data.get("status", "Unknown")
                    )
                ),
            ],
            spacing=12,
        )

        # Comparison analysis
        comparison_text = "No comparison data available"
        if self.comparison_data and "comparison_text" in self.comparison_data:
            comparison_text = self.comparison_data["comparison_text"]
        elif self.comparison_data and "error" in self.comparison_data:
            comparison_text = f"Error: {self.comparison_data['error']}"

        analysis_card = S.card(
            ft.Column(
                [
                    ft.Text("📊 Comparison Analysis", style=S.BODY),
                    ft.Container(
                        content=ft.Text(
                            comparison_text,
                            style=S.CAPTION,
                            selectable=True
                        ),
                        bgcolor=S.CARD_SOFT,
                        border_radius=16,
                        padding=12,
                        height=150
                    ),
                ],
                spacing=10,
            ),
            padding=18,
        )

        chart = S.card(
            ft.Column(
                [ft.Text("📉 AQI comparison (Backend Integration Active)", style=S.BODY),
                 ft.Container(height=180, bgcolor=S.CARD_SOFT, border_radius=16),
                 ft.Text("Real data loaded from CSV backend", style=S.CAPTION)],
                spacing=10,
            ),
            padding=18,
        )

        col = ft.Column(
            [ft.Text("Compare Cities", style=S.TITLE), pickers, comps, analysis_card, chart],
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
