import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Downloader", page_icon="📦")
st.title("📦 Amazon 3D Model Downloader")
st.write("Introduce el enlace de Amazon (Alemania, España, etc.) para descargar el modelo 3D.")

url_input = st.text_input("Enlace de Amazon:", placeholder="https://www.amazon.de/dp/...")

if url_input:
    # 1. Extraer el código ASIN del enlace (10 caracteres alfanuméricos)
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"Código ASIN detectado: {asin}")
        
        # 2. Consultar directamente el servidor de contenidos 3D de Amazon
        # Probamos primero el formato estándar de almacenamiento de Amazon
        glb_url = f"https://m.media-amazon.com/images/I/{asin}.glb"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }
        
        with st.spinner("Conectando con el servidor de Amazon 3D..."):
            # Comprobamos si el modelo existe en esa ruta directa
            check = requests.head(glb_url, headers=headers, timeout=10)
            
            if check.status_code == 200:
                st.success("¡Modelo 3D localizado!")
                file_bytes = requests.get(glb_url, headers=headers).content
                st.download_button(
                    label="⬇️ Descargar archivo .GLB",
                    data=file_bytes,
                    file_name=f"{asin}.glb",
                    mime="model/gltf-binary"
                )
            else:
                # Intento alternativo a través de la API móvil de AR
                api_url = f"https://www.amazon.de/api/g3d/view-in-your-room/assets?asin={asin}"
                api_response = requests.get(api_url, headers=headers, timeout=10)
                
                if api_response.status_code == 200 and ".glb" in api_response.text:
                    glb_found = re.search(r'(https://[^\s"\']+\.glb)', api_response.text)
                    if glb_found:
                        final_url = glb_found.group(1)
                        st.success("¡Modelo 3D localizado vía API!")
                        file_bytes = requests.get(final_url, headers=headers).content
                        st.download_button(
                            label="⬇️ Descargar archivo .GLB",
                            data=file_bytes,
                            file_name=f"{asin}.glb",
                            mime="model/gltf-binary"
                        )
                    else:
                        st.error("El producto tiene datos 3D pero no se pudo extraer el enlace directo.")
                else:
                    st.error("No se encontró ningún modelo 3D para este producto. Verifica que el artículo disponga de la opción 'Ver en 3D' o 'Visualizar en tu habitación' en Amazon.")
    else:
        st.error("No se pudo identificar el código ASIN en la URL. Asegúrate de que el enlace contiene la estructura '/dp/ASIN'")
