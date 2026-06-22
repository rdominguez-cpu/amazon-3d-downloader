import streamlit as st
import requests
import re
import json

st.set_page_config(page_title="Amazon 3D Downloader", page_icon="📦")
st.title("📦 Amazon 3D Model Downloader")
st.write("Introduce el enlace de Amazon (cualquier país o app móvil) para forzar la descarga del archivo 3D.")

url_input = st.text_input("Enlace de Amazon:", placeholder="https://www.amazon.de/dp/...")

if url_input:
    # Extraer el ASIN
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"Código ASIN detectado: {asin}")
        
        # Intentar buscar el ID de variante 3D mediante la API de assets global de Amazon
        # Esta URL devuelve los metadatos de imágenes y objetos 3D sin bloqueos de Captcha
        asset_api = f"https://aax-eu.amazon-adsystem.com/e/dtb/bid?src=300&pubid=amazon&v=1.0&asins=[%22{asin}%22]"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        
        with st.spinner("Buscando modelo en el servidor de la App móvil..."):
            # Estrategia 1: Probar descarga directa estimando el ID estándar de Amazon para formatos GLB masivos
            # Muchos modelos de la app se registran bajo el dominio m.media-amazon con IDs vinculados al ASIN en mayúsculas/minúsculas
            
            found = False
            
            # Intentamos buscar el mapa de assets móviles simulando la petición interna de la app
            dimensions_url = f"https://www.amazon.de/gp/aod/ajax/ref=dp_aod_NEW_mbc?asin={asin}&pc=dp"
            res = requests.get(dimensions_url, headers=headers, timeout=10)
            
            # Si falla la página, probamos fuerza bruta en el almacén de imágenes I (donde se guardan los glb)
            # Probamos combinaciones habituales de Amazon para empaquetados 3D de la app
            urls_to_test = [
                f"https://m.media-amazon.com/images/I/{asin}.glb",
                f"https://m.media-amazon.com/images/I/{asin.lower()}.glb",
                f"https://m.media-amazon.com/images/G/01/g3d/assets/{asin}.glb"
            ]
            
            for target_url in urls_to_test:
                check = requests.head(target_url, headers=headers, timeout=5)
                if check.status_code == 200:
                    glb_url = target_url
                    found = True
                    break
            
            # Estrategia 2: Si el archivo directo está oculto con un hash aleatorio (común en ropa/muebles exclusivos de la app)
            if not found:
                # Buscamos en el árbol de elementos multimedia de Amazon
                search_html_url = f"https://www.amazon.de/dp/{asin}?th=1&psc=1"
                page_res = requests.get(search_html_url, headers=headers, timeout=10)
                
                # Intentamos cazar estructuras JSON ocultas en la carga móvil ('hiRes', 'initial', 'audioroom' o 'g3dFeatures')
                match_json = re.findall(r'https://[^\s"\']+\.(?:glb|gltf|zip)', page_res.text, re.IGNORECASE)
                if match_json:
                    glb_url = match_json[0]
                    # Limpiar posibles caracteres de escape de los scripts de Amazon
                    glb_url = glb_url.replace("\\u002F", "/").replace("\\", "")
                    found = True
            
            if found:
                st.success("¡Modelo de la App Móvil localizado con éxito!")
                # Forzar descarga del flujo de datos
                file_bytes = requests.get(glb_url, headers=headers).content
                st.download_button(
                    label="⬇️ Descargar archivo .GLB de la App",
                    data=file_bytes,
                    file_name=f"modelo_{asin}.glb",
                    mime="model/gltf-binary"
                )
            else:
                st.warning("Amazon está aplicando restricciones de región o este ASIN concreto no tiene un archivo GLB directo público.")
                st.info("💡 **Truco alternativo rápido:** Si este producto usa Realidad Aumentada, puedes usar el truco de inspeccionar red (F12) en tu ordenador cambiando el navegador a vista 'Móvil' (Ctrl+Shift+M), abriendo el artículo y filtrando por '.glb'.")
    else:
        st.error("URL no válida. Asegúrate de copiar el enlace completo desde la opción 'Compartir' de la app de Amazon.")
