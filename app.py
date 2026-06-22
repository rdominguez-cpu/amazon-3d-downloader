import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Real Validator", page_icon="📦")
st.title("📦 Amazon 3D ZIP Link Validator")
st.write("Introduce el enlace para verificar si el producto tiene un modelo 3D real asignado en los servidores de Amazon.")

url_input = st.text_input("Enlace de Amazon (Cualquier país):", placeholder="https://www.amazon.es/dp/...")

if url_input:
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Enlaces de prueba directa a los servidores de imágenes de Amazon (donde se guardan los archivos reales)
        url_test_zip = f"https://m.media-amazon.com/images/I/{asin}.zip"
        url_test_glb = f"https://m.media-amazon.com/images/I/{asin}.glb"
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        with st.spinner("Comprobando disponibilidad real del archivo 3D..."):
            try:
                # Comprobamos si el archivo .zip o .glb existe en el almacén de Amazon
                res_zip = requests.head(url_test_zip, headers=headers, timeout=5)
                res_glb = requests.head(url_test_glb, headers=headers, timeout=5)
                
                if res_zip.status_code == 200 or res_glb.status_code == 200:
                    st.success("¡Modelo 3D real localizado en el servidor!")
                    
                    # Si existe, generamos el enlace limpio al visor
                    url_zip_visor = f"https://www.amazon.de/view-3d?asin={asin}&landingPage=true&extension=zip"
                    st.markdown(f"### 🔗 [Abrir Visor 3D Real en Amazon.de]({url_zip_visor})")
                    st.code(url_zip_visor, language="text")
                else:
                    # Si devuelve 404, sabemos que Amazon va a mostrar la zapatilla por defecto
                    st.error("❌ Este producto NO tiene ningún modelo 3D real subido a los servidores de Amazon.")
                    st.warning("⚠️ Si abres el visor de forma forzada para este ASIN, Amazon te mostrará la zapatilla de muestra (*fallback*).")
                    
            except Exception as e:
                st.error(f"Error de conexión con el servidor de Amazon: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido.")
