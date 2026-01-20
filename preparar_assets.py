from PIL import Image, ImageOps
import os

def procesar_imagen(input_path, output_path, size=(500, 500)):
    if not os.path.exists(input_path):
        print(f"❌ No encontré la imagen: {input_path}")
        return

    try:
        # 1. Abrir imagen
        img = Image.open(input_path)
        
        # 2. Transformación Inteligente (ImageOps.fit)
        # Esto recorta el centro y redimensiona, manteniendo la proporción.
        # Evita que tu imagen se vea "estirada" o aplastada.
        img_procesada = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)
        
        # 3. Guardar resultado
        img_procesada.save(output_path)
        print(f"✅ Imagen guardada correctamente en: {output_path} ({size[0]}x{size[1]}px)")
        
    except Exception as e:
        print(f"Error procesando imagen: {e}")

if __name__ == "__main__":
    # Asegúrate de poner tu imagen original en la carpeta assets con nombre 'original.jpg' (o png)
    # El script creará la versión final 'background.png'
    
    ruta_origen = "assets/original.jpg" # <--- CAMBIA ESTO SI TU IMAGEN TIENE OTRO NOMBRE
    ruta_destino = "assets/background.png"
    
    procesar_imagen(ruta_origen, ruta_destino)