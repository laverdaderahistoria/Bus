from http.server import BaseHTTPRequestHandler
import json
import requests
from bs4 import BeautifulSoup

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
                # Parseamos el HTML con BeautifulSoup
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Buscamos los elementos de las paradas o los horarios en la página
                paradas = []
                # Buscamos los nombres de las paradas que aparecen en la interfaz
                for item in soup.find_all(class_=lambda x: x and ('stop' in x.lower() or 'name' in x.lower())):
                    texto = item.get_text(strip=True)
                    if texto and texto not in paradas and len(texto) < 50:
                        paradas.append(texto)

                # Si no encuentra clases específicas, extraemos los textos relevantes
                if not paradas:
                    paradas = [p.get_text(strip=True) for p in soup.find_all(['span', 'div', 'a']) if len(p.get_text(strip=True)) > 3][:15]

                resultado = {
                    "linea": "TMP - Monbus 91",
                    "elementos_encontrados": paradas[:10]
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
