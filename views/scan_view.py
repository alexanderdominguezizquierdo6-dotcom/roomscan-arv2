import flet as ft

class ScanView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        super().__init__()
        self.page = page
        self.expand = True
        self.padding = 20
        self.bgcolor = "#0B0F19"
        
        # Componente HTML con JavaScript optimizado para permisos estrictos de iOS Safari
        self.camara_html = ft.Html(
            html=""""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; background: #000; border-radius: 12px; overflow: hidden; position: relative;">
                <video id="video-feed" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;"></video>
                
                <div id="controls-container" style="z-index: 10; position: absolute; bottom: 30px; display: flex; flex-direction: column; align-items: center; gap: 10px; width: 80%;">
                    <button id="btn-start" onclick="startCamera()" style="background: #00f2fe; color: #000; border: none; padding: 14px 24px; font-size: 16px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,242,254,0.4); width: 100%;">
                        📷 Activar Cámara del iPhone
                    </button>
                    <p id="error-msg" style="color: #ff4d4d; font-size: 12px; background: rgba(0,0,0,0.8); padding: 8px 12px; border-radius: 6px; display: none; text-align: center;"></p>
                </div>
            </div>

            <script>
                async function startCamera() {
                    const video = document.getElementById('video-feed');
                    const errorMsg = document.getElementById('error-msg');
                    const btnStart = document.getElementById('btn-start');
                    
                    errorMsg.style.display = 'none';
                    btnStart.innerText = "Conectando cámara...";

                    try {
                        // Intentar forzar la cámara trasera en iOS/Android
                        const constraints = {
                            video: {
                                facingMode: { ideal: "environment" }
                            },
                            audio: false
                        };
                        
                        let stream = await navigator.mediaDevices.getUserMedia(constraints);
                        video.srcObject = stream;
                        await video.play();
                        
                        // Ocultar botón de activación una vez abierta la cámara
                        btnStart.style.display = 'none';
                    } catch (err) {
                        console.error("Error al acceder a la cámara: ", err);
                        errorMsg.style.display = 'block';
                        errorMsg.innerText = "No se pudo acceder: " + err.message + ". Asegúrate de dar permisos en Ajustes > Safari > Cámara.";
                        btnStart.innerText = "Reintentar Activar Cámara";
                    }
                }
            </script>
            """,
            expand=True
        )

        self.content = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.CYAN_ACCENT, on_click=lambda _: self.page.go("/dashboard")),
                ft.Text("Escaneo AR y Cámara", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ]),
            ft.Text("Apunta con la cámara a la habitación para calcular área y volumen.", size=12, color=ft.colors.GREY_400),
            
            # Contenedor visual del visor de cámara
            ft.Container(
                expand=True,
                bgcolor="#111827",
                border_radius=12,
                border=ft.border.all(1, ft.colors.CYAN_900),
                content=self.camara_html
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