import flet as ft
from database import limpiar_base_datos

class SettingsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.unit_dropdown = ft.Dropdown(
            value="Métrico (m / m²)",
            options=[
                ft.dropdown.Option("Métrico (m / m²)"),
                ft.dropdown.Option("Imperial (ft / ft²)"),
            ],
            bgcolor="#1E293B", color=ft.colors.WHITE, border_color=ft.colors.CYAN_700
        )

        self.quality_switch = ft.Switch(label="Procesamiento AR de Alta Precision", value=True, active_color=ft.colors.CYAN_ACCENT)
        self.auto_save = ft.Switch(label="Guardar capturas automaticamente en SQLite", value=True, active_color=ft.colors.CYAN_ACCENT)
        self.cam_permission = ft.Switch(label="Acceso a Cámara / Sensores Video", value=True, active_color=ft.colors.GREEN_400)
        self.gps_permission = ft.Switch(label="Acceso a Servicio de Ubicación GPS", value=True, active_color=ft.colors.GREEN_400)

        self.content = ft.ListView(
            expand=True,
            spacing=20,
            controls=[
                ft.Text("Ajustes del Sistema", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Configuración general de sensores, unidades y datos", size=12, color=ft.colors.GREY_400),

                self._build_section("UNIDADES Y MEDICIÓN", [
                    ft.Text("Sistema de Medidas", size=12, color=ft.colors.GREY_300),
                    self.unit_dropdown,
                    self.quality_switch
                ]),

                self._build_section("PERMISOS DEL DISPOSITIVO", [
                    self.cam_permission,
                    self.gps_permission
                ]),

                self._build_section("ALMACENAMIENTO Y BASE DE DATOS", [
                    self.auto_save,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        text="Restablecer Base de Datos (Borrar Escaneos)",
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED_700,
                        height=45,
                        on_click=self._confirmar_borrado
                    )
                ]),

                ft.TextButton("Volver al Panel Principal", on_click=lambda _: self.page.go("/dashboard"))
            ]
        )

    def _build_section(self, title, controls):
        return ft.Container(
            padding=15,
            bgcolor="#1E293B",
            border_radius=12,
            content=ft.Column([
                ft.Text(title, size=11, color=ft.colors.CYAN_ACCENT, weight=ft.FontWeight.BOLD),
                ft.Divider(color=ft.colors.GREY_800),
                *controls
            ], spacing=10)
        )

    def _confirmar_borrado(self, e):
        def ejecutar_limpieza(ev):
            limpiar_base_datos()
            dlg.open = False
            self.page.snack_bar = ft.SnackBar(ft.Text("Base de datos restablecida a cero."), bgcolor=ft.colors.ORANGE_800)
            self.page.snack_bar.open = True
            self.page.update()

        def cerrar(ev):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Borrado", color=ft.colors.RED_ACCENT),
            content=ft.Text("¿Estás seguro de eliminar todos los escaneos registrados?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton("Sí, Borrar", on_click=ejecutar_limpieza, bgcolor=ft.colors.RED_700, color=ft.colors.WHITE)
            ],
            bgcolor="#111827"
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()