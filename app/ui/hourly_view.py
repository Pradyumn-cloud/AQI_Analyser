# ui/hourly_view.py
import flet as ft
from assets import styles as S

class HourlyView:
    def __init__(self, page: ft.Page, city="Unvarsad, Gujarat"):
        self.page = page
        self.city = city

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
            self.forecast_chip(t, a, s) for t, a, s in
            [("5 PM", 72, "Moderate"), ("6 PM", 69, "Moderate"),
             ("7 PM", 58, "Moderate"), ("8 PM", 51, "Moderate"),
             ("9 PM", 49, "Good"), ("10 PM", 45, "Good")]
        ]
        track = ft.Row(chips, spacing=12, scroll="auto")

        details_btn = ft.Container(
            content=ft.Text("More AQI details", style=S.BODY),
            bgcolor= "#99A9FF20",
            padding=ft.padding.symmetric(14, 18),
            alignment=ft.alignment.center,
            border_radius=14,
        )

        col = ft.Column(
            [
                ft.Text(self.city, style=S.TITLE),
                S.card(ft.Column([ft.Text("Hourly forecast", style=S.H2),
                                  ft.Text("Updated now", style=S.CAPTION),
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
