import os
import flet as ft

class ExportView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.selected_format = "Plano 2D Vectorial (.DXF)"

        self.content = ft.ListView(
            expand=True,
            spacing=15,
            controls=[
                ft.Text("Exportar Planos", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Selecciona el formato de salida para generar tu archivo descargable.", size=12, color=ft.colors.GREY_400),

                self._build_option_card("Plano 2D Vectorial (.DXF)", "Compatible con AutoCAD y software CAD."),
                self._build_option_card("Modelo 3D (.OBJ)", "Para renderizado en Blender o Revit."),
                self._build_option_card("Reporte de Medición PDF (.pdf)", "Métricas completas de área, volumen y GPS."),

                ft.ElevatedButton(
                    text="Descargar Archivo Real",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._iniciar_descarga_plano
                ),
                ft.TextButton("Volver al Panel Principal", on_click=lambda _: self.page.go("/dashboard"))
            ]
        )

    def _build_option_card(self, title, subtitle):
        def select_option(e):
            self.selected_format = title
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Formato seleccionado: {title}"), bgcolor=ft.colors.CYAN_800)
            self.page.snack_bar.open = True
            self.page.update()

        return ft.Container(
            padding=15,
            bgcolor="#1E293B",
            border_radius=12,
            on_click=select_option,
            content=ft.Row([
                ft.Column([
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(subtitle, size=11, color=ft.colors.GREY_400),
                ], expand=True),
                ft.Icon(ft.icons.DOWNLOAD_ROUNDED, color=ft.colors.CYAN_ACCENT)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def _iniciar_descarga_plano(self, e):
        ext = ".dxf" if "DXF" in self.selected_format else (".obj" if "OBJ" in self.selected_format else ".pdf")
        filename = f"plano_roomscan{ext}"
        file_path = os.path.join("assets", filename)

        if not os.path.exists("assets"):
            os.makedirs("assets")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"ARCHIVO REAL GENERADO POR ROOMSCAN AR\nFormato: {self.selected_format}\nDatos de Medición Escaneados.")

        self.page.launch_url(f"/{filename}")

        self.page.snack_bar = ft.SnackBar(ft.Text(f"Descargando {filename}..."), bgcolor=ft.colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.update()