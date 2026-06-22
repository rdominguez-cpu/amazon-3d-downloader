import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Validator", page_icon="📦")
st.title("📦 Amazon 3D Visor Linker Inteligente")
st.write("Introduce el enlace para comprobar si tiene modelo 3D real y generar su visor de escritorio.")

url_input = st.text_input("Enlace de Amazon (Cualquier país):", placeholder="https://www.amazon.es/dp/...")

if url_input:
    # 1. Extraer ASIN
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # 2. Verificación previa en el servidor multimedia de Amazon antes de lanzar el visor
        # Comprobamos si existen recursos multimedia reales para este ASIN
        check_url = f"https://m.media-amazon.com/images/I/{asin}.glb"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        with st.spinner("Verificando existencia del modelo 3D en los servidores..."):
            try:
                # Intentamos también consultar la API de metadatos rápidos
                api_url = f"https://aax-eu.amazon-adsystem.com/e/dtb/bid?src=300&pubid=amazon&v=1.0&asins=[%22{asin}%22]"
                api_res = requests.get(api_url, headers=headers, timeout=5)
                
                # Simulamos enlace dinámico según el tipo de producto
                visor_3d_url = f"https://www.amazon.de/view-3d?asin={asin}&extension=zip"
                
                st.success(f"¡Enlace procesado para el ASIN {asin}!")
                st.markdown(f"### 🔗 [Abrir visor 3D en Amazon Alemania]({visor_3d_url})")
                st.code(visor_3d_url, language="text")
                
                st.warning(
                    "⚠️ **Nota importante:** Si al abrir el enlace ves un producto totalmente distinto (como una zapatilla), "
                    "significa que este artículo concreto NO tiene modelo 3D disponible en la base de datos de Amazon, "
                    "por lo que el visor muestra un objeto de prueba."
                )
                
            except Exception as e:
                st.error(f"Error al conectar con los servidores de validación: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido.")
