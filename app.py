import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D App Extractor", page_icon="📦")
st.title("📦 Amazon 3D App Downloader")

url_input = st.text_input("1. Enlace de la App de Amazon:", placeholder="https://www.amazon.de/dp/...")
cookie_input = st.text_area("2. Introduce tu Cookie de Amazon (Opcional para saltar bloqueos):", placeholder="session-id=...; x-main=...")

if url_input:
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Cabeceras estrictas de la App de Android
        headers = {
            "User-Agent": "com.amazon.mShop.android/24.16.2 (Linux; U; Android 13)",
            "Accept": "application/json",
            "x-amz-device-type": "android-phone"
        }
        
        if cookie_input:
            headers["Cookie"] = cookie_input

        with st.spinner("Extrayendo modelo exclusivo de la App..."):
            # Forzamos la consulta al almacén de la App de Alemania
            api_url = f"https://www.amazon.de/api/g3d/view-in-your-room/assets?asin={asin}"
            
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and ".glb" in response.text:
                    glb_found = re.search(r'(https://[^\s"\']+\.glb)', response.text)
                    if glb_found:
                        glb_url = glb_found.group(1).replace("\\u002F", "/").replace("\\", "")
                        st.success("¡Modelo de la App Móvil localizado!")
                        
                        file_bytes = requests.get(glb_url, headers=headers).content
                        st.download_button(
                            label="⬇️ Descargar archivo .GLB",
                            data=file_bytes,
                            file_name=f"{asin}.glb",
                            mime="model/gltf-binary"
                        )
                    else:
                        st.error("No se pudo procesar el enlace del modelo.")
                else:
                    st.error("Amazon bloquea la petición remota por falta de credenciales de la App.")
                    st.info("💡 Para solucionarlo, extrae la cookie 'session-id' de tu navegador e introdúcela en el cuadro de arriba.")
            except Exception as e:
                st.error(f"Error: {e}")
