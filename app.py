import streamlit as st
import re

st.set_page_config(page_title="Amazon 3D Universal Linker", page_icon="📦")
st.title("📦 Amazon 3D Visor Linker Real")
st.write("Introduce el enlace para generar los accesos directos al visor oficial de Amazon Alemania.")

url_input = st.text_input("Enlace de Amazon (Cualquier país o App):", placeholder="https://www.amazon.de/dp/...")

if url_input:
    # Extraer ASIN
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Enlace Opción 1: Visor nativo G3D limpio (Evita la zapatilla genérica)
        url_visor_limpio = f"https://www.amazon.de/view-3d?asin={asin}"
        
        # Enlace Opción 2: Formato alternativo de Realidad Aumentada para navegador
        url_ar_spin = f"https://www.amazon.de/dp/{asin}?v=g3d"
        
        st.success("¡Enlaces de visualización generados!")
        
        st.markdown(f"### 🔗 [Opción 1: Abrir Visor 3D Directo para {asin}]({url_visor_limpio})")
        st.code(url_visor_limpio, language="text")
        
        st.markdown(f"### 🔗 [Opción 2: Abrir Ficha con Forzado 3D]({url_ar_spin})")
        st.code(url_ar_spin, language="text")
        
        st.info(
            "💡 **RECUERDA EL TRUCO DEL NAVEGADOR:**\n"
            "Como Amazon capa el 3D en ordenadores, tras hacer clic en cualquiera de los dos enlaces de arriba:\n"
            "1. Pulsa **F12** y activa la **vista móvil (Ctrl + Shift + M)** en tu navegador.\n"
            "2. Selecciona un dispositivo (por ejemplo, *iPhone* o *Samsung*) en la barra superior del emulador.\n"
            "3. **Recarga la página (F5)** para que Amazon crea que estás 100% en un teléfono.\n"
            "4. Ve a la pestaña **Red (Network)**, filtra por `.glb` o `.zip` y obtendrás tu archivo real."
        )
    else:
        st.error("No se pudo identificar un código ASIN válido.")
