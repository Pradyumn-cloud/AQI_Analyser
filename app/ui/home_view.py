# ui/home_view.py
import flet as ft
from assets import styles as S
from .components import header_row, big_aqi_card, grid_metrics, horizontal_chip_cards, phantom_image_box
from .backdrops import backdrop_for_status


class HomeView:
    def __init__(self, page: ft.Page, city="Delhi", aqi_data=None, app_instance=None):
        self._page = page
        self._city = city
        self._app = app_instance
        self._aqi_data = aqi_data or {}
        self._aqi_value = self._aqi_data.get("aqi_value", 0)
        self._status = self._aqi_data.get("status", "Unknown")
        self.__backdrop = backdrop_for_status(page, self._status)
        
    def _on_city_change(self, e):
        """Handle city selection change"""
        selected_city = e.control.value
        if selected_city and self._app:
            self._app.change_city(selected_city)
    
    def _refresh_data(self, e):
        """Refresh button callback"""
        if self._app:
            self._app.load_city_data()
            self._app.refresh_current_view()
    
    def _get_health_recommendation(self):
        """Get health recommendation from backend"""
        if self._app and self._app.backend:
            try:
                return self._app.backend.get_health_recommendation(self._city)
            except Exception as e:
                print(f"Error getting health recommendation: {e}")
        return "Unable to get health recommendation"
    
    def _create_city_selector(self):
        """Create city selection dropdown"""
        if not self._app:
            return ft.Container()
        
        return ft.Dropdown(
            label="Select City",
            value=self._city,
            options=[ft.dropdown.Option(city) for city in self._app.available_cities],
            on_change=self._on_city_change,
            width=200,
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
        )

    def build(self) -> ft.Column:
        # pick color by status
        _color = S.GOOD if "good" in self._status.lower() else S.MODERATE if "moderate" in self._status.lower() or "okay" in self._status.lower() else S.POOR

        # header with animated backdrop directly under it
        _hero = S.card(
            ft.Stack(
                controls=[
                    self.__backdrop.build(),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row([
                                    ft.Text(f"AQI Monitor - {self._city}", style=S.TITLE),
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.Icons.REFRESH_OUTLINED,
                                            on_click=self._refresh_data,
                                            tooltip="Refresh AQI data",
                                            icon_color=ft.Colors.WHITE
                                        ),
                                    ], spacing=5)
                                ], alignment="spaceBetween"),
                                ft.Container(height=10),
                                self._create_city_selector(),
                            ],
                            spacing=0,
                        ),
                        padding=ft.padding.only(16, 12, 16, 0),
                    ),
                ],
                expand=True,
            ),
            padding=0,
            expand=False,
        )

        # AQI today (big card)
        _aqi_card = big_aqi_card(self._aqi_value, self._status, _color)

        # Get real pollutant data
        pollutants = self._aqi_data.get("pollutants", {})
        
        # metrics like the "Current conditions" grid with real data
        metrics_data = [
            ("AQI Value", str(self._aqi_value), None),
            ("Status", self._status, None),
            ("PM2.5", f"{pollutants.get('PM2.5', 'N/A')}", "μg/m³"),
            ("PM10", f"{pollutants.get('PM10', 'N/A')}", "μg/m³"),
            ("NO2", f"{pollutants.get('NO2', 'N/A')}", "μg/m³"),
            ("O3", f"{pollutants.get('O3', 'N/A')}", "μg/m³"),
        ]
        _conditions = grid_metrics(metrics_data)

        # activities recommendations based on real AQI
        activity_status = "Good" if self._aqi_value <= 50 else "Moderate" if self._aqi_value <= 100 else "Poor"
        activity_color = S.GOOD if self._aqi_value <= 50 else S.MODERATE if self._aqi_value <= 100 else S.POOR
        
        _activities = S.section(
            "Outdoor Activities Recommendation",
            horizontal_chip_cards([
                (ft.Icons.DIRECTIONS_RUN, "Running", activity_status),
                (ft.Icons.DIRECTIONS_WALK, "Walking", activity_status),
                (ft.Icons.SPORTS_SOCCER, "Sports", activity_status),
            ]),
        )

        # Air quality status based on real data
        aqi_risk = "Low" if self._aqi_value <= 50 else "Moderate" if self._aqi_value <= 100 else "High" if self._aqi_value <= 200 else "Very High"
        aqi_risk_color = S.GOOD if self._aqi_value <= 50 else S.MODERATE if self._aqi_value <= 100 else S.POOR
        
        _allergies = S.section(
            "Air Quality Impact",
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.AIR, size=20, color=aqi_risk_color),
                        ft.Column(
                            [
                                ft.Text("Respiratory Risk Level", style=S.BODY),
                                ft.Text(aqi_risk, style=S.CAPTION, color=aqi_risk_color),
                                ft.Text(f"Based on AQI: {self._aqi_value}", style=S.CAPTION),
                            ],
                            spacing=2
                        )
                    ],
                    spacing=8,
                    alignment="start",
                ),
                padding=14,
                bgcolor=S.CARD_SOFT,
                border_radius=16,
            ),
        )

        # Health recommendation section (from backend)
        health_rec = self._get_health_recommendation()
        _health_recommendation = S.section(
            "Health Recommendation",
            ft.Container(
                content=ft.Text(
                    health_rec,
                    style=S.BODY,
                    color=ft.Colors.WHITE,
                    text_align="left"
                ),
                padding=14,
                bgcolor=S.CARD_SOFT,
                border_radius=16,
            ),
        )

        # radar / map placeholder + action buttons row
        _map_card = phantom_image_box("AQI / Weather radar (placeholder)")
        _actions = ft.Row(
            [
                S.card(ft.Row([ft.Icon(ft.Icons.AUTO_AWESOME), ft.Text("Backend Data", style=S.BODY)], spacing=8), padding=12),
                S.card(ft.Row([ft.Icon(ft.Icons.REFRESH), ft.Text("Real-time AQI", style=S.BODY)], spacing=8), padding=12),
            ],
            alignment="spaceBetween",
        )

        _content = ft.Column(
            [
                _hero,
                ft.Container(height=10),
                _aqi_card,
                _health_recommendation,  # Add health recommendation
                S.section("Current conditions", _conditions),
                _map_card,
                _actions,
                _activities,
                _allergies,
                ft.Container(height=10),
            ],
            spacing=16,
            expand=True,
            scroll="always",
        )

        # Subtle animation is not auto-started due to lack of on_mount support in this Flet version
        return ft.Container(
            content=ft.Column([
                _content
            ],
            spacing=0,
            expand=True,
            ),
            padding=16,
            bgcolor=S.BG,
            expand=True,
        )
