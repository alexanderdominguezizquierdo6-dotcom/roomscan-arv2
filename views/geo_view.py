import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.txt_nombre = ft.TextField(value="Levantamiento Catastral AR", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        self.txt_tipo = ft.TextField(value="Catastro / Bienes Raíces", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        
        self.map_container = ft.Container(
            padding=20,
            bgcolor="#111827",
            border_radius=12,
            border=ft.border.all(1, ft.colors.CYAN_900),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.GPS_FIXED, color=ft.colors.CYAN_ACCENT, size=28),
                    ft.Text("Módulo GPS con Permiso Real", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Toca el botón de abajo para iniciar el rastreo GPS en tiempo real de tu dispositivo.", size=12, color=ft.colors.GREY_300),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.ElevatedButton(
                    text="🛰️ Activar Rastreador GPS Real",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.launch_url("/geo.html")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Text("Geolocalización Satelital Real", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Sincronización GPS con hardware del dispositivo.", size=12, color=ft.colors.GREY_400),

                self.map_container,

                ft.Text("NOMBRE DEL PROYECTO", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_nombre,

                ft.Text("TIPO DE USO", size=11, color=ft.colors.GREY_400, weight=ft.FontWeight.BOLD),
                self.txt_tipo,

                ft.ElevatedButton(
                    text="Guardar en Base de Datos",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._guardar_registro
                ),
                ft.TextButton("Volver al Escaneo", on_click=lambda _: self.page.go("/scan"))
            ]
        )

    def _guardar_registro(self, e):
        guardar_inmueble(
            nombre=self.txt_nombre.value,
            tipo_uso=self.txt_tipo.value,
            latitud=18.4011,
            longitud=-93.2201,
            area=17.28,
            volumen=47.52
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble y coordenadas guardados con éxito!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")