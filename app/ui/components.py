# ui/components.py
import flet as ft
from assets import styles as S

def header_row(city: str, right_controls: list[ft.Control] | None = None) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Text(city, style=S.TITLE),
            ft.Row(right_controls or [], spacing=10),
        ],
        alignment="spaceBetween",
    )

def big_aqi_card(aqi_value: int, status: str, color: str) -> ft.Container:
    return S.card(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(str(aqi_value), style=S.H1),
                        S.aqi_badge(status, color),
                    ],
                    alignment="spaceBetween",
                ),
                ft.Text(
                    "Air Quality Index (demo data)",
                    style=S.CAPTION
                ),
            ],
            spacing=10,
        ),
        padding=20,
    )

def grid_metrics(items: list[tuple[str, str, str | None]]):
    """
    items: [(title, value, hint), ...]
    """
    tiles = [S.metric(t, v, h) for t, v, h in items]
    return ft.ResponsiveRow(
        controls=[
            ft.Container(col={"xs": 12, "sm": 6, "md": 4}, content=t) for t in tiles
        ],
        run_spacing=12,
        spacing=12,
    )

def horizontal_chip_cards(pairs: list[tuple[str,str,str]]):
    """
    pairs: [(icon, title, subtitle), ...]
    """
    cards = []
    for ic, title, sub in pairs:
        cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ic, size=22),
                        ft.Column(
                            [ft.Text(title, style=S.BODY),
                             ft.Text(sub, style=S.CAPTION, color=S.POOR if "Poor" in sub else S.MODERATE)],
                            spacing=2,
                        ),
                    ],
                    alignment="start",
                    spacing=10,
                ),
                padding=16,
                bgcolor=S.CARD_SOFT,
                border_radius=16,
            )
        )
    return ft.Row(cards, spacing=12, wrap=True)

def phantom_image_box(label="Map / Radar (placeholder)") -> ft.Container:
    return S.card(
        ft.Stack(
            controls=[
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1,-1),
                        end=ft.Alignment(1,1),
                        colors=[S.CARD_SOFT, S.CARD]
                    ),
                    border_radius=S.RADIUS,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(label, style=S.CAPTION),
                    alignment=ft.alignment.center,
                )
            ],
            expand=True,
        ),
        padding=0,
        expand=True,
    )
