# ui/historical_view.py
import flet as ft
from assets import styles as S

class HistoricalView:
    def __init__(self, page: ft.Page, city="Gandhinagar, Gujarat"):
        self.page = page
        self.city = city

    def stat(self, title: str, value: str, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, style=S.CAPTION),
                    ft.Text(value, style=S.H2, color=ft.Colors.BLACK),
                ],
                spacing=6,
            ),
            padding=16,
            bgcolor=color,
            border_radius=16,
            width=160,
        )

    def build(self) -> ft.Column:
        monthly = S.card(
            ft.Column(
                [
                    ft.Text("📊 Monthly AQI (placeholder chart)", style=S.BODY),
                    ft.Container(height=160, bgcolor=S.CARD_SOFT, border_radius=16),
                ],
                spacing=10,
            ),
            padding=18,
        )
        yearly = S.card(
            ft.Column(
                [
                    ft.Text("📈 Yearly AQI (placeholder chart)", style=S.BODY),
                    ft.Container(height=160, bgcolor=S.CARD_SOFT, border_radius=16),
                ],
                spacing=10,
            ),
            padding=18,
        )

        tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Monthly", content=monthly),
                ft.Tab(text="Yearly", content=yearly),
            ],
            selected_index=0,
            expand=1,
        )

        stats_row = ft.Row(
            [
                self.stat("Best AQI", "40", S.GOOD),
                self.stat("Worst AQI", "180", S.POOR),
                self.stat("Average", "92", S.MODERATE),
            ],
            spacing=12,
            wrap=True,
        )

        col = ft.Column(
            [
                ft.Text(self.city, style=S.TITLE),
                tabs,
                stats_row,
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
