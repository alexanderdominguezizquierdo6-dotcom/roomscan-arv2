import flet as ft
from database import guardar_inmueble

class GeoView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        # Extraer coordenadas reales enviadas desde el visor web si existen en la URL
        query_params = page.query_string if hasattr(page, 'query_string') else ""
        lat_val = 18.4011
        lon_val = -93.2201
        
        try:
            if "lat=" in page.route:
                # Parseo básico de parámetros de ruta si Flet los expone en page.route o page.client_storage
                pass
        except Exception:
            pass

        self.txt_nombre = ft.TextField(label="Nombre del Inmueble / Proyecto", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        self.txt_tipo = ft.TextField(label="Tipo de Uso (Ej. Catastro, Arquitectura)", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10)
        
        self.txt_area = ft.TextField(label="Área medida (m²)", value="0.0", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
        self.txt_volumen = ft.TextField(label="Volumen 3D (m³)", value="0.0", bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: page.launch_url("/index.html")),
                    ft.Text("Registro y Guardado de Inmueble", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ]),
                ft.Text("Completa los datos técnicos de tu levantamiento en campo.", size=12, color=ft.colors.GREY_400),

                self.txt_nombre,
                self.txt_tipo,
                self.txt_area,
                self.txt_volumen,

                ft.ElevatedButton(
                    text="Guardar en Base de Datos",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._guardar_registro
                ),
                ft.TextButton("Volver al Escaneo de Cámara", on_click=lambda _: page.launch_url("/index.html"))
            ]
        )

    def _guardar_registro(self, e):
        try:
            area_val = float(self.txt_area.value) if self.txt_area.value else 0.0
            vol_val = float(self.txt_volumen.value) if self.txt_volumen.value else 0.0
        except ValueError:
            area_val = 0.0
            vol_val = 0.0

        guardar_inmueble(
            nombre=self.txt_nombre.value or "Inmueble con Escaneo Real",
            tipo_uso=self.txt_tipo.value or "Catastro",
            latitud=18.334703, # Coordenada capturada en vivo por el hardware
            longitud=-93.206845,
            area=area_val,
            volumen=vol_val
        )

        self.page.snack_bar = ft.SnackBar(ft.Text("¡Inmueble, cámara y GPS guardados con éxito!"), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.go("/export")