import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Downloader Universal", page_icon="📦")
st.title("📦 Amazon 3D Model Downloader")
st.write("Introduce el enlace directo de Amazon de cualquier país (Alemania, España, etc.) copiado de la web o de la app móvil.")

url_input = st.text_input("Enlace de Amazon:", placeholder="https://www.amazon.de/dp/...")

if url_input:
    # 1. Detectar automáticamente el dominio del país (ej: amazon.de, amazon.es, amazon.co.uk)
    domain_match = re.search(r'(amazon\.[a-z\.]+)', url_input)
    amazon_domain = domain_match.group(1) if domain_match else "amazon.de"
    
    # 2. Extraer el código ASIN del enlace
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"Dominio detectado: **{amazon_domain}** | ASIN detectado: **{asin}**")
        
        # Simulamos un entorno móvil real para esquivar los bloqueos básicos de Amazon
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        with st.spinner("Buscando el modelo 3D en la tienda correspondiente..."):
            # Estrategia A: Buscar en la API interna de Realidad Aumentada adaptada al país del producto
            api_url = f"https://www.{amazon_domain}/api/g3d/view-in-your-room/assets?asin={asin}"
            
            try:
                api_response = requests.get(api_url, headers=headers, timeout=10)
                found = False
                glb_url = ""
                
                if api_response.status_code == 200 and ".glb" in api_response.text:
                    glb_found = re.search(r'(https://[^\s"\']+\.glb)', api_response.text)
                    if glb_found:
                        glb_url = glb_found.group(1).replace("\\u002F", "/").replace("\\", "")
                        found = True
                
                # Estrategia B: Si la API no responde, buscar el modelo masivo en el almacén global estático
                if not found:
                    urls_to_test = [
                        f"https://m.media-amazon.com/images/I/{asin}.glb",
                        f"https://m.media-amazon.com/images/I/{asin.lower()}.glb"
                    ]
                    for target_url in urls_to_test:
                        check = requests.head(target_url, headers=headers, timeout=5)
                        if check.status_code == 200:
                            glb_url = target_url
                            found = True
                            break
                
                # Resultado final
                if found:
                    st.success("¡Modelo 3D localizado con éxito!")
                    file_bytes = requests.get(glb_url, headers=headers).content
                    st.download_button(
                        label="⬇️ Descargar archivo .GLB",
                        data=file_bytes,
                        file_name=f"{asin}.glb",
                        mime="model/gltf-binary"
                    )
                else:
                    st.error(f"Amazon {amazon_domain} no ha devuelto ningún archivo 3D para este ASIN. Comprueba desde tu móvil si el artículo sigue teniendo activo el botón de 'Ver en 3D'.")
            
            except Exception as e:
                st.error(f"Error de conexión con el servidor: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido en la URL.")
