import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Matrices de conversión
RGBaYIQ = np.array([[0.299, 0.587, 0.114],
                    [0.596, -0.274, -0.322],
                    [0.211, -0.523, 0.312]])

YIQaRGB = np.array([[1.0, 0.956, 0.621],
                    [1.0, -0.272, -0.647],
                    [1.0, -1.106, 1.703]])

# Variables globales
imagen = None
imagen_modificada = None
canvas = None
iluminacion = None
saturacion = None

def mostrar_imagen(img):
    """Muestra la imagen en el canvas"""
    global canvas
    img_tk = ImageTk.PhotoImage(img)
    canvas.configure(image=img_tk)
    canvas.image = img_tk  # evitar garbage collection

def abrir_imagen():
    """Abre una imagen y la muestra"""
    global imagen
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png;*.jpeg;*.bmp")])
    if archivo:
        imagen = Image.open(archivo).convert("RGB")
        mostrar_imagen(imagen)

def aplicar_filtro():
    """Aplica cambios de luminancia y saturación"""
    global imagen, imagen_modificada, iluminacion, saturacion
    if imagen is None:
        return

    a = iluminacion.get()  # valor de luminancia
    b = saturacion.get()  # valor de saturación

    # Normalizar [0,1]
    arreglo = np.array(imagen).astype(np.float32) / 255.0

    # Convertir a YIQ
    yiq = arreglo @ RGBaYIQ.T

    # Aplicar coeficientes
    yiq[..., 0] = np.clip(a * yiq[..., 0], 0, 1)  # Y
    yiq[..., 1] = np.clip(b * yiq[..., 1], -0.5957, 0.5957)  # I
    yiq[..., 2] = np.clip(b * yiq[..., 2], -0.5226, 0.5226)  # Q

    # Volver a RGB
    rgb = yiq @ YIQaRGB.T
    rgb = np.clip(rgb, 0, 1)
    rgb = (rgb * 255).astype(np.uint8)

    imagen_modificada = Image.fromarray(rgb)
    mostrar_imagen(imagen_modificada)

def guardar_imagen():
    """Guarda la imagen modificada"""
    global imagen_modificada
    if imagen_modificada:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("BMP files", "*.bmp"),
                                                            ("TIFF files", "*.tiff")])
        if file_path:
            imagen_modificada.save(file_path)

    

# Interfaz Tkinter
root = tk.Tk()
root.title("Editor Luminancia y Saturación (RGB <-> YIQ)")

# Botones
abrir = tk.Button(root, text="Abrir Imagen", command=abrir_imagen)
abrir.pack(pady=5)

filtro = tk.Button(root, text="Aplicar Filtro", command=aplicar_filtro)
filtro.pack(pady=5)

guardar = tk.Button(root, text="Guardar Imagen", command=guardar_imagen)
guardar.pack(pady=5)

# Canvas para mostrar imagen
canvas = tk.Label(root)
canvas.pack()

# Sliders de control
iluminacion = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1,
                      orient="horizontal", label="Iluminacion (a)")
iluminacion.set(1.0)
iluminacion.pack(fill="x", padx=20, pady=5)

saturacion = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1,
                      orient="horizontal", label="Saturación (b)")
saturacion.set(1.0)
saturacion.pack(fill="x", padx=20, pady=5)

# Ejecutar interfaz
root.mainloop()
