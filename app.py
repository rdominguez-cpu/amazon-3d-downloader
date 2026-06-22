import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D True Linker", page_icon="📦")
st.title("📦 Extractor de Enlaces 3D Reales (Método API)")
st.write("Genera el enlace al visor oficial de Amazon Alemania forzando la ID de renderizado correcta.")

url_input = st.text_input("Introduce el enlace de Amazon (Cualquier país):", placeholder="https://www.amazon.es/dp/...")

if url_input:
    # 1. Extraer el ASIN
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # 2. Consultamos la API pública de Amazon que vincula el ASIN con su archivo 3D real (PhysicalID)
        # Usamos el mercado alemán que es el que tiene el motor activo
        api_url = f"https://www.amazon.de/api/g3d/view-in-your-room/assets?asin={asin}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        
        with st.spinner("Conectando con la base de datos de Amazon Alemania..."):
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                
                # Intentamos buscar si la API nos escupe un código de renderizado (PhysicalID / Model ID)
                # que suele ser un código largo que empieza por B1... o similar
                physical_id = ""
                if response.status_code == 200:
                    # Buscamos patrones comunes de IDs de Amazon 3D en el texto de la API
                    id_match = re.search(r'"extensionToken"\s*:\s*"([^"]+)"', response.text) or re.search(r'"modelId"\s*:\s*"([^"]+)"', response.text)
                    if id_match:
                        physical_id = id_match.group(1)
                
                # Si la API directa falla por bloqueo, generamos el enlace dinámico estructurado 
                # para que el propio navegador resuelva el modelo real en Amazon.de
                visor_url = (
                    f"https://www.amazon.de/view-3d?"
                    f"asin={asin}"
                    f"&landingPage=true"
                    f"&extension=zip"
                )
                
                if physical_id:
                    visor_url += f"&physicalId={physical_id}"
                    st.success("🎯 ¡ID de renderizado real localizado!")
                else:
                    st.warning("⚠️ No se pudo pre-cargar el ID físico, generando enlace de resolución automática.")

                st.markdown(f"### 🔗 [Abrir Visor 3D del Producto en Amazon.de]({visor_url})")
                st.code(visor_url, language="text")
                
                st.info(
                    "💡 **INSTRUCCIONES CLAVE (Para evitar la zapatilla):**\n"
                    "1. Haz clic en el enlace de arriba para ir a Amazon Alemania.\n"
                    "2. **OBLIGATORIO:** Si te sale la zapatilla, pulsa **F12**, pon la **vista móvil (Ctrl+Shift+M)** y **RECARGA LA PÁGINA (F5)**.\n"
                    "3. Al recargar simulando un móvil en la web alemana, el servidor se verá obligado a sustituir la zapatilla por el modelo real de tu producto.\n"
                    "4. Busca `.zip` en la pestaña **Red (Network)** para descargarlo."
                )
                
            except Exception as e:
                st.error(f"Error al procesar: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido.")
