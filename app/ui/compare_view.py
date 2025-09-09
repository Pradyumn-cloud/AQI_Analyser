# ui/compare_view.py
import flet as ft
from assets import styles as S

class CompareView:
    def __init__(self, page: ft.Page):
        self.page = page

    def city_card(self, city: str, aqi: int) -> ft.Container:
        color = S.GOOD if aqi <= 50 else S.MODERATE if aqi <= 100 else S.POOR
        return S.card(
            ft.Column(
                [
                    ft.Text(city, style=S.H2),
                    ft.Text(str(aqi), style=S.H1),
                    S.aqi_badge("Good" if color==S.GOOD else "Moderate" if color==S.MODERATE else "Poor", color),
                ],
                spacing=8,
            ),
            padding=18,
            expand=True,
        )

    def build(self) -> ft.Column:
        pickers = ft.Row(
            [
                ft.Dropdown(
                    label="City A",
                    options=[ft.dropdown.Option(c) for c in ["Delhi", "Mumbai", "Ahmedabad", "Kolkata"]],
                    value="Delhi",
                    width=200,
                ),
                ft.Dropdown(
                    label="City B",
                    options=[ft.dropdown.Option(c) for c in ["Delhi", "Mumbai", "Ahmedabad", "Kolkata"]],
                    value="Mumbai",
                    width=200,
                ),
            ],
            spacing=12,
        )

        comps = ft.ResponsiveRow(
            [
                ft.Container(col={"xs":12,"md":6}, content=self.city_card("Delhi", 120)),
                ft.Container(col={"xs":12,"md":6}, content=self.city_card("Mumbai", 80)),
            ],
            spacing=12,
        )

        chart = S.card(
            ft.Column(
                [ft.Text("📉 AQI comparison (placeholder)", style=S.BODY),
                 ft.Container(height=180, bgcolor=S.CARD_SOFT, border_radius=16)],
                spacing=10,
            ),
            padding=18,
        )

        col = ft.Column(
            [ft.Text("Compare Cities", style=S.TITLE), pickers, comps, chart],
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
