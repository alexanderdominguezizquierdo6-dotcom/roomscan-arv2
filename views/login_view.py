import sqlite3
import flet as ft
from database import DB_NAME

class LoginView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 30
        self.alignment = ft.alignment.center
        self.bgcolor = "#0B0F19"

        self.email_input = ft.TextField(
            label="Correo electrónico o teléfono",
            prefix_icon=ft.icons.EMAIL,
            bgcolor="#1E293B",
            color=ft.colors.WHITE,
            border_color=ft.colors.CYAN_700,
            border_radius=10
        )
        self.pass_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK,
            bgcolor="#1E293B",
            color=ft.colors.WHITE,
            border_color=ft.colors.CYAN_700,
            border_radius=10
        )

        self.content = ft.Container(
            width=420,
            padding=30,
            bgcolor="#111827",
            border_radius=16,
            border=ft.border.all(1, ft.colors.CYAN_900),
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.VIEW_IN_AR, color=ft.colors.CYAN_ACCENT, size=36),
                    ft.Text("RoomScan AR", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Plataforma de Mapeo y Medición Espacial", size=12, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                
                self.email_input,
                self.pass_input,
                
                ft.ElevatedButton(
                    text="Iniciar Sesión",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=45,
                    width=420,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=self._login_email
                ),

                ft.Divider(height=15, color=ft.colors.GREY_800),
                ft.Text("O continúa con proveedores oficiales:", size=11, color=ft.colors.GREY_500, text_align=ft.TextAlign.CENTER),

                ft.ElevatedButton(
                    text="Continuar con Google",
                    icon=ft.icons.G_MOBILEDATA,
                    color=ft.colors.WHITE,
                    bgcolor="#DB4437",
                    height=42,
                    width=420,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self._login_con_proveedor("https://accounts.google.com/ServiceLogin", "Google")
                ),

                ft.ElevatedButton(
                    text="Continuar con Apple",
                    icon=ft.icons.APPLE,
                    color=ft.colors.WHITE,
                    bgcolor="#000000",
                    height=42,
                    width=420,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self._login_con_proveedor("https://appleid.apple.com/sign-in", "Apple")
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14)
        )

    def _login_email(self, e):
        if not self.email_input.value or "@" not in self.email_input.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Ingresa un correo electrónico válido."), bgcolor=ft.colors.RED_700)
            self.page.snack_bar.open = True
            self.page.update()
            return
        nombre = self.email_input.value.split('@')[0].capitalize()
        self._registrar_y_entrar(self.email_input.value, nombre, "Email Directo")

    def _login_con_proveedor(self, url, proveedor):
        self.page.launch_url(url)
        
        correo = f"usuario.{proveedor.lower()}@gmail.com" if proveedor == "Google" else f"usuario.{proveedor.lower()}@icloud.com"
        nombre = f"Operador {proveedor}"
        
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Redirigiendo al login de {proveedor}..."), 
            bgcolor=ft.colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        self._registrar_y_entrar(correo, nombre, f"OAuth {proveedor}")

    def _registrar_y_entrar(self, email, nombre, metodo):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO usuarios (email, nombre, metodo_login) VALUES (?, ?, ?)", 
                       (email, nombre, metodo))
        conn.commit()
        conn.close()
        
        # Guardado doble (client_storage y session) para garantizar persistencia absoluta al usar hardware externo
        self.page.client_storage.set("usuario_activo", email)
        self.page.client_storage.set("usuario_nombre", nombre)
        self.page.client_storage.set("usuario_metodo", metodo)
        
        self.page.session.set("usuario_activo", email)
        self.page.session.set("usuario_nombre", nombre)
        self.page.session.set("usuario_metodo", metodo)
        
        self.page.go("/dashboard")