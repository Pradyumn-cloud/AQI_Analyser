# ui/home_view.py
import flet as ft
from assets import styles as S
from .components import header_row, big_aqi_card, grid_metrics, horizontal_chip_cards, phantom_image_box
from .backdrops import backdrop_for_status


class HomeView:
    def __init__(self, page: ft.Page, city="Gandhinagar, Gujarat", aqi_value=74, status="Poor"):
        self._page = page
        self._city = city
        self._aqi_value = aqi_value
        self._status = status
        self.__backdrop = backdrop_for_status(page, status)

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
                                header_row(self._city, [
                                    ft.Icon(ft.Icons.ADD_LOCATION_ALT_OUTLINED),
                                    ft.Icon(ft.Icons.SETTINGS_OUTLINED),
                                    ft.Icon(ft.Icons.REFRESH_OUTLINED),
                                ]),
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

        # metrics like the "Current conditions" grid in your screenshots
        _conditions = grid_metrics([
            ("Humidity", "75%", None),
            ("Precipitation", "1 mm", None),
            ("Wind", "14.5 km/h", None),
            ("AQI", f"{self._status} ({self._aqi_value})", None),
            ("UV index", "Low", None),
            ("Pressure", "1002.0 mb", None),
        ])

        # activities / allergies
        _activities = S.section(
            "Activities",
            horizontal_chip_cards([
                (ft.Icons.DIRECTIONS_RUN, "Running", "Poor"),
                (ft.Icons.DIRECTIONS_WALK, "Jogging", "Poor"),
            ]),
        )

        _allergies = S.section(
            "Allergies",
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WATER_DROP_OUTLINED, size=20),
                        ft.Column(
                            [
                                ft.Text("Dust and dander", style=S.BODY),
                                ft.Text("Extreme", style=S.CAPTION, color=S.POOR),
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

        # radar / map placeholder + action buttons row
        _map_card = phantom_image_box("AQI / Weather radar (placeholder)")
        _actions = ft.Row(
            [
                S.card(ft.Row([ft.Icon(ft.Icons.AUTO_AWESOME), ft.Text("AccuWeather", style=S.BODY)], spacing=8), padding=12),
                S.card(ft.Row([ft.Icon(ft.Icons.RADAR), ft.Text("Weather radar", style=S.BODY)], spacing=8), padding=12),
            ],
            alignment="spaceBetween",
        )

        _content = ft.Column(
            [
                _hero,
                ft.Container(height=10),
                _aqi_card,
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
