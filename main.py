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

    if not os.path.exists("assets"):
        os.makedirs("assets")

    def route_change(route):
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

    def close_dlg(e):
        confirm_dlg.open = False
        page.update()

    def trigger_real_download(e):
        platform = selected_software_target.value
        confirm_dlg.open = False
        page.update()
        
        # En iPhone (iOS) Apple bloquea descargas directas de .ipa; mostramos la instalación PWA fluida
        if platform == "iOS":
            dlg_ios = ft.AlertDialog(
                title=ft.Text("Instalar en tu iPhone", color=ft.colors.CYAN_ACCENT, weight=ft.FontWeight.BOLD),
                content=ft.Text(
                    "Por seguridad de iOS, los iPhone instalan la app directo desde el navegador:\n\n"
                    "1. Toca el botón 'Compartir' (cuadrado con flecha hacia arriba) abajo en Safari.\n"
                    "2. Selecciona 'Agregar a inicio'.\n\n"
                    "¡Así tendrás RoomScan AR como app nativa en tu pantalla principal!",
                    color=ft.colors.WHITE,
                    size=13
                ),
                actions=[ft.ElevatedButton("¡Entendido!", on_click=lambda _: close_ios_dlg(dlg_ios), bgcolor=ft.colors.CYAN_ACCENT, color=ft.colors.BLACK)],
                bgcolor="#111827"
            )
            page.dialog = dlg_ios
            dlg_ios.open = True
            page.update()
            return

        # Para Android, Windows y macOS
        ext_map = {
            "Android": "roomscan_ar_installer.apk",
            "Windows": "roomscan_ar_installer.exe",
            "macOS": "roomscan_ar_installer.dmg",
            "Web PWA": "roomscan_ar_web.zip"
        }
        filename = ext_map.get(platform, "roomscan_installer.bin")
        file_path = os.path.join("assets", filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"INSTALADOR OFICIAL DE ROOMSCAN AR PARA {platform.upper()}\nEstado: Software Listo.")

        page.launch_url(f"/{filename}")

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Descargando {filename}...", color=ft.colors.WHITE),
            bgcolor=ft.colors.GREEN_700
        )
        page.snack_bar.open = True
        page.update()

    def close_ios_dlg(dlg):
        dlg.open = False
        page.update()

    confirm_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Descarga de Software", color=ft.colors.CYAN_ACCENT),
        content=ft.Text("¿Estás seguro de que deseas descargar el instalador oficial?"),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dlg),
            ft.ElevatedButton("Sí, Continuar", on_click=trigger_real_download, bgcolor=ft.colors.CYAN_400, color=ft.colors.BLACK),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#111827"
    )

    def handle_download_selection(e):
        platform = e.control.data
        selected_software_target.value = platform
        confirm_dlg.content = ft.Text(f"¿Deseas obtener RoomScan AR para {platform}?")
        page.dialog = confirm_dlg
        confirm_dlg.open = True
        page.update()

    def abrir_perfil_modal(e):
        email = page.session.get("usuario_activo") or "invitado@roomscan.ar"
        nombre = page.session.get("usuario_nombre") or "Usuario Registrado"
        metodo = page.session.get("usuario_metodo") or "Autenticación Local"

        def cerrar_perfil(ev):
            profile_dlg.open = False
            page.update()

        def logout(ev):
            profile_dlg.open = False
            page.session.clear()
            page.go("/")

        profile_dlg = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.icons.ACCOUNT_CIRCLE, color=ft.colors.CYAN_ACCENT, size=30),
                ft.Text("Perfil del Usuario", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Column([
                ft.ListTile(leading=ft.Icon(ft.icons.PERSON), title=ft.Text(nombre, color=ft.colors.WHITE), subtitle=ft.Text("Nombre del Operador", size=11, color=ft.colors.GREY_400)),
                ft.ListTile(leading=ft.Icon(ft.icons.EMAIL), title=ft.Text(email, color=ft.colors.WHITE), subtitle=ft.Text("Correo Electrónico", size=11, color=ft.colors.GREY_400)),
                ft.ListTile(leading=ft.Icon(ft.icons.VERIFIED_USER), title=ft.Text(metodo, color=ft.colors.CYAN_ACCENT), subtitle=ft.Text("Método de Autenticación", size=11, color=ft.colors.GREY_400)),
            ], height=210, spacing=5),
            actions=[
                ft.ElevatedButton("Cerrar Sesión", icon=ft.icons.LOGOUT, bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, on_click=logout),
                ft.TextButton("Cerrar", on_click=cerrar_perfil)
            ],
            bgcolor="#111827"
        )
        page.dialog = profile_dlg
        profile_dlg.open = True
        page.update()

    download_menu = ft.PopupMenuButton(
        icon=ft.icons.DOWNLOAD,
        icon_color=ft.colors.CYAN_ACCENT,
        tooltip="Descargar Software Multiplataforma",
        items=[
            ft.PopupMenuItem(text="Android (.apk)", icon=ft.icons.ANDROID, on_click=handle_download_selection, data="Android"),
            ft.PopupMenuItem(text="iOS / iPhone", icon=ft.icons.APPLE, on_click=handle_download_selection, data="iOS"),
            ft.PopupMenuItem(text="Windows (.exe)", icon=ft.icons.WINDOW, on_click=handle_download_selection, data="Windows"),
            ft.PopupMenuItem(text="macOS (.app)", icon=ft.icons.LAPTOP_MAC, on_click=handle_download_selection, data="macOS"),
            ft.PopupMenuItem(text="Web PWA / Cloud", icon=ft.icons.WEB, on_click=handle_download_selection, data="Web PWA"),
        ]
    )

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
                    download_menu,
                    ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, icon_color=ft.colors.CYAN_ACCENT, tooltip="Perfil de Usuario", on_click=abrir_perfil_modal)
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