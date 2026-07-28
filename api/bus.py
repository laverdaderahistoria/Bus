from http.server import BaseHTTPRequestHandler
import json
import re
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://moovitapp.com/tripplan/murcia-3738/lines/91/65629805/5931424/en?customerId=4908"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cookie": "euconsent-v2=CPXx...; __cmpcc={%22consent%22:true}"
        }

        try:
            res = requests.get(url, headers=headers, timeout=8)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if res.status_code == 200:
                html_content = res.text
                matches = re.findall(r'>([^<>\n]{2,50})<', html_content)
                
                exclusiones = [
                    "Moovit", "Cookie", "Privacy", "About", "Terms", "Ads", "Press", 
                    "Sign", "Log", "EN", "Get the App", "Community", "App Support", 
                    "Contact Us", "Change direction", "Today", "assets_", "cls-1", 
                    "Back", "Change day", "Select a stop", "TMP - Monbus"
                ]
                
                paradas_dict = []
                parada_actual = None
                
                for t in matches:
                    t_limpio = t.strip()
                    if not t_limpio or "{" in t_limpio or "}" in t_limpio or any(exc.lower() in t_limpio.lower() for exc in exclusiones):
                        continue
                    
                    if re.search(r'\d{1,2}:\d{2}', t_limpio) or "Additional Times" in t_limpio:
                        if parada_actual and t_limpio != "Additional Times":
                            for hora in t_limpio.split(","):
                                hora_limpia = hora.strip()
                                if hora_limpia and hora_limpia != "Additional Times:" and hora_limpia not in parada_actual["horarios"]:
                                    parada_actual["horarios"].append(hora_limpia)
                    else:
                        if len(t_limpio) > 2 and not t_limpio.isdigit():
                            parada_actual = {"parada": t_limpio, "horarios": []}
                            paradas_dict.append(parada_actual)

                itinerario_valido = [p for p in paradas_dict if len(p["horarios"]) > 0]

                # Construimos el diseño HTML moderno y responsivo
                html_output = f"""<!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Horarios Línea 91 - TMP Monbus</title>
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; }}
                        h1 {{ color: #1a73e8; font-size: 24px; margin-bottom: 5px; }}
                        .subtitle {{ color: #666; font-size: 14px; margin-bottom: 25px; }}
                        .card {{ background: #fff; padding: 16px 20px; margin-bottom: 12px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1a73e8; }}
                        .parada-nombre {{ font-size: 16px; font-weight: bold; color: #202124; margin-bottom: 10px; }}
                        .horarios-list {{ display: flex; flex-wrap: wrap; gap: 8px; }}
                        .badge {{ background: #e8f0fe; color: #1a73e8; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: 550; }}
                        .footer {{ text-align: center; font-size: 12px; color: #888; margin-top: 30px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🚌 TMP - Monbus Línea 91</h1>
                        <div class="subtitle">Próximas llegadas en tiempo real</div>
                """

                if itinerario_valido:
                    for item in itinerario_valido:
                        html_output += f"""
                        <div class="card">
                            <div class="parada-nombre">📍 {item['parada']}</div>
                            <div class="horarios-list">
                        """
                        for hora in item['horarios']:
                            html_output += f'<span class="badge">🕒 {hora}</span>'
                        html_output += """
                            </div>
                        </div>
                        """
                else:
                    html_output += "<p>No hay horarios disponibles en este momento.</p>"

                html_output += """
                        <div class="footer">Actualizado automáticamente desde Moovit</div>
                    </div>
                </body>
                </html>
                """

                self.wfile.write(html_output.encode('utf-8'))
            else:
                self.wfile.write(b"Error al conectar con la fuente de datos.")
                
        except Exception as e:
            error_msg = f"<!DOCTYPE html><html><body><h3>Error interno:</h3><p>{str(e)}</p></body></html>"
            self.wfile.write(error_msg.encode('utf-8'))
