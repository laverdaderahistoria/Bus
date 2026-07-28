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
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if res.status_code == 200:
                html_content = res.text
                
                # Extraemos textos entre etiquetas
                matches = re.findall(r'>([^<>\n]{2,50})<', html_content)
                
                # Filtramos menús de navegación, código CSS y elementos irrelevantes
                exclusiones = [
                    "Moovit", "Cookie", "Privacy", "About", "Terms", "Ads", "Press", 
                    "Sign", "Log", "EN", "Get the App", "Community", "App Support", 
                    "Contact Us", "Change direction", "Today", "assets_", "cls-1"
                ]
                
                textos_filtrados = []
                for t in matches:
                    t_limpio = t.strip()
                    # Comprobamos que tenga contenido válido y no sea parte de la interfaz web
                    if t_limpio and not t_limpio.startswith("{") and not any(exc.lower() in t_limpio.lower() for exc in exclusiones):
                        if t_limpio not in textos_filtrados:
                            textos_filtrados.append(t_limpio)

                resultado = {
                    "linea": "TMP - Monbus 91",
                    "paradas_y_horarios": textos_filtrados[:15]
                }
                
                self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode('utf-8'))
            else:
                error_data = json.dumps({"status": res.status_code, "error": "No se pudo conectar"})
                self.wfile.write(error_data.encode('utf-8'))
                
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_data = json.dumps({"error": str(e)})
            self.wfile.write(error_data.encode('utf-8'))
