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
                ft.Text("Escaneo AR y Cámara en Vivo", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            ft.Text("Apunta con la cámara a la habitación para calcular área y volumen.", size=12, color=ft.colors.GREY_400),
            
            ft.Container(
                expand=True,
                bgcolor="#111827",
                border_radius=12,
                border=ft.border.all(1, ft.colors.CYAN_900),
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.icons.CAMERA_ALT, size=48, color=ft.colors.CYAN_ACCENT),
                    ft.Text("Cámara lista para activarse", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text("Pulsa el botón inferior para iniciar el visor AR en tiempo real.", size=12, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ),

            ft.Row([
                ft.ElevatedButton(
                    text="Guardar Captura / Medición",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_ACCENT,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.go("/geo")
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], expand=True, spacing=10)

    def did_mount(self):
        # Se ejecuta automáticamente al abrir la vista de escaneo en el celular
        js_code = """
        (function() {
            if (!document.getElementById('ar-video-wrapper')) {
                let videoContainer = document.createElement('div');
                videoContainer.id = 'ar-video-wrapper';
                videoContainer.style.position = 'fixed';
                videoContainer.style.top = '0';
                videoContainer.style.left = '0';
                videoContainer.style.width = '100vw';
                videoContainer.style.height = '100vh';
                videoContainer.style.zIndex = '99999';
                videoContainer.style.background = '#000';
                videoContainer.style.display = 'flex';
                videoContainer.style.flexDirection = 'column';
                videoContainer.style.alignItems = 'center';
                videoContainer.style.justifyContent = 'center';

                videoContainer.innerHTML = `
                    <video id="live-ar-video" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;"></video>
                    <div style="position: absolute; bottom: 40px; z-index: 100000; display: flex; gap: 15px;">
                        <button id="close-cam-btn" style="background: #ff4d4d; color: #fff; border: none; padding: 12px 24px; font-size: 14px; font-weight: bold; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">Cerrar Cámara</button>
                    </div>
                `;
                document.body.appendChild(videoContainer);

                // Forzar apertura de la cámara trasera del celular (iPhone/Android)
                navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: "environment" } }, audio: false })
                    .then(stream => {
                        const video = document.getElementById('live-ar-video');
                        video.srcObject = stream;
                        video.play();
                    })
                    .catch(err => {
                        alert("No se pudo acceder a la cámara: " + err.message + ". Verifica los permisos en tu navegador.");
                        document.getElementById('ar-video-wrapper').remove();
                    });

                document.getElementById('close-cam-btn').onclick = function() {
                    let videoElement = document.getElementById('live-ar-video');
                    if (videoElement && videoElement.srcObject) {
                        videoElement.srcObject.getTracks().forEach(track => track.stop());
                    }
                    document.getElementById('ar-video-wrapper').remove();
                };
            }
        })();
        """
        self.page.run_js(js_code)