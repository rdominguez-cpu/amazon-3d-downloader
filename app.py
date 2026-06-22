import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Downloader Pro", page_icon="📦")
st.title("📦 Amazon 3D Model Downloader")
st.write("Introduce el enlace de Amazon (de la web o copiado desde la app móvil) para forzar la extracción del archivo 3D.")

url_input = st.text_input("Enlace de Amazon:", placeholder="https://www.amazon.de/dp/...")

if url_input:
    # 1. Extraer el código ASIN de forma limpia
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # 2. Configurar las credenciales móviles que usa la App de Amazon Android
        # Esto hace que el servidor nos trate como la aplicación oficial, saltándose el Captcha
        headers = {
            "User-Agent": "com.amazon.mShop.android/24.16.2 (Linux; U; Android 13; es_ES; Build/TP1A.220624.014)",
            "Accept": "application/json",
            "x-amz-device-type": "android-phone",
            "x-amzn-identity-auth-domain": "www.amazon.de"
        }
        
        with st.spinner("Conectando con la API interna de la App de Amazon..."):
            # Atacamos directamente al almacén de recursos de Realidad Aumentada (G3D) de Amazon Alemania
            api_url = f"https://www.amazon.de/api/g3d/view-in-your-room/assets?asin={asin}"
            
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                found = False
                glb_url = ""
                
                # Si la API responde el mapa de objetos, buscamos el enlace .glb oculto dentro
                if response.status_code == 200 and ".glb" in response.text:
                    glb_found = re.search(r'(https://[^\s"\']+\.glb)', response.text)
                    if glb_found:
                        glb_url = glb_found.group(1).replace("\\u002F", "/").replace("\\", "")
                        found = True
                
                # Ruta alternativa secundaria en el servidor multimedia de Amazon
                if not found:
                    test_url = f"https://m.media-amazon.com/images/I/{asin}.glb"
                    check = requests.head(test_url, headers=headers, timeout=5)
                    if check.status_code == 200:
                        glb_url = test_url
                        found = True
                
                # Mostrar resultado en la pantalla
                if found:
                    st.success("¡Modelo de la App Móvil localizado!")
                    file_bytes = requests.get(glb_url, headers=headers).content
                    st.download_button(
                        label="⬇️ Descargar archivo .GLB de la App",
                        data=file_bytes,
                        file_name=f"{asin}.glb",
                        mime="model/gltf-binary"
                    )
                else:
                    st.error("No se ha podido extraer el modelo automático debido al cifrado por región de Amazon.")
                    st.info("💡 **Consejo:** Si ves que se resiste, abre el enlace en tu ordenador, pulsa **F12**, haz clic en la pestaña **Red (Network)**, pon en el buscador `.glb` y dale al botón 'Ver en 3D' en la pantalla de Amazon para descargarlo con un doble clic.")
            
            except Exception as e:
                st.error(f"Error de conexión: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido en la URL.")
