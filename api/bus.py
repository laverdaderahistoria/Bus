from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        html_output = """<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Línea 91 - Mapa y Horarios en Vivo</title>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    width: 100%;
                    overflow: hidden;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background-color: #f4f6f9;
                }
                .header {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 50px;
                    background: #1a73e8;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 20px;
                    font-weight: bold;
                    z-index: 10;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .iframe-container {
                    position: absolute;
                    top: 50px;
                    bottom: 0;
                    left: 0;
                    right: 0;
                }
                iframe {
                    width: 100%;
                    height: 100%;
                    border: none;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <span>🚌 Línea 91: Sangonera - Javalí - Murcia</span>
                <span style="font-size: 13px; font-weight: normal; background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 4px;">Vista Oficial</span>
            </div>
            <div class="iframe-container">
                <iframe src="https://moovitapp.com/tripplan/murcia-3738/lines/lineName/65629805/5931424/en?customerId=4908&ref=16&af_sub8=%252F&af_sub9=Search%20bar%20button&query=Sangonera%20la%20Seca%20-%20Javal%C3%AD%20Nuevo%20-%20Murcia"></iframe>
            </div>
        </body>
        </html>
        """

        self.wfile.write(html_output.encode('utf-8'))
