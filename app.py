import streamlit as st
import re

st.set_page_config(page_title="Amazon 3D Link Generator (DE)", page_icon="📦")
st.title("📦 Amazon 3D Visor Linker (Fijado a Alemania)")
st.write("Genera el enlace del visor 3D forzando el servidor de Amazon Alemania (donde el servicio sigue activo).")

url_input = st.text_input("Enlace de Amazon (cualquier país):", placeholder="https://www.amazon.es/dp/...")

if url_input:
    # Extraer el código ASIN del enlace introducido
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Construimos la URL forzando SIEMPRE el dominio .de (Alemania)
        visor_3d_url = (
            f"https://www.amazon.de/view-3d?"
            f"asin={asin}"
            f"&productType=watch"
            f"&affinity=Furniture"
            f"&extension=zip"
            f"&modelDescriptor=WOODSHOP"
        )
        
        st.success("¡Enlace al visor 3D de Amazon Alemania generado!")
        
        # Enlace clickeable
        st.markdown(f"### 🔗 [Abrir visor 3D en Amazon.de]({visor_3d_url})")
        
        # Código para copiar
        st.code(visor_3d_url, language="text")
        
        st.info(
            "💡 **Instrucciones:** Haz clic en el enlace para abrir el visor en Amazon Alemania. "
            "Pulsa **F12**, ve a la pestaña **Red (Network)**, recarga la página (F5) y busca `.zip` o `.glb` "
            "para descargar el archivo."
        )
        
    else:
        st.error("No se pudo identificar un código ASIN válido en la URL.")
