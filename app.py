import streamlit as st
import re

st.set_page_config(page_title="Amazon 3D Zip Finder", page_icon="📦")
st.title("📦 Amazon 3D ZIP Link Generator")
st.write("Genera el enlace del visor oficial de Amazon Alemania optimizado para buscar archivos .zip.")

url_input = st.text_input("Enlace de Amazon (Cualquier país):", placeholder="https://www.amazon.es/dp/...")

if url_input:
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # URL oficial idéntica al extractor de Reddit pero fijada a Alemania (.de) 
        # Añade 'landingPage=true' para forzar que cargue el producto real y no la zapatilla
        url_zip_visor = (
            f"https://www.amazon.de/view-3d?"
            f"asin={asin}"
            f"&landingPage=true"
            f"&extension=zip"
        )
        
        st.success("¡Enlace al visor .ZIP generado con éxito!")
        st.markdown(f"### 🔗 [Abrir Visor 3D Real en Amazon.de]({url_zip_visor})")
        st.code(url_zip_visor, language="text")
        
        st.info(
            "💡 **Cómo descargar el .zip ahora:**\n"
            "1. Haz clic en el enlace de arriba (se abrirá Amazon Alemania).\n"
            "2. Pulsa **F12** en tu teclado y ve a la pestaña **Red (Network)**.\n"
            "3. En el filtro de búsqueda de la pestaña Red, escribe **.zip**.\n"
            "4. Recarga la página (**F5**), espera a que cargue el objeto y verás el archivo en la lista. ¡Clic derecho y descargar!"
        )
    else:
        st.error("No se pudo identificar un código ASIN válido.")
