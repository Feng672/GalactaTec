from tkinter import *
import csv
from tkinter import filedialog
import os

# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

nombre_archivo = "registro.csv"
global numero_usuario


class Datos:
    def iniciarVariables(self):
        global usuario
        global nombre
        global correo
        global musica
        global musica2
        global musica3
        global imagen
        global nave
        global ruta_musica
        global ruta_musica2
        global ruta_musica3
        global ruta_imagen
        global ruta_nave
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector_csv = csv.reader(archivo)
            datos = list(lector_csv)
            for fila in datos:
                if int(fila[7]) == numero_usuario:
                    usuario = fila[0]
                    nombre = fila[1]
                    correo = fila[2]
                    ruta_imagen = fila[4]
                    ruta_nave = fila[5]
                    ruta_musica = fila[6]
                    ruta_musica2 = fila[8]
                    ruta_musica3 = fila[9]

        musica = os.path.basename(ruta_musica)
        musica2 = os.path.basename(ruta_musica2)
        musica3 = os.path.basename(ruta_musica3)
        imagen = os.path.basename(ruta_imagen)
        nave = os.path.basename(ruta_nave)
    def obtenerPosi(self, posicion):
        global numero_usuario
        numero_usuario = posicion
    def Cancelar(self):
        ventana.destroy()
        self.DatosDelUsuario()
    def leer_datos_csv(self, ruta):
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector_csv = csv.reader(archivo)
            datos = list(lector_csv)
        return datos
    def escribir_datos_csv(self, datos, ruta):
        with open(ruta, 'w', newline='') as archivo2:
            escritor_csv = csv.writer(archivo2)
            for fila in datos:
                escritor_csv.writerow(fila)
        ventana.destroy()
    def modificar_datos(self,nuevo_usuario,nuevo_nombre,nuevo_correo,nueva_foto,nueva_nave,nueva_música,nueva_música2,nueva_música3):
        datos = self.leer_datos_csv(nombre_archivo)

        for fila in datos:
            if int(fila[7]) == numero_usuario:
                fila[0] = nuevo_usuario
                fila[1] = nuevo_nombre
                fila[2] = nuevo_correo
                fila[4] = nueva_foto
                fila[5] = nueva_nave
                fila[6] = nueva_música
                fila[8] = nueva_música2
                fila[9] = nueva_música3
                break

        self.escribir_datos_csv(datos, nombre_archivo)

    def Foto(self):
        global ruta_imagen
        ruta_imagen = filedialog.askopenfilename(title = "Seleccionar imagen", filetypes = [("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        imagen = os.path.basename(ruta_imagen)
        label4 = Label(ventana, text=imagen)
        label4.place(x = 400, y = 160)
    def Nave(self):
        global ruta_nave
        ruta_nave = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        nave = os.path.basename(ruta_nave)
        label5 = Label(ventana, text=nave)
        label5.place(x=400, y=190)
    def Musica(self):
        global ruta_musica
        ruta_musica = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica = os.path.basename(ruta_musica)
        label6 = Label(ventana, text=musica)
        label6.place(x=400, y=220)
    def Musica2(self):
        global ruta_musica2
        ruta_musica2 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica2 = os.path.basename(ruta_musica2)
        label7 = Label(ventana, text=musica2)
        label7.place(x=400, y=250)
    def Musica3(self):
        global ruta_musica3
        ruta_musica3 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica3 = os.path.basename(ruta_musica3)
        label8 = Label(ventana, text=musica3)
        label8.place(x=400, y=280)

    def __init__(self):
        global ventana
        ventana = Tk()
        ventana.geometry("900x450")
        #Caja de texto de usuario
        caja = Entry()
        caja.place(x = 280, y = 70)
        caja.insert(0, usuario)
        label = Label(ventana, text="Usuario:")
        label.place(x = 230, y = 70)
        #Caja de texto de nombre
        caja2 = Entry()
        caja2.place(x=280, y=100)
        caja2.insert(0, nombre)
        label2 = Label(ventana, text="Nombre:")
        label2.place(x=228, y=100)
        #Caja de texto de correo
        caja3 = Entry()
        caja3.place(x=280, y=130)
        caja3.insert(0, correo)
        label3 = Label(ventana, text="Correo:")
        label3.place(x=230, y=130)
        #Caja de texto de contraseña
        #self.caja3 = Entry()
        #self.caja3.place(x=280, y=250)
        #label3 = Label(ventana, text="Contraseña:")
        #label3.place(x=200, y=250)
        #Botón para aplicar cambios
        boton = Button(text = "Aplicar cambios", command = lambda : self.modificar_datos(caja.get(),caja2.get(), caja3.get(), ruta_imagen, ruta_nave, ruta_musica, ruta_musica2, ruta_musica3))
        boton.place(x = 300, y = 310)
        #Botón para elegir fotografía
        boton2 = Button(text="Fotografía", command=self.Foto)
        boton2.place(x=300, y=160)
        global label4
        label4 = Label(ventana, text=imagen)
        label4.place(x=400, y=160)
        #Botón para elegir imagen de nave
        boton3 = Button(text="Imagen de nave", command=self.Nave)
        boton3.place(x=285, y=190)
        global label5
        label5 = Label(ventana, text=nave)
        label5.place(x=400, y=190)
        #Botón para elegir música
        boton4 = Button(text="Música", command=self.Musica)
        boton4.place(x=310, y=220)
        global label6
        label6 = Label(ventana, text=musica)
        label6.place(x=400, y=220)
        # Botón para elegir música 2
        boton5 = Button(text="Música 2", command=self.Musica2)
        boton5.place(x=310, y=250)
        global label7
        label7 = Label(ventana, text=musica2)
        label7.place(x=400, y=250)
        # Botón para elegir música 3
        boton6 = Button(text="Música 3", command=self.Musica3)
        boton6.place(x=310, y=280)
        global label8
        label8 = Label(ventana, text=musica3)
        label8.place(x=400, y=280)
        #Botón para cancelar cambios
        boton7 = Button(text="Cancelar", command=self.Cancelar)
        boton7.place(x=300, y=340)
        print("muestra")
        ventana.mainloop()

#objeto = Datos()
#objeto.DatosDelUsuario()