import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Universal Linker", page_icon="📦")
st.title("📦 Extractor de Modelos 3D Reales (Sin Zapatilla)")
st.write("Genera el acceso directo al visor de Amazon Alemania forzando la carga del objeto real.")

# 1. Entrada de datos
url_input = st.text_input("1. Enlace del producto de Amazon:", placeholder="https://www.amazon.de/dp/...")
cookie_input = st.text_area("2. Introduce tu cookie 'session-id' o la cadena completa (Opcional para forzar la carga):", 
                            placeholder="session-id=262-5385381-7350448")

if url_input:
    # Extraer el ASIN
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Intentar extraer IDs físicos en segundo plano si hay cookies presentes
        physical_id = ""
        if cookie_input:
            api_url = f"https://www.amazon.de/api/g3d/view-in-your-room/assets?asin={asin}"
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
                "Accept": "application/json",
                "Cookie": cookie_input.strip()
            }
            try:
                res = requests.get(api_url, headers=headers, timeout=10)
                if res.status_code == 200:
                    id_match = re.search(r'"extensionToken"\s*:\s*"([^"]+)"', res.text) or re.search(r'"modelId"\s*:\s*"([^"]+)"', res.text)
                    if id_match:
                        physical_id = id_match.group(1)
            except:
                pass

        # Construir la URL del visor forzando los parámetros que lee el motor G3D de Amazon
        visor_url = (
            f"https://www.amazon.de/view-3d?"
            f"asin={asin}"
            f"&landingPage=true"
            f"&extension=zip"
        )
        if physical_id:
            visor_url += f"&physicalId={physical_id}"
            st.success("🎯 ¡ID físico de renderizado cargado desde tu sesión!")

        st.success("¡Enlace listo para usar!")
        st.markdown(f"### 🔗 [Abrir Visor 3D del Producto en Amazon.de]({visor_url})")
        st.code(visor_url, language="text")
        
        st
