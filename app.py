import streamlit as st
import requests
import re

st.set_page_config(page_title="Amazon 3D Asset Finder", page_icon="📦")
st.title("📦 Extractor de Modelos 3D Reales (Amazon.de)")
st.write("Extrae los archivos de origen (.glb/.zip) de los servidores de Amazon simulando la App móvil.")

url_input = st.text_input("Introduce el enlace del producto:", placeholder="https://www.amazon.de/dp/...")

if url_input:
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url_input) or re.search(r'/product/([A-Z0-9]{10})', url_input)
    
    if asin_match:
        asin = asin_match.group(1)
        st.info(f"ASIN detectado: **{asin}**")
        
        # Simular los navegadores internos que usa la App móvil para leer datos
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": f"https://www.amazon.de/dp/{asin}"
        }
        
        with st.spinner("Buscando archivos 3D reales en el código de Amazon..."):
            try:
                # Buscamos en la página móvil de Alemania donde se inyectan los scripts 3D
                prod_url = f"https://www.amazon.de/dp/{asin}?th=1&psc=1"
                response = requests.get(prod_url, headers=headers, timeout=15)
                
                html_content = response.text
                
                # Expresiones regulares para cazar los enlaces directos a los modelos (.glb o .zip)
                urls_3d = re.findall(r'(https://[^\s"\']+\.(?:glb|zip))', html_content)
                
                # Filtrar duplicados y limpiar formatos unicode de Amazon
                clean_urls = []
                for url in urls_3d:
                    url_clean = url.replace("\\u002F", "/").replace("\\", "")
                    if url_clean not in clean_urls and "media-amazon.com" in url_clean:
                        clean_urls.append(url_clean)
                
                if clean_urls:
                    st.success(f"¡Se han encontrado {len(clean_urls)} archivo(s) 3D de origen para este producto!")
                    for idx, link in enumerate(clean_urls, 1):
                        ext = "GLB" if ".glb" in link.lower() else "ZIP"
                        st.markdown(f"**Archivo {idx} ({ext}):**")
                        st.code(link, language="text")
                        
                        # Botón de descarga directa desde Streamlit
                        try:
                            file_data = requests.get(link, headers=headers, timeout=10).content
                            st.download_button(
                                label=f"⬇️ Descargar Archivo {idx} ({ext})",
                                data=file_data,
                                file_name=f"{asin}_{idx}.{ext.lower()}",
                                mime="application/octet-stream"
                            )
                        except:
                            st.markdown(f"🔗 [Enlace de descarga directa alternativo]({link})")
                else:
                    st.error("No se han localizado enlaces de archivos 3D en el código de esta página.")
                    st.info(
                        "💡 **Nota:** Si el producto tiene 3D en la app de Alemania pero aquí no aparece, "
                        "Amazon requiere obligatoriamente token de sesión iniciada para mostrar el recurso. "
                        "Usa el método F12 (Pestaña Red) en tu navegador tras loguearte en Amazon.de."
                    )
            except Exception as e:
                st.error(f"Error durante el análisis: {e}")
    else:
        st.error("No se pudo identificar un código ASIN válido.")
