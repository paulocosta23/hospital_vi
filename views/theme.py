import customtkinter as ctk
from typing import Optional

LIGHT = "Light"
DARK = "Dark"
DEFAULT_MODE = DARK

COLOR_THEME = {
    LIGHT: {
        "menu_text": "#FFFFFF",
        "bg": "#F8FAFC",
        "panel": "#E2E8F0",
        "surface": "#FFFFFF",
        "surface_alt": "#F1F5F9",
        "surface_dark": "#E2E8F0",
        "sidebar": "#E2E8F0",
        "topbar": "#DBEAFE",
        "card": "#FFFFFF",
        "border": "#CBD5E1",
        "text": "#0F172A",
        "text_secondary": "#475569",
        "text_muted": "#6B7280",
        "accent": "#2563EB",
        "accent_hover": "#1D4ED8",
        "button": "#2563EB",
        "button_hover": "#1D4ED8",
        "success": "#16A34A",
        "success_hover": "#15803D",
        "danger": "#DC2626",
        "info": "#0EA5E9",
        "purple": "#8B5CF6",
        "login_bg": "#DBEAFE",
        "login_circle1": "#60A5FA",
        "login_circle2": "#3B82F6",
        "login_left": "#0F172A",
        "login_left_inner": "#111827",
        "login_icon": "#0EA5E9",
        "login_divider": "#3B82F6",
        "login_subtitle": "#1E293B",
        "login_right": "#E0F2FE",
        "login_decor_top": "#93C5FD",
        "login_decor_bottom": "#60A5FA",
        "login_card": "#FFFFFF",
        "login_card_text": "#0F172A",
        "login_card_subtitle": "#475569",
    },
    DARK: {
        "menu_text": "#FCF8F8",
        "bg": "#0F172A",
        "panel": "#1E293B",
        "surface": "#111827",
        "surface_alt": "#111827",
        "surface_dark": "#1E293B",
        "sidebar": "#081B49",
        "topbar": "#243F91",
        "card": "#111827",
        "border": "#475569",
        "text": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
        "accent": "#2246BA",
        "accent_hover": "#1D4ED8",
        "button": "#2EC7E6",
        "button_hover": "#1D4ED8",
        "success": "#34D399",
        "success_hover": "#059669",
        "danger": "#F87171",
        "info": "#0EA5E9",
        "purple": "#A855F7",
        "login_bg": "#1E3A8A",
        "login_circle1": "#3B82F6",
        "login_circle2": "#2563EB",
        "login_left": "#0F172A",
        "login_left_inner": "#111827",
        "login_icon": "#22D3EE",
        "login_divider": "#22D3EE",
        "login_subtitle": "#BAE6FD",
        "login_right": "#0E3A5F",
        "login_decor_top": "#1E6FAB",
        "login_decor_bottom": "#2563EB",
        "login_card": "#FFFFFF",
        "login_card_text": "#1F2937",
        "login_card_subtitle": "#6B7280",
    },
}


def set_theme_mode(mode: str = DEFAULT_MODE):
    ctk.set_appearance_mode(mode)


def get_color(name: str, mode: Optional[str] = None) -> str:
    if mode is None:
        mode = ctk.get_appearance_mode()
    mode = mode.capitalize()
    return COLOR_THEME.get(mode, COLOR_THEME[DEFAULT_MODE]).get(
        name, COLOR_THEME[DEFAULT_MODE]["text"]
    )