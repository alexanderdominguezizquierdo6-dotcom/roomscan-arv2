import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"
        
        self.content = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                ft.Text("Escaneo AR y Sensores en Vivo", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            ft.Container(
                expand=True,
                bgcolor="#111827",
                border_radius=12,
                border=ft.border.all(1, ft.colors.CYAN_900),
                padding=25,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.icons.CAMERA_ALT, size=56, color=ft.colors.CYAN_ACCENT),
                    ft.Text("Módulo de Realidad Aumentada y GPS", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text("Abre el visor optimizado para activar la cámara trasera y capturar la geolocalización satelital real.", size=12, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        text="🚀 Abrir Visor de Hardware en Vivo",
                        color=ft.colors.BLACK,
                        bgcolor=ft.colors.CYAN_ACCENT,
                        height=48,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=lambda _: self.page.launch_url("/index.html")
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ),
            ft.ElevatedButton(
                text="Continuar a Geolocalización y Registro ➔",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_400,
                height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda _: self.page.go("/geo")
            )
        ], expand=True, spacing=12)