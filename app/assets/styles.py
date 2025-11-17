import flet as ft
from typing import Union

# ===== Professional AQI Theme - Environmental Monitoring =====
BG = "#0A0E27"
BG_SECONDARY = "#121729"
CARD = "#1A1F3A"
CARD_ELEVATED = "#232947"
CARD_SOFT = "#2A3150"
SURFACE = "#161B33"

# Text colors
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B8C1EC"
TEXT_MUTED = "#8B93B8"
TEXT_DISABLED = "#5A6280"

# AQI Status Colors (Indian Standards)
AQI_GOOD = "#10B981"
AQI_SATISFACTORY = "#3B82F6"
AQI_MODERATE = "#F59E0B"
AQI_POOR = "#EF4444"
AQI_VERY_POOR = "#991B1B"
AQI_SEVERE = "#7F1D1D"

# Accent colors
PRIMARY = "#6366F1"
PRIMARY_LIGHT = "#818CF8"
PRIMARY_DARK = "#4F46E5"
ACCENT = "#06B6D4"
ACCENT_LIGHT = "#22D3EE"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"
INFO = "#3B82F6"

# Gradients
GRADIENT_PRIMARY = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#6366F1", "#8B5CF6"]
)

GRADIENT_AQI_GOOD = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#10B981", "#059669"]
)

GRADIENT_AQI_MODERATE = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    # Use a blue-teal gradient to better match the app's primary theme
    colors=["#06B6D4", "#6366F1"]
)

GRADIENT_AQI_POOR = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    # Use a deeper blue / indigo gradient (still noticeable but complementary)
    colors=["#4F46E5", "#0EA5E9"]
)

GRADIENT_DARK = ft.LinearGradient(
    begin=ft.alignment.top_center,
    end=ft.alignment.bottom_center,
    colors=[BG_SECONDARY, BG]
)

GRADIENT_ACCENT = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#06B6D4", "#0891B2"]
)

# Typography
TITLE = ft.TextStyle(size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
H1 = ft.TextStyle(size=48, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
H2 = ft.TextStyle(size=24, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY)
H3 = ft.TextStyle(size=20, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY)
H4 = ft.TextStyle(size=18, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY)
BODY = ft.TextStyle(size=16, color=TEXT_SECONDARY)
BODY_LARGE = ft.TextStyle(size=18, color=TEXT_SECONDARY)
CAPTION = ft.TextStyle(size=14, color=TEXT_MUTED)
SMALL = ft.TextStyle(size=12, color=TEXT_MUTED)

# Component Styles
RADIUS = 16
RADIUS_SMALL = 8
RADIUS_LARGE = 24
RADIUS_FULL = 9999

SHADOW = ft.BoxShadow(
    spread_radius=0,
    blur_radius=24,
    color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
    offset=ft.Offset(0, 8),
)

SHADOW_ELEVATED = ft.BoxShadow(
    spread_radius=0,
    blur_radius=40,
    color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
    offset=ft.Offset(0, 12),
)

SHADOW_GLOW = ft.BoxShadow(
    spread_radius=2,
    blur_radius=30,
    color=ft.Colors.with_opacity(0.3, PRIMARY),
    offset=ft.Offset(0, 0),
)

# Helper Functions
def card(content: ft.Control,
         padding: Union[int, float] = 20,
         bgcolor: str = CARD,
         radius: int = RADIUS,
         expand: bool = False,
         elevated: bool = False) -> ft.Container:
    """Professional card component"""
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        padding=padding,
        border_radius=radius,
        expand=expand,
        shadow=SHADOW_ELEVATED if elevated else SHADOW,
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, TEXT_PRIMARY))
    )

def gradient_card(content: ft.Control,
                  gradient,
                  padding: Union[int, float] = 20,
                  radius: int = RADIUS,
                  expand: bool = False) -> ft.Container:
    """Gradient card for highlighted content"""
    return ft.Container(
        content=content,
        gradient=gradient,
        padding=padding,
        border_radius=radius,
        expand=expand,
        shadow=SHADOW_GLOW
    )

def glass_card(content: ft.Control,
               padding: Union[int, float] = 20,
               radius: int = RADIUS,
               expand: bool = False) -> ft.Container:
    """Glassmorphism card effect"""
    return ft.Container(
        content=content,
        bgcolor=ft.Colors.with_opacity(0.1, TEXT_PRIMARY),
        padding=padding,
        border_radius=radius,
        expand=expand,
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, TEXT_PRIMARY))
    )

def aqi_badge(label: str, aqi_value: int) -> ft.Container:
    """AQI status badge with proper color"""
    if aqi_value <= 50:
        color = AQI_GOOD
    elif aqi_value <= 100:
        color = AQI_SATISFACTORY
    elif aqi_value <= 200:
        color = AQI_MODERATE
    elif aqi_value <= 300:
        color = AQI_POOR
    elif aqi_value <= 400:
        color = AQI_VERY_POOR
    else:
        color = AQI_SEVERE
    
    return ft.Container(
        content=ft.Text(label, style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
        bgcolor=color,
        padding=ft.padding.symmetric(8, 16),
        border_radius=RADIUS_FULL,
    )

def metric_card(title: str, value: str, icon: str, color: str = PRIMARY) -> ft.Container:
    """Metric display card"""
    return card(
        ft.Column([
            ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Text(title, style=CAPTION)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=8),
            ft.Text(value, style=H2),
        ], spacing=4),
        padding=16,
    )

def get_aqi_gradient(aqi_value: int):
    """Get gradient based on AQI value"""
    if aqi_value <= 50:
        return GRADIENT_AQI_GOOD
    elif aqi_value <= 200:
        return GRADIENT_AQI_MODERATE
    else:
        return GRADIENT_AQI_POOR

def get_aqi_color(aqi_value: int) -> str:
    """Get color based on AQI value"""
    if aqi_value <= 50:
        return AQI_GOOD
    elif aqi_value <= 100:
        return AQI_SATISFACTORY
    elif aqi_value <= 200:
        return AQI_MODERATE
    elif aqi_value <= 300:
        return AQI_POOR
    elif aqi_value <= 400:
        return AQI_VERY_POOR
    else:
        return AQI_SEVERE