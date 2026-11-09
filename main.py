import os
import flet as ft
from database import init_db
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.scan_view import ScanView
from views.geo_view import GeoView
from views.export_view import ExportView
from views.settings_view import SettingsView

def main(page: ft.Page):
    init_db()

    page.title = "RoomScan AR - Mapeo y Medición Espacial"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#0B0F19"
    
    body_container = ft.Container(expand=True)
    selected_software_target = ft.Text(value="", visible=False)

    def route_change(route):
        # Si no hay sesión activa, forzar ir al login
        if page.route != "/" and not page.session.get("usuario_activo"):
            page.go("/")
            return

        if page.route == "/dashboard":
            body_container.content = DashboardView(page)
            app_bar.visible = True
        elif page.route == "/scan":
            body_container.content = ScanView(page)
            app_bar.visible = True
        elif page.route == "/geo":
            body_container.content = GeoView(page)
            app_bar.visible = True
        elif page.route == "/export":
            body_container.content = ExportView(page)
            app_bar.visible = True
        elif page.route == "/settings":
            body_container.content = SettingsView(page)
            app_bar.visible = True
        else:
            body_container.content = LoginView(page)
            app_bar.visible = False
        page.update()

    page.on_route_change = route_change

    # Barra superior de navegación unificada
    app_bar = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#111827",
        content=ft.Row(
            [
                ft.Row([
                    ft.Icon(ft.icons.VIEW_IN_AR, color=ft.colors.CYAN_ACCENT, size=28),
                    ft.Text("RoomScan AR", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ], spacing=10),
                ft.Row([
                    ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.CYAN_ACCENT, tooltip="Ajustes", on_click=lambda _: page.go("/settings")),
                    ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.CYAN_ACCENT, tooltip="Perfil", on_click=lambda _: page.go("/dashboard"))
                ], spacing=5)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    page.add(
        ft.Column([
            app_bar,
            body_container
        ], expand=True, spacing=0)
    )

    page.go("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, assets_dir="assets")