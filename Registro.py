from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import csv
import yagmail
import random

# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

archivo = open("registro.csv", "a")
nombre_archivo = "registro.csv"
archivoR = open("registro.csv", "r")
ruta_musica = ''
ruta_musica2 = ''
ruta_musica3 = ''
email = 'progra672@gmail.com'
contraseña = 'znioymdmmtslkgar'
asunto = 'Comprobación de correo'
mensaje = 'Este es tu código de verificación'
yag = yagmail.SMTP(user = email, password=contraseña)

def contar_lineas_csv(ruta):
    with open(ruta, 'r') as archivo2:
        contador_lineas = sum(1 for linea in archivo2)
    return contador_lineas

contador = contar_lineas_csv(nombre_archivo)

class registro:
    def Registrarse(self, usuario, nombre, correo, contraseña, foto, nave, musica, musica2, musica3, nombre_archivo):
        global contador
        if self.nombre_existe(usuario, nombre_archivo) == True:
            pass
        elif self.correo_existe(correo, nombre_archivo) == True:
            pass
        elif self.verificar_contra(contraseña) == True:
            pass
        elif self.verificacionCorreo(correo) == True:
            pass
        else:
            contador += 1
            archivo.write(usuario)
            archivo.write(",")
            archivo.write(nombre)
            archivo.write(",")
            archivo.write(correo)
            archivo.write(",")
            archivo.write(contraseña)
            archivo.write(",")
            archivo.write(foto)
            archivo.write(",")
            archivo.write(nave)
            archivo.write(",")
            archivo.write(musica)
            archivo.write(",")
            archivo.write(str(contador))
            archivo.write(",")
            archivo.write(musica2)
            archivo.write(",")
            archivo.write(musica3)
            archivo.write("\n")
            archivo.close()
    def nombre_existe(self, usuario, archivo):
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == usuario:
                    messagebox.showinfo(message="Ya existe ese usuario", title = "Error")
                    return True
                    break
            return False
    def correo_existe(self, correo, archivo):
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[2] == correo:
                    messagebox.showinfo(message="Ya existe ese correo", title = "Error")
                    return True
                    break
            return False
    def verificar_contra(self, contraseña):
        if len(contraseña) < 7:
            messagebox.showinfo(message = "La contraseña debe tener al menos 7 caracteres", title = "Error")
            return True

        if not any(caracter.isupper() for caracter in contraseña):
            messagebox.showinfo(message="La contraseña debe tener al menos una mayúscula", title="Error")
            return True

        if not any(caracter in "!@#$%&/()-_+=[]{}|;:,.<>?/)`~" for caracter in contraseña):
            messagebox.showinfo(message="La contraseña debe tener al menos un símbolo especial", title="Error")
            return True

        if not any(caracter.isdigit() for caracter in contraseña):
            messagebox.showinfo(message="La contraseña debe tener al menos un número", title="Error")
            return True

        if not any(caracter.islower() for caracter in contraseña):
            messagebox.showinfo(message="La contraseña debe tener al menos una minúscula", title="Error")
            return True

        return False
    def verificacionCorreo(self, correo):
        codigo = random.randint(10000, 99999)
        yag.send(correo, asunto, mensaje + ", " + str(codigo))
        global ventana2
        ventana2 = Tk()
        ventana2.geometry("900x450")
        # Caja de texto de código
        caja5 = Entry(ventana2)
        caja5.place(x=280, y=70)
        label = Label(ventana2, text="Código:")
        label.place(x=230, y=70)
        # Botón para verificar
        boton7 = Button(ventana2, text ="Verificar", command=lambda : self.verificarCodigo(codigo, int(caja5.get())))
        boton7.place(x=310, y=280)
        ventana2.mainloop()
    def verificarCodigo(self, codigo, numero):
        if codigo == numero:
            return False
        else:
            messagebox.showinfo(message="Código erróneo",title="Error")
            return True
    def Foto(self):
        global ruta_imagen
        ruta_imagen = filedialog.askopenfilename(title = "Seleccionar imagen", filetypes = [("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    def Nave(self):
        global ruta_nave
        ruta_nave = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    def Musica(self):
        global ruta_musica
        ruta_musica = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
    def Musica2(self):
        global ruta_musica2
        ruta_musica2 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
    def Musica3(self):
        global ruta_musica3
        ruta_musica3 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])

    def __init__(self):
        global ventana
        ventana = Tk()
        ventana.geometry("900x450")
        #Caja de texto de usuario
        caja = Entry()
        caja.place(x = 280, y = 70)
        label = Label(ventana, text="Usuario:")
        label.place(x = 230, y = 70)
        #Caja de texto de nombre
        caja2 = Entry()
        caja2.place(x=280, y=100)
        label2 = Label(ventana, text="Nombre:")
        label2.place(x=228, y=100)
        #Caja de texto de correo
        caja3 = Entry()
        caja3.place(x=280, y=130)
        label3 = Label(ventana, text="Correo:")
        label3.place(x=230, y=130)
        #Caja de texto de contraseña
        caja4 = Entry()
        caja4.place(x=280, y=310)
        label3 = Label(ventana, text="Contraseña:")
        label3.place(x=200, y=310)
        #Botón para registrarse
        boton = Button(text = "Registrarse", command = lambda : self.Registrarse(caja.get(), caja2.get(), caja3.get(), caja4.get(), ruta_imagen, ruta_nave, ruta_musica, ruta_musica2, ruta_musica3, nombre_archivo))
        boton.place(x = 300, y = 340)
        #Botón para elegir fotografía
        boton2 = Button(text="Fotografía", command=self.Foto)
        boton2.place(x=300, y=160)
        #Botón para elegir imagen de nave
        boton3 = Button(text="Imagen de nave", command=self.Nave)
        boton3.place(x=285, y=190)
        #Botón para elegir música
        boton4 = Button(text="Música", command=self.Musica)
        boton4.place(x=310, y=220)
        # Botón para elegir música 2
        boton5 = Button(text="Música 2", command=self.Musica2)
        boton5.place(x=310, y=250)
        # Botón para elegir música 3
        boton6 = Button(text="Música 3", command=self.Musica3)
        boton6.place(x=310, y=280)
        ventana.mainloop()

#objeto = registro()
#objeto.Registro()