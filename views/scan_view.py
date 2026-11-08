import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"

        self.alto = 2.75
        self.ancho = 4.80
        self.largo = 3.60
        self.calcular_mediciones()

        # HTML y JS configurado para activar la CÁMARA TRASERA del celular con HTTPS
        self.camera_html = ft.Html(
            html="""
            <div style="width:100%; height:100%; position:relative; background:#000; border-radius:12px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                <video id="live-camera" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
                <div id="cam-error" style="position:absolute; color:#ff4444; font-family:sans-serif; text-align:center; padding:20px; display:none; font-size:12px;">
                    Acceso a cámara denegado. Asegúrate de usar HTTPS.
                </div>
                <script>
                    // Intentamos abrir la cámara trasera (environment)
                    navigator.mediaDevices.getUserMedia({ 
                        video: { facingMode: { exact: "environment" } }, 
                        audio: false 
                    })
                    .then(stream => {
                        document.getElementById('live-camera').srcObject = stream;
                    })
                    .catch(err => {
                        // Si el celular no tiene la cámara exacta trasera, recurrimos a cualquier cámara disponible
                        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
                        .then(stream => {
                            document.getElementById('live-camera').srcObject = stream;
                        })
                        .catch(e => {
                            console.error("Error crítico de cámara: ", e);
                            document.getElementById('cam-error').style.display = 'block';
                        });
                    });
                </script>
            </div>
            """,
            expand=True
        )

        self.viewport_container = ft.Container(
            expand=True,
            bgcolor="#111827",
            border_radius=12,
            alignment=ft.alignment.center,
            content=self.camera_html
        )

        self.content = ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text("• ESCANEO AR (CÁMARA TRASERA / LIDAR)", size=10, color=ft.colors.CYAN_ACCENT, weight=ft.FontWeight.BOLD),
                    padding=8, bgcolor="#1E293B", border_radius=6
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            self.viewport_container,

            ft.Container(
                padding=15,
                bgcolor="#1E293B",
                border_radius=12,
                content=ft.Row([
                    ft.Column([ft.Text(f"{self.area} m²", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Text("ÁREA CALCULADA", size=9, color=ft.colors.GREY_400)]),
                    ft.Column([ft.Text(f"{self.volumen} m³", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), ft.Text("VOLUMEN ESTIMADO", size=9, color=ft.colors.GREY_400)]),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ),

            ft.ElevatedButton(
                text="Capturar y Geolocalizar Inmueble",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_ACCENT,
                height=50,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda _: self.page.go("/geo")
            ),
            ft.TextButton("Volver al Inicio", on_click=lambda _: self.page.go("/dashboard"))
        ], spacing=15)

    def calcular_mediciones(self):
        self.area = round(self.ancho * self.largo, 2)
        self.volumen = round(self.area * self.alto, 2)