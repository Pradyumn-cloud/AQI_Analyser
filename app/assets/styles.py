# assets/styles.py
import flet as ft

# ===== Color system (dark, soft, readable) =====
BG = "#0D1117"                 # page background
CARD = "#1B212C"               # surface
CARD_SOFT = "#222938"
TEXT = "#E6EDF3"
SUBTLE = "#A9B3C1"
MUTED = "#7E8AA0"

GOOD = "#39D353"               # good AQI accent
MODERATE = "#F2C94C"           # okayish accent
POOR = "#FF6B6B"               # poor AQI accent
PRIMARY = "#7AA2F7"            # general accent (buttons/links)

# ===== Typography =====
TITLE = ft.TextStyle(size=26, weight="bold", color=TEXT)
H1 = ft.TextStyle(size=40, weight="bold", color=TEXT)
H2 = ft.TextStyle(size=20, weight="w600", color=TEXT)
BODY = ft.TextStyle(size=15, color=TEXT)
CAPTION = ft.TextStyle(size=13, color=SUBTLE)

# ===== Shadows & radii =====
RADIUS = 20
SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=20,
    color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
    offset=ft.Offset(0, 8),
)

def card(content: ft.Control,
         padding: int | float = 16,
         bgcolor: str = CARD,
         radius: int = RADIUS,
         expand: bool = False) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        padding=padding,
        border_radius=radius,
        expand=expand,
        shadow=SHADOW,
    )

def section(title: str, child: ft.Control) -> ft.Container:
    return card(
        ft.Column(
            controls=[
                ft.Text(title, style=H2),
                child,
            ],
            spacing=10,
        ),
        padding=18,
    )

def pill(text: str, icon: str | None = None) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=16) if icon else ft.Container(),
                ft.Text(text, style=CAPTION),
            ],
            spacing=6,
            alignment="center",
        ),
        padding=ft.padding.symmetric(8, 10),
        bgcolor=CARD_SOFT,
        border_radius=999,
    )

def metric(title: str, value: str, hint: str | None = None) -> ft.Container:
    return card(
        ft.Column(
            controls=[
                ft.Text(title, style=CAPTION),
                ft.Text(value, style=H2),
                ft.Text(hint, style=CAPTION) if hint else ft.Container(),
            ],
            spacing=4,
        ),
        padding=14,
    )

def aqi_badge(label: str, color_hex: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, style=CAPTION, color=ft.Colors.BLACK),
        bgcolor=color_hex,
        padding=ft.padding.symmetric(6, 10),
        border_radius=999,
    )
