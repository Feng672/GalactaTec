from tkinter import *
import tkinter as tk
import csv
from tkinter import messagebox
import random
import yagmail
import threading
import time
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from tkinter import ttk

import pygame
import math
from screeninfo import get_monitors

# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

global numero_usuario
global id2
global primeros_cinco
global primeros_cinco_nuevo
primeros_cinco_nuevo = []

opcion_seleccionada = None
opcion_seleccionada2 = None
opcion_seleccionada3 = None

archivo = open("registro.csv", "a")
salon = open("records.csv", "a")
nombre_archivo = "registro.csv"
archivoR = open("registro.csv", "r")
ruta_musica = ''
ruta_musica2 = ''
ruta_musica3 = ''

nombre_archivo = "registro.csv"
email = 'progra672@gmail.com'
contraseña = 'znioymdmmtslkgar'
global destinatario
#destinatario = 'bryanfeng01@gmail.com'
asunto1 = 'Recuperación de contraseña'
asunto2 = 'Verificación de correo'
mensaje = 'Este es tu código de verificación'
yag = yagmail.SMTP(user = email, password=contraseña)
#yag.send(destinatario, asunto, mensaje)

def contar_lineas_csv(ruta):
    with open(ruta, 'r') as archivo2:
        contador_lineas = sum(1 for linea in archivo2)
    return contador_lineas

contador = contar_lineas_csv(nombre_archivo)

class Inicio:
    def InicioDeSesion(self, usuario, contraseña, archivo):
        if usuario == "" or contraseña == "":
            messagebox.showinfo(message = "Hay un campo vacío", title = "Error")
        elif self.usuario_correcto(usuario, contraseña, archivo) == False:
            messagebox.showinfo(message = "Usuario o contraseña incorrecta", title = "Error")
        else:
            ventana.destroy()
            menu = Menú()
            #messagebox.showinfo(message = "Usuario existente", title = "Éxito")
    def RecuperarContraAux(self, correo):
        if self.CorreoExiste(correo) == True:
            global correo2
            correo2 = correo
            self.generar_codigo()
            global ventana3
            ventana3 = Tk()
            ventana3.configure(bg="black")
            ventana3.geometry("900x450")
            #Caja de código de verificación
            caja4 = Entry(ventana3,font=("fixedsys", 20), fg="white", bg="black")
            caja4.place(x=280, y=70)
            label4 = Label(ventana3, text="Código:", font=("fixedsys", 20), fg="white", bg="black")
            label4.place(x=230, y=70)
            # Botón de verificar
            boton4 = Button(ventana3, text ="Verificar", command=lambda : self.VerificarCodigo(self.codigo, int(caja4.get())), font=("fixedsys", 20), fg="white", bg="black")
            boton4.place(x=310, y=130)
            ventana3.mainloop()
        else:
            pass
    def generar_codigo(self):
        self.codigo = random.randint(10000, 99999)
        #print(self.codigo)
        self.tiempo_inicio = time.time()
        self.tiempo_expiracion = self.tiempo_inicio + 300
        self.iniciar_temporizador()
    def iniciar_temporizador(self):
        if self.timer:
            self.timer.cancel()

        tiempo_restante = self.tiempo_expiracion - time.time()
        if tiempo_restante > 0:
            yag.send(correo2, asunto1, mensaje + "," + str(self.codigo))
            self.timer = threading.Timer(tiempo_restante, self.generar_codigo)
            self.timer.start()
            messagebox.showinfo(message="Código nuevo enviado, revisar correo", title="Aviso")
    def cancelar_temporizador(self):
        if self.timer:
            self.timer.cancel()
    def VerificarCodigo(self, codigo, numero):
        if codigo == numero:
            self.cancelar_temporizador()
            ventana2.destroy()
            ventana3.destroy()
            global ventana4
            ventana4 = Tk()
            ventana4.configure(bg="black")
            ventana4.geometry("900x450")
            #Caja de contraseña nueva
            caja5 = Entry(ventana4,font=("fixedsys", 20), fg="white", bg="black")
            caja5.place(x=310, y=70)
            label5 = Label(ventana4, text="Contraseña:",font=("fixedsys", 20), fg="white", bg="black")
            label5.place(x=230, y=70)
            #Botón de cambiar contraseña
            boton5 = Button(text="Confirmar", command=lambda: self.CambioDeContra(caja5.get(), contraCambiar),font=("fixedsys", 20), fg="white", bg="black")
            boton5.place(x=310, y=130)
            ventana4.mainloop()
        else:
            messagebox.showinfo(message="Código erróneo", title="Error")
    def CambioDeContra(self, contraseña_nueva, posicion):
        verificar = registro
        if verificar.verificar_contra(self, contraseña_nueva) == False:
            fila = int(posicion[7])
            with open(nombre_archivo, 'r', newline='') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                filas_csv = list(lector_csv)
            fila -= 1
            filas_csv[fila][3] = contraseña_nueva
            with open(nombre_archivo, 'w', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerows(filas_csv)
            messagebox.showinfo(message="Cambio de contraseña exitosa", title="Aviso")
            ventana4.destroy()
            self.InicioSesion()
        else:
            pass
    def CorreoExiste(self, correo):
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[2] == correo:
                    global contraCambiar
                    contraCambiar = fila
                    return True
                    break
            return False
    def RecuperarContra(self):
        ventana.destroy()
        global ventana2
        ventana2 = Tk()
        ventana2.configure(bg="black")
        ventana2.geometry("900x450")
        #Caja de texto de correo
        caja3 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja3.place(x=280, y=70)
        label3 = Label(ventana2, text="Correo:",font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=230, y=70)
        #Botón de enviar
        boton4 = Button(text="Enviar", command=lambda : self.RecuperarContraAux(caja3.get()),font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=310, y=130)
        ventana2.mainloop()
    def usuario_correcto(self, usuario, contraseña, archivo):
        global numero_usuario
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == usuario and fila[3] == contraseña:
                    numero_usuario = int(fila[7])
                    return True
                    break
            return False
    def contra_correcta(self, contraseña, archivo):
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[3] == contraseña:
                    return True
                    break
            return False
    def Ventana_registro(self):
        ventana.destroy()
        registro()
        
    def mostrar_ayuda(self):
        ventana.destroy()
        VentanaAyuda(5)
        
    def InicioSesion(self):
        self.timer = None
        self.codigo = None
        self.tiempo_inicio = None
        self.tiempo_expiracion = None
        global ventana
        ventana = Tk()
        ventana.configure(bg="black")
        ventana.geometry("900x450")
        #Caja de texto de usuario
        caja = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja.place(x = 400, y = 70)
        label = Label(ventana, text="Usuario:",font=("fixedsys", 20), fg="white", bg="black")
        label.place(x = 230, y = 70)
        #Caja de texto de contraseña
        caja2 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja2.place(x=400, y=110)
        label2 = Label(ventana, text="Contraseña:",font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=210, y=110)
        #Botón para registrarse
        boton = Button(text = "Registrarse", command = self.Ventana_registro,font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x = 355, y = 150)
        #Botón para iniciar sesión
        boton2 = Button(text="Iniciar sesión", command= lambda: self.InicioDeSesion(caja.get(), caja2.get(), nombre_archivo),font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=330, y=210)
        #Botón para recuperar contraseña
        boton3 = Button(text="Recuperar contraseña", command=self.RecuperarContra,font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=285, y=270)
        #Boton de ayuda
        boton3 = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=10, y=10)
        ventana.mainloop()
#[0]usuario
#[1]nombre
#[2]correo
#[3]contraseña
#[4]foto
#[5]nave
#[6]musica
#[7]id
#[8]musica2
#[9]musica3
#[10]puntaje

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
            archivo.write(",")
            archivo.write("0")
            archivo.write("\n")
            archivo.close()
            ventana6.destroy()
            ventana5.destroy()
            login = Inicio
            login.InicioSesion(login)
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
        yag.send(correo, asunto2, mensaje + ", " + str(codigo))
        global ventana6
        ventana6 = Tk()
        ventana6.configure(bg="black")
        ventana6.geometry("900x450")
        # Caja de texto de código
        caja5 = Entry(ventana6,font=("fixedsys", 20), fg="white", bg="black")
        caja5.place(x=350, y=70)
        label = Label(ventana6, text="Código:",font=("fixedsys", 20), fg="white", bg="black")
        label.place(x=230, y=70)
        # Botón para verificar
        boton7 = Button(ventana6, text ="Verificar", command=lambda : self.verificarCodigo(codigo, int(caja5.get())),font=("fixedsys", 20), fg="white", bg="black")
        boton7.place(x=370, y=280)
        ventana6.mainloop()
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
        global ventana5
        ventana5 = Tk()
        ventana5.configure(bg="black")
        ventana5.geometry("900x900")
        #Caja de texto de usuario
        caja = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja.place(x = 380, y = 70)
        label = Label(ventana5, text="Usuario:",font=("fixedsys", 20), fg="white", bg="black")
        label.place(x = 230, y = 70)
        #Caja de texto de nombre
        caja2 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja2.place(x=380, y=110)
        label2 = Label(ventana5, text="Nombre:",font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=228, y=110)
        #Caja de texto de correo
        caja3 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja3.place(x=380, y=150)
        label3 = Label(ventana5, text="Correo:",font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=230, y=150)
        #Caja de texto de contraseña
        caja4 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja4.place(x=380, y=490)
        label3 = Label(ventana5, text="Contraseña:",font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=190, y=490)
        #Botón para registrarse
        boton = Button(text = "Registrarse", command = lambda : self.Registrarse(caja.get(), caja2.get(), caja3.get(), caja4.get(), ruta_imagen, ruta_nave, ruta_musica, ruta_musica2, ruta_musica3, nombre_archivo),font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x = 370, y = 530)
        #Botón para elegir fotografía
        boton2 = Button(text="Fotografía", command=self.Foto,font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=380, y=190)
        #Botón para elegir imagen de nave
        boton3 = Button(text="Imagen de nave", command=self.Nave,font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=350, y=250)
        #Botón para elegir música
        boton4 = Button(text="Música", command=self.Musica,font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=410, y=310)
        # Botón para elegir música 2
        boton5 = Button(text="Música 2", command=self.Musica2,font=("fixedsys", 20), fg="white", bg="black")
        boton5.place(x=395, y=370)
        # Botón para elegir música 3
        boton6 = Button(text="Música 3", command=self.Musica3,font=("fixedsys", 20), fg="white", bg="black")
        boton6.place(x=395, y=430)
        ventana5.mainloop()

class Menú:
    def Presionó(self):
        ventana7.destroy()
    def IniciarJugador2(self):
        ventana7.destroy()
        inicio2()
    def Datos(self):
        ventana7.destroy()
        Datos(1,numero_usuario)
    def salón(self):
        global primeros_cinco_nuevo
        ventana7.destroy()
        observador = ObserverCSV()
        observador.__int__()
        SalonDeLaFama(primeros_cinco_nuevo,1)
    def ConfiPartida(self):
        ventana7.destroy()
        ConfiguracionDeLaPartida(1)
    def mostrar_ayuda(self):
        ventana7.destroy()
        VentanaAyuda(1)
    def __init__(self):
        global ventana7
        ventana7 = Tk()
        ventana7.configure(bg="black")
        ventana7.geometry("900x500")
        #Botón para editar configuaciones
        boton = Button(text = "Editar configuración del usuario", command = self.Datos,font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x = 200, y = 50)
        # Botón para ver salón de la fama
        boton = Button(text="Salón de la fama", command=self.salón,font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x=320, y=110)
        #Botón para editar configuración de la partida
        boton2 = Button(text="Editar configuración de la partida", command=self.ConfiPartida,font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=190, y=170)
        # Botón para iniciar jugador 2
        boton = Button(text="Iniciar jugador 2", command=self.IniciarJugador2,font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x=310, y=230)
        #Botón para iniciar partida
        boton3 = Button(text="Iniciar partida", command=lambda:IniciarPartida(1,numero_usuario,0),font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=325, y=290)
        #Botón para acceder a la ayuda del juego
        boton5 = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton5.place(x=10, y=10)
        #Botón para salir del juego
        boton4 = Button(text="Salir del juego", command=self.Presionó,font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=325, y=350)
        ventana7.mainloop()

class Datos:
    def iniciarVariables(self, id):
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
                if int(fila[7]) == id:
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
    def Cancelar(self):
        ventana8.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()
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
        ventana8.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()
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
        ventana8.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()

    def Foto(self):
        global ruta_imagen
        ruta_imagen = filedialog.askopenfilename(title = "Seleccionar imagen", filetypes = [("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        imagen = os.path.basename(ruta_imagen)
        label4 = Label(ventana8, text=imagen,font=("fixedsys", 20), fg="white", bg="black")
        label4.place(x = 400, y = 160)
    def Nave(self):
        global ruta_nave
        ruta_nave = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        nave = os.path.basename(ruta_nave)
        label5 = Label(ventana8, text=nave,font=("fixedsys", 20), fg="white", bg="black")
        label5.place(x=400, y=190)
    def Musica(self):
        global ruta_musica
        ruta_musica = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica = os.path.basename(ruta_musica)
        label6 = Label(ventana8, text=musica,font=("fixedsys", 20), fg="white", bg="black")
        label6.place(x=400, y=220)
    def Musica2(self):
        global ruta_musica2
        ruta_musica2 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica2 = os.path.basename(ruta_musica2)
        label7 = Label(ventana8, text=musica2,font=("fixedsys", 20), fg="white", bg="black")
        label7.place(x=400, y=250)
    def Musica3(self):
        global ruta_musica3
        ruta_musica3 = filedialog.askopenfilename(title="Seleccionar MP3", filetypes=[("Archivos de audio", "*.mp3")])
        musica3 = os.path.basename(ruta_musica3)
        label8 = Label(ventana8, text=musica3,font=("fixedsys", 20), fg="white", bg="black")
        label8.place(x=400, y=280)

    def __init__(self, cantidad_de_jugador, id):
        self.iniciarVariables(id)
        global modo
        modo = cantidad_de_jugador
        global ventana8
        ventana8 = Tk()
        ventana8.configure(bg="black")
        ventana8.geometry("900x900")
        #Caja de texto de usuario
        caja = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja.place(x = 355, y = 70)
        caja.insert(0, usuario)
        label = Label(ventana8, text="Usuario:",font=("fixedsys", 20), fg="white", bg="black")
        label.place(x = 220, y = 70)
        #Caja de texto de nombre
        caja2 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja2.place(x=355, y=110)
        caja2.insert(0, nombre)
        label2 = Label(ventana8, text="Nombre:",font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=228, y=110)
        #Caja de texto de correo
        caja3 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja3.place(x=355, y=150)
        caja3.insert(0, correo)
        label3 = Label(ventana8, text="Correo:",font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=230, y=150)
        #Caja de texto de contraseña
        #self.caja3 = Entry()
        #self.caja3.place(x=280, y=250)
        #label3 = Label(ventana, text="Contraseña:")
        #label3.place(x=200, y=250)
        #Botón para aplicar cambios
        boton = Button(text = "Aplicar cambios", command = lambda : self.modificar_datos(caja.get(),caja2.get(), caja3.get(), ruta_imagen, ruta_nave, ruta_musica, ruta_musica2, ruta_musica3),font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x = 300, y = 510)
        #Botón para elegir fotografía
        boton2 = Button(text="Fotografía", command=self.Foto,font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=230, y=210)
        global label4
        label4 = Label(ventana8, text=imagen,font=("fixedsys", 20), fg="white", bg="black")
        label4.place(x=480, y=217)
        #Botón para elegir imagen de nave
        boton3 = Button(text="Imagen de nave", command=self.Nave,font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=230, y=270)
        global label5
        label5 = Label(ventana8, text=nave,font=("fixedsys", 20), fg="white", bg="black")
        label5.place(x=480, y=277)
        #Botón para elegir música
        boton4 = Button(text="Música", command=self.Musica,font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=230, y=330)
        global label6
        label6 = Label(ventana8, text=musica,font=("fixedsys", 20), fg="white", bg="black")
        label6.place(x=400, y=337)
        # Botón para elegir música 2
        boton5 = Button(text="Música 2", command=self.Musica2,font=("fixedsys", 20), fg="white", bg="black")
        boton5.place(x=230, y=390)
        global label7
        label7 = Label(ventana8, text=musica2,font=("fixedsys", 20), fg="white", bg="black")
        label7.place(x=400, y=397)
        # Botón para elegir música 3
        boton6 = Button(text="Música 3", command=self.Musica3,font=("fixedsys", 20), fg="white", bg="black")
        boton6.place(x=230, y=450)
        global label8
        label8 = Label(ventana8, text=musica3,font=("fixedsys", 20), fg="white", bg="black")
        label8.place(x=400, y=457)
        #Botón para cancelar cambios
        boton7 = Button(text="Cancelar", command=self.Cancelar,font=("fixedsys", 20), fg="white", bg="black")
        boton7.place(x=355, y=570)
        ventana8.mainloop()
#Clase singleton para jugador dos
class JugadorDos:
    _instancia = None
    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super().__new__(cls, *args, **kwargs)
            cls._instancia.valor = 0
        return cls._instancia
    def get_valor(self):
        return self.valor
    def set_valor(self, nuevo_valor):
        self.valor = nuevo_valor

class inicio2:
    def mostrar_ayuda(self):
        ventana9.destroy()
        VentanaAyuda(6)
    def __init__(self):
        global ventana9
        ventana9 = Tk()
        ventana9.configure(bg="black")
        ventana9.geometry("900x450")
        # Caja de texto de usuario
        caja = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja.place(x=400, y=70)
        label = Label(ventana9, text="Usuario:", font=("fixedsys", 20), fg="white", bg="black")
        label.place(x=230, y=70)
        # Caja de texto de contraseña
        caja2 = Entry(font=("fixedsys", 20), fg="white", bg="black")
        caja2.place(x=400, y=110)
        label2 = Label(ventana9, text="Contraseña:", font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=210, y=110)
        # Botón para iniciar sesión
        boton2 = Button(text="Iniciar sesión", command=lambda: self.InicioDeSesion2(caja.get(), caja2.get(), nombre_archivo), font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=330, y=210)
        #Boton de ayuda
        boton3 = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton3.place(x=10, y=10)
        ventana9.mainloop()
    def InicioDeSesion2(self, usuario, contraseña, archivo):
        global id2
        id2 = JugadorDos()
        if usuario == "" or contraseña == "":
            messagebox.showinfo(message = "Hay un campo vacío", title = "Error")
        elif self.usuario_correcto2(usuario, contraseña, archivo) == False:
            messagebox.showinfo(message = "Usuario o contraseña incorrecta", title = "Error")
        elif id2.get_valor() == numero_usuario:
            messagebox.showinfo(message = "Usuario logeado", title = "Error")
        else:
            ventana9.destroy()
            Menú2()
    def usuario_correcto2(self, usuario, contraseña, archivo):
        global numero_usuario
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == usuario and fila[3] == contraseña:
                    id2.set_valor(int(fila[7]))
                    return True
                    break
            return False
    def usuario1(self, usuario, contraseña, id1):
        with open(archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == usuario and fila[3] == contraseña:
                    numero_usuario = int(fila[7])
                    return True
                    break
            return False

class Menú2:
    def Datos(self,id):
        ventana10.destroy()
        Datos(2, id)
    def Presionó(self):
        ventana10.destroy()
    def salón(self):
        ventana10.destroy()
        observador = ObserverCSV()
        observador.__int__()
        SalonDeLaFama(primeros_cinco_nuevo,2)
    def ConfiPartida(self):
        ventana10.destroy()
        ConfiguracionDeLaPartida(2)
    def mostrar_ayuda(self):
        ventana10.destroy()
        VentanaAyuda(2)
    def __init__(self):
        global ventana10
        ventana10 = Tk()
        ventana10.configure(bg="black")
        ventana10.geometry("1700x500")
        # Etiqueta que indica que los botones son del jugador 1
        label = Label(ventana10, text="Jugador 1", font=("fixedsys", 20), fg="white", bg="black")
        label.place(x=390, y=50)
        # Botón para editar configuaciones
        boton = Button(text="Editar configuración del usuario", command=lambda : self.Datos(numero_usuario), font=("fixedsys", 20), fg="white",
                       bg="black")
        boton.place(x=200, y=110)
        # Botón para ver salón de la fama
        boton2 = Button(text="Salón de la fama", command=self.salón, font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=320, y=170)
        # Botón para editar configuración de la partida
        boton3 = Button(text="Editar configuración de la partida", command= self.ConfiPartida, font=("fixedsys", 20),
                        fg="white", bg="black")
        boton3.place(x=190, y=230)
        # Botón para iniciar partida
        boton4 = Button(text="Iniciar partida", command=lambda :IniciarPartida(2,numero_usuario,id2.get_valor()), font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=325, y=290)
        #Botón para acceder a la ayuda del juego
        boton5 = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton5.place(x=10, y=10)
        # Botón para salir del juego
        boton6 = Button(text="Salir del juego", command=self.Presionó, font=("fixedsys", 20), fg="white", bg="black")
        boton6.place(x=325, y=350)

        # Etiqueta que indica que los botones son del jugador 2
        label2 = Label(ventana10, text="Jugador 2", font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=1190, y=50)
        # Botón para editar configuaciones para jugador 2
        boton7 = Button(text="Editar configuración del usuario", command=lambda :self.Datos(id2.get_valor()), font=("fixedsys", 20), fg="white",
                       bg="black")
        boton7.place(x=1000, y=110)
        # Botón para ver salón de la fama para jugador 2
        boton8 = Button(text="Salón de la fama", command=self.salón, font=("fixedsys", 20), fg="white", bg="black")
        boton8.place(x=1120, y=170)
        # Botón para editar configuración de la partida para jugador 2
        boton9 = Button(text="Editar configuración de la partida", command= self.ConfiPartida, font=("fixedsys", 20),
                        fg="white", bg="black")
        boton9.place(x=990, y=230)
        # Botón para iniciar partida para jugador 2
        boton10 = Button(text="Iniciar partida", command=lambda :IniciarPartida(2,numero_usuario,id2.get_valor()), font=("fixedsys", 20), fg="white", bg="black")
        boton10.place(x=1125, y=290)
        #Botón para acceder a la ayuda del juego
        boton11 = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton11.place(x=850, y=10)
        # Botón para salir del juego para jugador 2
        boton12 = Button(text="Salir del juego", command=self.Presionó, font=("fixedsys", 20), fg="white", bg="black")
        boton12.place(x=1125, y=350)
        ventana10.mainloop()

class IniciarPartida:
    def __init__(self,modo,id1,id2):
        if modo == 1:
            print("Modo de juego para el futuro")
        else:
            if opcion_seleccionada == None:
                messagebox.showwarning(message="No has seleccionado un patrón de vuelo para el primer nivel", title="Error")
            if opcion_seleccionada2 == None:
                messagebox.showwarning(message="No has seleccionado un patrón de vuelo para el segundo nivel", title="Error")
            if opcion_seleccionada3 == None:
                messagebox.showwarning(message="No has seleccionado un patrón de vuelo para el tercer nivel", title="Error")
            else:
                print(opcion_seleccionada)
                print(opcion_seleccionada2)
                print(opcion_seleccionada3)
                with open(nombre_archivo, 'r', newline='') as archivo_csv:
                    lector_csv = csv.reader(archivo_csv)
                    for fila in lector_csv:
                        if int(fila[7]) == id1:
                            jugador1 = fila[0]
                        elif int(fila[7]) == id2:
                            jugador2 = fila[0]
                jugador_inicial = random.choice([jugador1, jugador2])
                print("El jugador " + jugador_inicial + " iniciará la partida")
                ventana10.destroy()
                juego = Juego()
                juego.iniciar_partida()

# Clase observer para saber cuándo se modifica el archivo CSV
class ObserverCSV:
    def __int__(self):
        global primeros_cinco
        global primeros_cinco_nuevo
        global puntajes
        puntajes = []
        primeros_cinco = primeros_cinco_nuevo
        with open("records.csv", 'r') as file:
            reader = csv.reader(file)
            for fila in reader:
                puntajes.append([int(fila[1]),int(fila[0])])
        self.sort(puntajes)
        primeros_cinco_nuevo = puntajes[:5]
    def sort(self, lista_de_puntuaciones):
        n = len(lista_de_puntuaciones)
        for i in range(n):
            for j in range(0, n-i-1):
                # Si el primer elemento de la lista j es menor que el de j+1, intercambiar
                if lista_de_puntuaciones[j][0] < lista_de_puntuaciones[j+1][0]:
                    lista_de_puntuaciones[j], lista_de_puntuaciones[j+1] = lista_de_puntuaciones[j+1], lista_de_puntuaciones[j]


class SalonDeLaFama:
    def Iniciar_Variables(self, top5):
        global usuario1
        global usuario2
        global usuario3
        global usuario4
        global usuario5
        global foto1
        global foto2
        global foto3
        global foto4
        global foto5
        global ganador1
        global ganador2
        global ganador3
        global ganador4
        global ganador5
        global puntuacion1
        global puntuacion2
        global puntuacion3
        global puntuacion4
        global puntuacion5
        ganador1 = 0
        ganador2 = 0
        ganador3 = 0
        ganador4 = 0
        ganador5 = 0
        puntuacion1 = 0
        puntuacion2 = 0
        puntuacion3 = 0
        puntuacion4 = 0
        puntuacion5 = 0
        largo = len(top5)
        if largo == 1:
            ganador1 = top5[0][1]
            puntuacion1 = top5[0][0]
        elif largo == 2:
            ganador1 = top5[0][1]
            puntuacion1 = top5[0][0]
            ganador2 = top5[1][1]
            puntuacion2 = top5[1][0]
        elif largo == 3:
            ganador1 = top5[0][1]
            puntuacion1 = top5[0][0]
            ganador2 = top5[1][1]
            puntuacion2 = top5[1][0]
            ganador3 = top5[2][1]
            puntuacion3 = top5[2][0]
        elif largo == 4:
            ganador1 = top5[0][1]
            puntuacion1 = top5[0][0]
            ganador2 = top5[1][1]
            puntuacion2 = top5[1][0]
            ganador3 = top5[2][1]
            puntuacion3 = top5[2][0]
            ganador4 = top5[3][1]
            puntuacion4 = top5[3][0]
        elif largo == 5:
            ganador1 = top5[0][1]
            puntuacion1 = top5[0][0]
            ganador2 = top5[1][1]
            puntuacion2 = top5[1][0]
            ganador3 = top5[2][1]
            puntuacion3 = top5[2][0]
            ganador4 = top5[3][1]
            puntuacion4 = top5[3][0]
            ganador5 = top5[4][1]
            puntuacion5 = top5[4][0]
        with open(nombre_archivo, 'r') as file:
            reader = csv.reader(file)
            for fila in reader:
                if int(fila[7]) == ganador1:
                    usuario1 = fila[0]
                    foto1 = fila[4]
                if int(fila[7]) == ganador2:
                    usuario2 = fila[0]
                    foto2 = fila[4]
                if int(fila[7]) == ganador3:
                    usuario3 = fila[0]
                    foto3 = fila[4]
                if int(fila[7]) == ganador4:
                    usuario4 = fila[0]
                    foto4 = fila[4]
                if int(fila[7]) == ganador5:
                    usuario5 = fila[0]
                    foto5 = fila[4]

    def Regresar(self,modo):
        ventana11.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()

    def mostrar_ayuda(self, modo):
        ventana11.destroy()
        if modo == 1:
            VentanaAyuda(3)
        else:
            VentanaAyuda(7)

    def __init__(self, top5, modo):
        self.Iniciar_Variables(top5)
        global ventana11
        ventana11 = Tk()
        ventana11.geometry("900x700")
        ventana11.configure(bg="black")
        label = Label(ventana11, text="Primer lugar",font=("fixedsys", 20), fg="white", bg="black")
        label.place(x = 50, y = 100)
        label2 = Label(ventana11, text="Segundo lugar", font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=50, y=200)
        label3 = Label(ventana11, text="Tercer lugar", font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=50, y=300)
        label4 = Label(ventana11, text="Cuarto lugar", font=("fixedsys", 20), fg="white", bg="black")
        label4.place(x=50, y=400)
        label5 = Label(ventana11, text="Quinto lugar", font=("fixedsys", 20), fg="white", bg="black")
        label5.place(x=50, y=500)
        label16 = Label(ventana11, text="Foto", font=("fixedsys", 20), fg="white", bg="black")
        label16.place(x=300, y=25)
        label17 = Label(ventana11, text="Usuario", font=("fixedsys", 20), fg="white", bg="black")
        label17.place(x=450, y=25)
        label18 = Label(ventana11, text="puntuación", font=("fixedsys", 20), fg="white", bg="black")
        label18.place(x=700, y=25)
        nuevo_tamaño = (80, 80)
        boton = Button(text="Regresar", command=lambda :self.Regresar(modo), font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x= 375, y= 600)
        #Boton de ayuda
        boton2 = Button(text="Ayuda", command=lambda: self.mostrar_ayuda(modo),font=("fixedsys", 20), fg="white", bg="black")
        boton2.place(x=10, y=650)
        imagen14 = Image.open("Campeón.png")
        imagen15 = imagen14.resize(nuevo_tamaño)
        imagen16 = ImageTk.PhotoImage(imagen15)
        label_imagen6 = tk.Label(ventana11, image=imagen16)
        label_imagen6.place(x=100, y=15)
        if puntuacion1 == 0:
            label19 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label19.place(x=450, y=100)
        else:
            imagen1 = Image.open(foto1)
            imagen2 = imagen1.resize(nuevo_tamaño)
            imagen = ImageTk.PhotoImage(imagen2)
            label_imagen = tk.Label(ventana11, image=imagen)
            label_imagen.place(x=300, y=70)
            label6 = Label(ventana11, text=usuario1, font=("fixedsys", 20), fg="white", bg="black")
            label6.place(x=450, y=100)
            label11 = Label(ventana11, text=puntuacion1, font=("fixedsys", 20), fg="white", bg="black")
            label11.place(x=700, y=100)
        if puntuacion2 == 0:
            label20 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label20.place(x=450, y=200)
        else:
            imagen2 = Image.open(foto2)
            imagen3 = imagen2.resize(nuevo_tamaño)
            imagen4 = ImageTk.PhotoImage(imagen3)
            label_imagen2 = tk.Label(ventana11, image=imagen4)
            label_imagen2.place(x=300, y=180)
            label7 = Label(ventana11, text=usuario2, font=("fixedsys", 20), fg="white", bg="black")
            label7.place(x=450, y=200)
            label12 = Label(ventana11, text=puntuacion2, font=("fixedsys", 20), fg="white", bg="black")
            label12.place(x=700, y=200)
        if puntuacion3 == 0:
            label21 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label21.place(x=450, y=300)
        else:
            imagen5 = Image.open(foto3)
            imagen6 = imagen5.resize(nuevo_tamaño)
            imagen7 = ImageTk.PhotoImage(imagen6)
            label_imagen3 = tk.Label(ventana11, image=imagen7)
            label_imagen3.place(x=300, y=290)
            label8 = Label(ventana11, text=usuario3, font=("fixedsys", 20), fg="white", bg="black")
            label8.place(x=450, y=300)
            label13 = Label(ventana11, text=puntuacion3, font=("fixedsys", 20), fg="white", bg="black")
            label13.place(x=700, y=300)
        if puntuacion4 == 0:
            label22 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label22.place(x=450, y=400)
        else:
            imagen8 = Image.open(foto4)
            imagen9 = imagen8.resize(nuevo_tamaño)
            imagen10 = ImageTk.PhotoImage(imagen9)
            label_imagen4 = tk.Label(ventana11, image=imagen10)
            label_imagen4.place(x=300, y=400)
            label9 = Label(ventana11, text=usuario4, font=("fixedsys", 20), fg="white", bg="black")
            label9.place(x=450, y=400)
            label14 = Label(ventana11, text=puntuacion4, font=("fixedsys", 20), fg="white", bg="black")
            label14.place(x=700, y=400)
        if puntuacion5 == 0:
            label23 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label23.place(x=450, y=500)
        else:
            imagen11 = Image.open(foto5)
            imagen12 = imagen11.resize(nuevo_tamaño)
            imagen13 = ImageTk.PhotoImage(imagen12)
            label_imagen5 = tk.Label(ventana11, image=imagen13)
            label_imagen5.place(x=300, y=510)
            label10 = Label(ventana11, text=usuario5, font=("fixedsys", 20), fg="white", bg="black")
            label10.place(x=450, y=500)
            label15 = Label(ventana11, text=puntuacion5, font=("fixedsys", 20), fg="white", bg="black")
            label15.place(x=700, y=500)
        if top5[0][0] == 0:
            pass
        else:
           # imagen1 = Image.open()
            #imagen = ImageTk.PhotoImage(imagen1)
            pass
        ventana11.mainloop()

class ConfiguracionDeLaPartida:
    def actualizar_opcion(self, modo):
        global opcion_seleccionada
        global opcion_seleccionada2
        global opcion_seleccionada3
        opcion_seleccionada = opcion.get()
        opcion_seleccionada2 = opcion2.get()
        opcion_seleccionada3 = opcion3.get()
        if opcion_seleccionada == opcion_seleccionada2 == opcion_seleccionada3:
            messagebox.showwarning(message="No puedes elegir el mismo patrón para los 3 niveles", title="Advertencia")
        elif opcion_seleccionada == opcion_seleccionada2:
            messagebox.showwarning(message="No puede elegir el mismo patrón para el nivel 1 y 2", title="Advertencia")
        elif opcion_seleccionada == opcion_seleccionada3:
            messagebox.showwarning(message="No puedes elegir el mismo patrón para el nivel 1 y 3", title="Advertencia")
        elif opcion_seleccionada2 == opcion_seleccionada3:
            messagebox.showwarning(message="No puede elegir el mismo patrón para el nivel 2 y 3", title="Advertencia")
        else:
            ventana12.destroy()
            if modo == 1:
                Menú()
            else:
                Menú2()
            
    def mostrar_ayuda(self):
        ventana12.destroy()
        VentanaAyuda(4)
        
    def __init__(self,modo):
        global ventana12
        global opcion
        global opcion2
        global opcion3
        ventana12 = Tk()
        ventana12.geometry("900x500")
        ventana12.configure(bg="black")
        label = Label(ventana12, text="Nivel 1", font=("fixedsys", 20), fg="white", bg="black")
        label.place(x=50, y=100)
        opciones = ["Zigzag", "Diagonal", "Spiral", "Horizontal", "Senoidal"]
        opcion = tk.StringVar(ventana12, value=opcion_seleccionada)
        menu_desplegable = ttk.Combobox(ventana12, textvariable=opcion, values=opciones)
        menu_desplegable.pack()
        menu_desplegable.config(font=("fixedsys", 20), background="black", foreground="black", width=10,state="readonly")
        menu_desplegable.place(x=15, y=150)
        boton = Button(text ="Confirmar",command=lambda :self.actualizar_opcion(modo), font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x=365, y=400)

        label2 = Label(ventana12, text="Nivel 2", font=("fixedsys", 20), fg="white", bg="black")
        label2.place(x=385, y=100)
        opcion2 = tk.StringVar(ventana12, value=opcion_seleccionada2)
        menu_desplegable2 = ttk.Combobox(ventana12, textvariable=opcion2, values=opciones)
        menu_desplegable2.pack()
        menu_desplegable2.config(font=("fixedsys", 20), background="black", foreground="black", width=10,state="readonly")
        menu_desplegable2.place(x=350, y=150)

        label3 = Label(ventana12, text="Nivel 3", font=("fixedsys", 20), fg="white", bg="black")
        label3.place(x=735, y=100)
        opcion3 = tk.StringVar(ventana12, value=opcion_seleccionada3)
        menu_desplegable3 = ttk.Combobox(ventana12, textvariable=opcion3, values=opciones)
        menu_desplegable3.pack()
        menu_desplegable3.config(font=("fixedsys", 20), background="black", foreground="black", width=10, state="readonly")
        menu_desplegable3.place(x=700, y=150)
        #Boton de ayuda
        boton = Button(text="Ayuda", command=self.mostrar_ayuda,font=("fixedsys", 20), fg="white", bg="black")
        boton.place(x=10, y=10)
        ventana12.mainloop()

class VentanaAyuda:
    def __init__(self, modo):
        self.modo = modo
        self.ventana13 = Tk()
        self.ventana13.configure(bg="black")
        self.ventana13.title("Ayuda del Videojuego")
        self.ventana13.geometry("800x600")

        # Contenido de la ventana de ayuda
        label = Label(self.ventana13, text="El videojuego se basa en derrotar las naves enemigas que aparecen en la interfaz",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(15, 5), anchor="n")

        label = Label(self.ventana13, text="Controles:",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Para los controles de la nave se puede mover con las teclas del teclado o el joystick",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        label = Label(self.ventana13, text="Con el joystick es igual que con las teclas, el botón de disparo es el espacio igual",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Mover arriba: ↑ ",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")
        
        label = Label(self.ventana13, text="Mover abajo: ↓ ",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Mover izquierda: ← ",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        label = Label(self.ventana13, text="Mover derecha: → ",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Disparar: Espacio __",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        label = Label(self.ventana13, text="Power-ups: Existen 5 bonos",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Bono Disparo Expansivo: Para destruir más de una nave a la vez",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        label = Label(self.ventana13, text="Bono Disparo Perseguidor: Para destruir una nave enemiga sin disparar donde se encuentra",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Bono Puntos Dobles: Los puntos al destruir naves se multiplican por 2 durante 15 seg",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        label = Label(self.ventana13, text="Bono Escudo: Se formará un escudo de 3 niveles para la protección",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=5, anchor="n")

        label = Label(self.ventana13, text="Bono Vida Extra: Se le otorgará una vida de más al jugador",  font=("fixedsys", 15), fg="white", bg="black")
        label.pack(pady=(5, 5), anchor="n")

        # Botón para cerrar la ventana de ayuda
        boton_cerrar = Button(self.ventana13, text="Cerrar", command=self.cerrar_ventana, font=("fixedsys", 20), fg="white", bg="black")
        boton_cerrar.pack(side="top", pady=20)

        self.ventana13.mainloop()

    def cerrar_ventana(self):
        self.ventana13.destroy()
        if self.modo == 1:
            Menú()
        elif self.modo == 2:
            Menú2()
        elif self.modo == 3:
            SalonDeLaFama(primeros_cinco, 1)
        elif self.modo == 4:
            ConfiguracionDeLaPartida(1)
        elif self.modo == 5:
            inicio = Inicio()
            inicio.InicioSesion()
        elif self.modo == 6:
            inicio2()
        elif self.modo == 7:
            SalonDeLaFama(primeros_cinco, 2)

class Juego:
    def iniciar_partida(self):
        # Información de los jugadores
        global nave1
        global nave2
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if int(fila[7]) == numero_usuario:
                    jugador1 = fila[0]
                    nave1 = fila[5]

                elif int(fila[7]) == id2.get_valor():
                    jugador2 = fila[0]
                    nave2 = fila[5]


        global user1
        global user2
        global fotoU1
        global fotoU2
        user1, user2 = random.sample([jugador1, jugador2],2)
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila[0] == user1:
                    fotoU1 = fila[4]

                elif fila[0] == user2:
                    fotoU2 = fila[4]

        # Dimensiones de la ventana
        monitor_info = get_monitors()[0]
        screen_width = monitor_info.width
        screen_height = monitor_info.height
        margin = 200
        global WIDTH
        global HEIGHT
        WIDTH = screen_width - margin
        HEIGHT = screen_height - margin

        # Colores (R, G, B)
        BLACK = (0, 0, 0)
        global WHITE
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        global YELLOW
        YELLOW = (255, 255, 0)
        global RED
        RED = (255, 0, 0)

        # Inicialización de Pygame
        pygame.init()
        pygame.mixer.init()
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("GALAGA")

        global clock
        clock = pygame.time.Clock()
        global famous_lobby
        famous_lobby = []

        # Variables de inicio
        global game_over
        game_over = True
        global running
        running = True
        global last_shot_time_game
        last_shot_time_game = 0

        # Esto funcionará como una especie de "caché" para saber cuál nivel se debe restaurar al morir un jugador
        global levels
        levels = []

        # Cargar recursos
        global background
        background = self.load_image("assets/background.png", (WIDTH, HEIGHT))
        global basic_sound_player
        basic_sound_player = self.load_sound("assets/laser_player.ogg")
        global basic_sound_ship
        basic_sound_ship = self.load_sound("assets/laser_ship.mp3")
        global CA_sound
        CA_sound = self.load_sound("assets/laser_ship_CA.mp3")
        global explosion_sound
        explosion_sound = self.load_sound("assets/explosion.wav")
        global bonus_sound
        bonus_sound = self.load_sound("assets/bonus_sound.mp3")

        # Cargar música inicial
        pygame.mixer.music.load("assets/lobby.ogg")
        pygame.mixer.music.set_volume(100)
        pygame.mixer.music.play(loops=-1)

        # Inicialización de niveles y jugadores
        global fly_patterns
        fly_patterns = ["Diagonal", "Spiral", "Zigzag","Horizontal","Senoidal"]
        global music_levels
        music_levels = [
            "assets/level_1_pump_it.mp3",
            "assets/level_2_cant_stop.mp3",
            "assets/level_3_thats_what_you_get.mp3",
        ]
        global ships_images
        ships_images = [self.load_image(img) for img in ["assets/A1.png", "assets/A2.png", "assets/A3.png"]]

        global current_player
        global player1
        global player2
        global bonus_bar
        global descending_bonus
        global next_bonus_time
        current_player, player1, player2, bonus_bar, descending_bonus, next_bonus_time = self.startConfiguration()
        global all_sprites
        all_sprites = pygame.sprite.Group()
        global ship_list
        ship_list = pygame.sprite.Group()
        global bullets
        bullets = pygame.sprite.Group()
        global bullets_ships
        bullets_ships = pygame.sprite.Group()
        global need_reestart
        need_reestart = True
        global explosion_anim
        explosion_anim = self.load_explosions()

        # Bucle principal
        while running:
            clock.tick(60)
            if need_reestart:
                self.show_go_screen()
                all_sprites = pygame.sprite.Group()
                ship_list = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                bullets_ships = pygame.sprite.Group()
                current_player, player1, player2, bonus_bar, descending_bonus, next_bonus_time = self.startConfiguration()
                self.music_player_level(current_player)
                all_sprites.add(current_player)
                game_over = False
                need_reestart = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    global volume
                    volume = 0.5
                    if event.key == pygame.K_i:
                        # Incrementar el volumen
                        volume = min(volume + 0.1, 1.0)
                        pygame.mixer.music.set_volume(volume)

                    elif event.key == pygame.K_o:
                        # Decrecmentar el volumen
                        volume = max(volume - 0.1, 0.0)
                        pygame.mixer.music.set_volume(volume)

                    elif event.key == pygame.K_SPACE:
                        current_player.shoot(ship_list)
                    elif event.key == pygame.K_z:
                        bonus_bar.select_next("L")
                    elif event.key == pygame.K_x:
                        bonus_bar.select_next("R")
                    elif event.key == pygame.K_c:
                        current_player = bonus_bar.use_action(current_player)
                        if current_player.player_number == 1:
                            player1 = current_player
                        else:
                            player2 = current_player

            if current_player.level.ships_created == 0:
                current_player = self.spawn_ship(3, all_sprites, ship_list, current_player)

            current_player, player1, player2 = self.handle_collisions(levels, all_sprites, ship_list, bullets,
                                                                      explosion_sound,
                                                                      current_player, player1, player2,
                                                                      descending_bonus)

            if current_player.last_level:
                current_player, player1, player2 = self.handle_turn(current_player, player1, player2)
                current_player = self.spawn_ship(3, all_sprites, ship_list, current_player)
                if descending_bonus:
                    descending_bonus.kill()
                    descending_bonus = None

            global current_time
            current_time = pygame.time.get_ticks()
            if current_time >= next_bonus_time:
                if current_player.level.bonus_availables and descending_bonus is None:
                    descending_bonus = self.create_descending_bonus(current_player.level)
                    current_player.bonus_available = True
                    all_sprites.add(descending_bonus)
                next_bonus_time = current_time + random.randint(2000, 5000)

            if descending_bonus:
                screen.blit(descending_bonus.image, descending_bonus.rect.topleft)
                if current_player.rect.colliderect(descending_bonus.rect):
                    bonus_sound.play()
                    bonus_bar.active_disabled_bonus(descending_bonus.type)
                    descending_bonus.kill()
                    descending_bonus = None
                elif descending_bonus.rect.top > HEIGHT:
                    descending_bonus = None

            if current_player.player_number == 1:
                player1 = current_player
            else:
                player2 = current_player

            screen.blit(background, [0, 0])
            all_sprites.update()
            bonus_bar.draw(screen)
            all_sprites.draw(screen)

            self.draw_text(screen, f"Patrón de Vuelo de Naves Enemigas: {str(current_player.level.fly_pattern)}", 15,
                           WIDTH - 160, HEIGHT - 50)

            # información jugador 1
            self.draw_text(screen, user1, 25, 17, 12,
                           color=YELLOW if current_player.player_number == player1.player_number else RED if player1.lives == 0 else WHITE,
                           left_align=True)
            self.draw_shield_bar(screen, 20, 35, player1.shield, player1.layers_shield)
            self.draw_text(screen, "Vidas:", 20, 42, 45)

            screen.blit(player1.foto1, (160,10))

            for i in range(player1.lives):
                screen.blit(player1.icon_life, (80 + i * 25, 50))

            # Vidas del jugador activo
            for i in range(current_player.lives):
                screen.blit(current_player.icon_life, (80 + i * 25, 800))
            player1_text = f"Marcador: {player1.score}\nNivel: {player1.level.number}\nEnemigos Destruidos: {player1.cant_enemies_distroyed}"

            if player1.bonus_double_points_active and player1.bonus_double_points_end_time != 0:
                player1_text += f"\nTiempo doble puntaje: {int(player1.bonus_double_points_end_time - time.time())}"
            self.draw_text(screen, player1_text, 20, 300, 65)

            # información jugador 2
            self.draw_text(screen, user2, 25, WIDTH - 250, 12,
                           color=YELLOW if current_player.player_number == player2.player_number else RED if player2.lives == 0 else WHITE,
                           left_align=True)
            self.draw_shield_bar(screen, WIDTH - 270, 35, player2.shield, player2.layers_shield)
            self.draw_text(screen, "Vidas:", 20, WIDTH - 250, 45)

            screen.blit(player1.foto2, (1600, 10))

            for i in range(player2.lives):
                screen.blit(player2.icon_life, (WIDTH - 200 + i * 25, 50))

            player2_text = f"Marcador: {player2.score}\nNivel: {player2.level.number}\nEnemigos Destruidos: {player2.cant_enemies_distroyed}"

            if player2.bonus_double_points_active and player2.bonus_double_points_end_time != 0:
                player2_text += f"\nTiempo doble puntaje: {int(player2.bonus_double_points_end_time - time.time())}"

            self.draw_text(screen, player2_text, 20, WIDTH - 400, 65)
            game_over, winner, player1, player2 = self.check_game_over(player1, player2)

            if game_over and winner:
                self.end_screen(player1, player2)
                need_reestart = True



            pygame.display.flip()
        pygame.quit()

    def load_image(self, path, size=None):
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    def load_sound(self, path):
        global sound
        sound = pygame.mixer.Sound(path)
        return sound

    # Función para mostrar mensajes modales en pantalla
    def show_modal_message(self, message):
        self.draw_text(screen, message, 30, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(3000)
        screen.fill(BLACK)
        pygame.display.flip()

    # funcion para escribir texto
    def draw_text(self, surface, text, size, x, y, color=WHITE, left_align=False):
        font = pygame.font.SysFont("serif", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if left_align:
            text_rect.midleft = (x, y)
        else:
            text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    # funcion para dibujar la barra de vida de los jugadores
    def draw_shield_bar(self, surface, x, y, percentage, layers_shield):
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        BONUS_WIDTH = 20
        fill_size = (percentage / 100) * BAR_LENGTH
        border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill = pygame.Rect(x, y, fill_size, BAR_HEIGHT)
        pygame.draw.rect(surface, pygame.Color("green"), fill)
        pygame.draw.rect(surface, pygame.Color("white"), border, 2)
        if layers_shield > 0:
            bonus_colors = [pygame.Color("orange"), pygame.Color("blue"), pygame.Color("purple")]
            for i in range(min(layers_shield, len(bonus_colors))):
                bonus_start_x = x + fill_size + i * BONUS_WIDTH
                bonus_rect = pygame.Rect(bonus_start_x, y, BONUS_WIDTH, BAR_HEIGHT)
                pygame.draw.rect(surface, bonus_colors[i], bonus_rect)
                pygame.draw.rect(surface, pygame.Color("white"), bonus_rect, 2)

    # muestra pantallas
    def show_screen(self, title, instructions, wait_key, extra_texts=[], images=[]):
        screen.blit(background, [0, 0])
        self.draw_text(screen, title, 65, WIDTH // 2, HEIGHT // 4)
        self.draw_text(screen, instructions, 27, WIDTH // 2, HEIGHT // 2)
        for extra_text in extra_texts:
            self.draw_text(screen, extra_text['text'], extra_text['size'], extra_text['x'], extra_text['y'],
                      color=YELLOW if extra_text.get('is_colored_yellow', False) else WHITE,
                      left_align=extra_text.get('left_align', False))
        for image in images:
            screen.blit(image['image'], image['position'])
        if wait_key == pygame.K_RETURN:
            self.draw_text(screen, "Presiona 'ENTER' para continuar", 20, WIDTH // 2, HEIGHT - 80, color=YELLOW)
        else:
            self.draw_text(screen, "Presiona cualquier tecla para continuar", 20, WIDTH // 2, HEIGHT - 80, color=YELLOW)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if wait_key is None or event.key == wait_key:
                        waiting = False

    # muestra la pantalla de inicio
    def show_go_screen(self):
        initial_height = HEIGHT // 2 - 50
        extra_texts = [
            {"text": "Instrucciones:", "size": 25, "x": WIDTH // 2, "y": initial_height}
        ]
        instructions = [
            "- Utiliza las flechas para moverte.",
            "- Utiliza 'espacio' para disparar.",
            "- Se habilitarán bonus aleatoriamente, debes chocar con ellos para activarlos.",
            "- Muevete con Z (izquierda) y X (derecha) entre la barra de bonus.",
            "- Utiliza C para seleccionar el bonus por utilizar."
        ]
        initial_height += 20
        for instruction in instructions:
            initial_height += 20
            extra_texts.append({
                "text": instruction,
                "size": 20,
                "x": WIDTH // 2 - 300,
                "y": initial_height,
                "left_align": True
            })
        self.show_screen("GALAGA", "", None, extra_texts)

    # Pantalla de final
    def end_screen(self, player1, player2):
        # Cargar imágenes de jugadores
        player1_image = pygame.image.load(fotoU1).convert_alpha()
        player2_image = pygame.image.load(fotoU2).convert_alpha()

        # Escalar imágenes
        player1_image = pygame.transform.scale(player1_image, (60, 60))
        player2_image = pygame.transform.scale(player2_image, (60, 60))

        # Se carga la corona
        crown = pygame.image.load("assets/crown.png").convert_alpha()
        # Se escala la corona
        crown = pygame.transform.scale(crown, (45, 45))

        # Cargar música de ceremonia
        pygame.mixer.music.load("assets/end_screen_sound.mp3")
        pygame.mixer.music.set_volume(1.0)  # Volumen entre 0.0 y 1.0
        pygame.mixer.music.play(loops=-1)

        first_place = player1 if player1.is_winner else player2
        famous_lobby.append(first_place)

        second_place = player1 if not player1.is_winner else player2

        extra_texts = [
            {"text": "Los resultados fueron: ", "size": 30, "x": WIDTH // 2, "y": HEIGHT // 2 - 30},
            {"text": f"- 1er lugar: {self.user_place(first_place.player_number)}", "size": 27, "x": WIDTH // 2 + 25,
             "y": HEIGHT // 2 + 40},
            {"text": f"... {first_place.score} puntos.", "size": 20, "x": WIDTH // 2 - 20, "y": HEIGHT // 2 + 80,
             "left_align": True},
            {"text": f"... {first_place.lives} vidas.", "size": 20, "x": WIDTH // 2 - 20, "y": HEIGHT // 2 + 100,
             "left_align": True},
            {"text": f"- 2do lugar: {self.user_place(second_place.player_number)}", "size": 27, "x": WIDTH // 2 + 25,
             "y": HEIGHT // 2 + 120},
            {"text": f"... {second_place.score} puntos.", "size": 20, "x": WIDTH // 2 - 20, "y": HEIGHT // 2 + 160,
             "left_align": True},
            {"text": f"... {second_place.lives} vidas.", "size": 20, "x": WIDTH // 2 - 20, "y": HEIGHT // 2 + 180,
             "left_align": True}
        ]

        images = [
            {"image": player1_image, "position": (WIDTH // 2 - 170, HEIGHT // 2 + 20)},
            {"image": player2_image, "position": (WIDTH // 2 - 170, HEIGHT // 2 + 100)},
            {"image": crown, "position": (WIDTH // 2 - 200, HEIGHT // 2 + 20)}
        ]

        self.show_screen("GALAGA", "", None, extra_texts, images)


        with open('records.csv', mode ='a', newline='') as archivo_csv:
            archivo_csv.write(self.user_id(self.user_place(first_place.player_number)))
            archivo_csv.write(",")
            archivo_csv.write(str(first_place.score))
            archivo_csv.write("\n")
        
        observador = ObserverCSV()
        observador.__int__()
        pygame.quit()
        if primeros_cinco != primeros_cinco_nuevo:
            print("Se actualizó el salón de la fama")
        else:
            pass
        SalonDeLaFama(primeros_cinco_nuevo ,2)

    # Función para obtener el usuario del primer lugar y el segundo lugar
    def user_place(self,num):
        if num == 1:
            return user1
        else:
            return user2

    # Función para obtener el id de un usuario
    def user_id(self, user):
        with open(nombre_archivo, 'r') as file:
            reader = csv.reader(file)
            for fila in reader:
                if fila[0] == user:
                    return fila[7]

    # Función para mostrar la pantalla de cambio de nivel y permitir la selección de un patrón
    def level_change_screen(self, current_player):
        # Poner el fondo de pantalla
        screen.blit(background, [0, 0])
        # Mostrar el título y las instrucciones
        self.draw_text(screen, f"¡Jugador {current_player.player_number} avanzas de nivel!", 65, WIDTH // 2, HEIGHT // 4)

        # Mostrar la instrucción para continuar
        self.draw_text(screen, "Presiona cualquier tecla para continuar", 20, WIDTH // 2, HEIGHT - 80, YELLOW)
        pygame.display.flip()

        # Esperar la selección del usuario
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    # Pantalla de continuar luego de cambiar de turno
    def continue_screen(self, current_player):
        self.show_screen("GALAGA", f"Turno del jugador {current_player.player_number}", pygame.K_RETURN)
        self.music_player_level(current_player)

    # Pantalla de error
    def error_screen(self):
        self.show_screen("GALAGA", "Ocurrió un error", pygame.K_RETURN)

    # pantalla sala de la fama
    def famous_lobby_screen(self):
        # Se carga la corona
        crown = pygame.image.load("assets/crown.png").convert_alpha()
        # Se escala la corona
        crown = pygame.transform.scale(crown, (45, 45))

        # Preparar los textos adicionales
        extra_texts = [
            {"text": "Sala de Fama:", "size": 30, "x": WIDTH // 2, "y": HEIGHT // 2 - 50}
        ]

        initial_height = HEIGHT // 2
        images = []

        # se ordena la lista por puntos
        famous_lobby_ordered = sorted(famous_lobby, key=lambda obj: obj.score, reverse=True)
        if famous_lobby_ordered != famous_lobby:
            extra_texts.append({
                "text": "¡La sala de la fama cambió!",
                "size": 20,
                "x": WIDTH // 2,
                "y": initial_height - 80,
                "is_colored_yellow": True
            })

        for index, player in enumerate(famous_lobby_ordered):
            if index > 5:
                break
            else:
                initial_height += 20
                if index == 0:
                    images.append({"image": crown, "position": (WIDTH // 2 - 180, initial_height - 5)})

                extra_texts.append({
                    "text": f"{index + 1}. Jugador {player.player_number} - {player.score}",
                    "size": 27,
                    "x": WIDTH // 2,
                    "y": initial_height
                })

        self.show_screen("GALAGA", "", None, extra_texts, images)
        pygame.mixer.music.stop()

    def handle_collisions(self, levels, all_sprites, ship_list, bullets, explosion_sound, current_player, player1, player2,
                          descending_bonus):
        current_player, player1, player2 = self.handle_player_bullet_collisions(all_sprites, bullets_ships, explosion_sound,
                                                                           current_player, ship_list, player1, player2,
                                                                           descending_bonus)
        current_player, player1, player2 = self.handle_player_ship_collisions(all_sprites, ship_list, explosion_sound,
                                                                         current_player, player1, player2,
                                                                         descending_bonus, levels)
        current_player = self.handle_ship_bullet_collisions(levels, all_sprites, ship_list, bullets, explosion_sound,
                                                       current_player)
        return current_player, player1, player2

    def handle_player_bullet_collisions(self, all_sprites, bullets_ships, explosion_sound, current_player, ship_list, player1,
                                        player2, descending_bonus):
        hits = pygame.sprite.spritecollide(current_player, bullets_ships, True)
        for hit in hits:
            explosion = Explosion(current_player.rect.center)
            all_sprites.add(explosion)
            explosion_sound.play()
            last_lives = current_player.lives
            current_player.score -= 200
            current_player = hit.impact(current_player)
            current_player.disappear()
            if not game_over:
                current_player_last = current_player
                current_player, player1, player2 = self.verify_handle_turn(current_player, player1, player2, last_lives)
                if current_player != current_player_last:
                    self.spawn_ship(3, all_sprites, ship_list, current_player)
                else:
                    self.spawn_ship(1, all_sprites, ship_list, current_player)
            if descending_bonus:
                descending_bonus.kill()

        return current_player, player1, player2

    def handle_player_ship_collisions(self, all_sprites, ship_list, explosion_sound, current_player, player1, player2,
                                      descending_bonus, levels):
        hits = pygame.sprite.spritecollide(current_player, ship_list, True)
        for hit in hits:
            current_player.enemy_destroyed()
            last_lives = current_player.lives
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosion = Explosion(current_player.rect.center)
            all_sprites.add(explosion)
            explosion_sound.play()
            current_player.disappear()
            current_player.dead()
            current_player = self.update_level(levels, current_player)
            if not game_over:
                current_player_last = current_player
                current_player, player1, player2 = self.verify_handle_turn(current_player, player1, player2, last_lives)
                if current_player != current_player_last:
                    self.spawn_ship(3, all_sprites, ship_list, current_player)
                else:
                    self.spawn_ship(1, all_sprites, ship_list, current_player)
            if descending_bonus:
                descending_bonus.kill()
        return current_player, player1, player2

    def handle_ship_bullet_collisions(self, levels, all_sprites, ship_list, bullets, explosion_sound, current_player):
        hits = pygame.sprite.groupcollide(ship_list, bullets, True, True)
        for hit in hits:
            current_player.enemy_destroyed()
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosion_sound.play()
            current_player = self.spawn_ship(1, all_sprites, ship_list, current_player)
            current_player = self.update_level(levels, current_player)
        return current_player

    def verify_handle_turn(self, current_player, player1, player2, last_lives):
        if current_player.lives == 0:
            self.show_modal_message("¡Perdiste todas tus vidas!")
            current_player, player1, player2 = self.handle_turn(current_player, player1, player2)
            bonus_bar.disabled_all_bonus()

        elif current_player.lives < last_lives:
            self.show_modal_message("¡Perdiste una vida!")
            current_player, player1, player2 = self.handle_turn(current_player, player1, player2)
            bonus_bar.disabled_all_bonus()
        return current_player, player1, player2

    def spawn_ship(self, cant, all_sprites, ship_list, current_player):
        created = 0
        while created < cant:
            level = current_player.level
            ship = Ship(level, level.fly_pattern, level.image)
            all_sprites.add(ship)
            ship_list.add(ship)
            current_player.level.add_ship()
            created += 1
        return current_player

    def check_level_points(self, level, current_player):
        if current_player.cant_enemies_distroyed == 20:
            if level == 1:
                return 2
            elif level == 2:
                return 3
            elif level == 3:
                return 4
        return level

    def remove_all_sprites(self, sprite_type):
        global all_sprites
        for sprite in all_sprites:
            if isinstance(sprite, sprite_type):
                sprite.kill()

    def update_level(self, levels, current_player):
        current_level = current_player.level
        new_level_number = self.check_level_points(current_level.number, current_player)
        if current_level.number < new_level_number and new_level_number <= 3:
            shared_level = levels[new_level_number - 1]
            shared_level.reset_ships_created()
            if new_level_number == 1:
                self.level_change_screen(current_player)
                pattern = opcion_seleccionada
                shared_level.fly_pattern = pattern
            elif new_level_number == 2:
                self.level_change_screen(current_player)
                pattern = opcion_seleccionada2
                shared_level.fly_pattern = pattern
            elif new_level_number == 3:
                self.level_change_screen(current_player)
                pattern = opcion_seleccionada3
                shared_level.fly_pattern = pattern
            current_player.level = shared_level
            self.remove_all_sprites(Ship)
            self.remove_all_sprites(Bullet)
            self.remove_all_sprites(Explosion)
            self.remove_all_sprites(Bonus)
            self.music_player_level(current_player)
            current_player.cant_enemies_distroyed = 0
            current_player.bonus_double_points_active = False
            current_player.bonus_double_points_end_time = 0
            current_player.bonus_expansive_bullet = False
            current_player.bonus_seek_bullet = False
        elif new_level_number > 3:
            self.show_modal_message("¡Has completado todos los niveles!")
            current_player.last_level = True
            current_player.cant_enemies_distroyed = 0
            current_player.bonus_double_points_active = False
            current_player.bonus_double_points_end_time = 0
            current_player.bonus_expansive_bullet = False
            current_player.bonus_seek_bullet = False
        return current_player

        all_sprites.remove_internal(current_player)

    def handle_turn(self, current_player, player1, player2):
        if current_player.player_number == 1:
            player1 = current_player
            current_player = player2
        else:
            player2 = current_player
            current_player = player1

        self.remove_all_sprites(Player)
        self.remove_all_sprites(Ship)
        self.remove_all_sprites(Bullet)
        self.remove_all_sprites(Explosion)
        self.remove_all_sprites(Bonus)

        current_player.spawn()
        all_sprites.add(current_player)
        self.continue_screen(current_player)
        current_player.bonus_available = False
        return current_player, player1, player2

    def check_game_over(self, player1, player2):
        if player1.last_level and player2.last_level:
            if player1.score > player2.score:
                player1.is_winner = True
                return True, user1, player1, player2
            elif player2.score > player1.score:
                player2.is_winner = True
                return True, user2, player1, player2
            else:
                player1.is_winner = True
                player2.is_winner = True
                return True, "Empate", player1, player2
        elif player1.lives == 0 and player2.lives == 0:
            if player1.score > player2.score:
                player1.is_winner = True
                return True, user1, player1, player2
            elif player2.score > player1.score:
                player2.is_winner = True
                return True, user2, player1, player2
            else:
                player1.is_winner = True
                player2.is_winner = True
                return True, "Empate", player1, player2
        elif player1.lives == 0 and player2.last_level == True:
            player2.is_winner = True
            return True, user2, player1, player2
        elif player2.lives == 0 and player1.last_level == True:
            player1.is_winner = True
            return True, user1, player1, player2
        else:
            return False, None, player1, player2

    def load_explosions(self, size="SMALL"):
        explosion_anim = []
        for i in range(9):
            img = self.load_image(f"assets/regularExplosion0{i}.png", (200, 200) if size == "BIG" else (70, 70))
            explosion_anim.append(img)
        return explosion_anim

    def music_player_level(self, current_player):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(current_player.level.music)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)

    def create_level(self, used_image_indices, used_pattern_indices, used_music_indices):
        new_image_index = random.choice([i for i in range(3) if i not in used_image_indices])
        used_image_indices.append(new_image_index)
        new_pattern_index = random.choice([i for i in range(3) if i not in used_pattern_indices])
        used_pattern_indices.append(new_pattern_index)
        new_music_index = random.choice([i for i in range(3) if i not in used_music_indices])
        used_music_indices.append(new_music_index)
        image = ships_images[new_image_index]
        fly_pattern = opcion_seleccionada
        music = music_levels[new_music_index]
        level = Level(len(used_image_indices), image, fly_pattern, music)
        return level

    def functionBonus(self, current_player, type):
        bonus_actions = {
            'escudo': current_player.activate_bonus_shield,
            'puntos_dobles': current_player.activate_double_points,
            'vida_extra': current_player.activate_extra_life_bonus,
            'disparo_expansivo': current_player.activate_bonus_expansive_bullet,
            'disparo_perseguidor': current_player.activate_bonus_seek_bullet
        }
        if type in bonus_actions:
            bonus_actions[type]()
            if type in ['disparo_expansivo', 'disparo_perseguidor']:
                current_player.shoot(ship_list)

    def load_bonus_bar(self):
        bonus_types = ['disparo_expansivo', 'disparo_perseguidor', 'puntos_dobles', 'escudo', 'vida_extra']
        bonus_bar = BonusBar()
        for bonus_type in bonus_types:
            bonus = Bonus(bonus_type, self.functionBonus)
            bonus.is_descending = False
            bonus.load_images()
            bonus_bar.add_bonus(bonus)
        return bonus_bar

    def create_descending_bonus(self, level):
        if level.bonus_availables:
            bonus_type = random.choice(level.bonus_availables)
            level.bonus_availables.remove(bonus_type)
            bonus = Bonus(bonus_type, self.functionBonus)
            return bonus
        return None

    def startConfiguration(self):
        next_bonus_time = pygame.time.get_ticks() + random.randint(2000, 5000)
        levels.clear()
        used_image_indices = []
        used_pattern_indices = []
        used_music_indices = []
        for _ in range(3):
            level = self.create_level(used_image_indices, used_pattern_indices, used_music_indices)
            levels.append(level)
        shared_level = levels[0]
        player1 = Player(1)
        player1.level = shared_level
        player2 = Player(2)
        player2.level = shared_level
        current_player = player1
        bonus_bar = self.load_bonus_bar()
        descending_bonus = None
        return current_player, player1, player2, bonus_bar, descending_bonus, next_bonus_time

global juego1
juego1 = Juego()
# clase bonus
class Bonus(pygame.sprite.Sprite):
    def __init__(self, type, action):
        super().__init__()
        self.type = type
        self.is_active = False
        self.is_selected = False
        self.is_descending = True
        self.action = action
        self.load_images()
        if self.image:
            self.rect = self.image.get_rect()
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.top = 0

    def load_images(self):
        if self.is_descending:
            image_path = f"assets/bonus/incognit.png"
            self.image = juego1.load_image(image_path, (30, 30))
        else:
            if self.type:
                image_path = f"assets/bonus/{self.type}.png" if self.is_active else f"assets/bonus/{self.type}_disabled.png"
                self.image = juego1.load_image(image_path, (30, 30))
            else:
                self.image = None

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.kill()

    def select(self):
        self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def activate(self):
        self.is_active = True
        self.load_images()

    def disable(self):
        self.is_active = False
        self.is_selected = False
        self.load_images()

    def use_action(self, current_player):
        self.action(current_player, self.type)
        self.disable()
        return current_player


# clase para la creación de la barra de bonus
class BonusBar:
    def __init__(self):
        self.bonuses = []
        self.screen_height = HEIGHT
        self.bar_height = 50
        self.padding = 10
        self.selected_index = -1

    def update_positions(self):
        start_x = 1500
        y_position = self.screen_height - self.bar_height - 40
        x = start_x
        for bonus in self.bonuses:
            bonus.rect.topleft = (x, y_position)
            x += bonus.rect.width + self.padding

    def draw(self, screen):
        for bonus in self.bonuses:
            if bonus.is_selected:
                pygame.draw.rect(screen, YELLOW, bonus.rect, 2)
            screen.blit(bonus.image, bonus.rect.topleft)

    # esto sirve para desplazarse entre los bonus
    def select_next(self, direction="R"):
        if self.selected_index != -1:
            self.bonuses[self.selected_index].unselect()
        if len(self.bonuses) > 0:
            checked = 0
            while True:
                self.selected_index = (self.selected_index + 1 if direction == "R" else self.selected_index - 1) % len(
                    self.bonuses)
                checked += 1
                if self.bonuses[self.selected_index].is_active:
                    self.bonuses[self.selected_index].select()
                    break
                if checked == len(self.bonuses):
                    break

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        self.update_positions()
        self.select_next()

    def disabled_all_bonus(self):
        for bonus in self.bonuses:
            bonus.disable()

    def remove_bonus(self, bonus):
        self.bonuses.remove(bonus)
        self.update_positions()

    def active_disabled_bonus(self, bonus_type):
        for bonus in self.bonuses:
            if bonus.type == bonus_type and not bonus.is_active:
                bonus.activate()
                return bonus

    def use_action(self, current_player):
        for index, bonus in enumerate(self.bonuses):
            if bonus.is_selected:
                current_player = bonus.use_action(current_player)
                self.bonuses[index] = bonus
        return current_player


# clase jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, player_number):
        super().__init__()
        self.load_images(player_number)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100
        self.lives = 3
        self.player_number = player_number
        self.score = 0
        self.level = None
        self.is_winner = False
        self.last_level = False

        self.spawnX = self.rect.centerx
        self.spawnY = self.rect.centery

        self.cant_enemies_distroyed = 0
        self.disappear_start_time = 0

        # atributos para bonus
        self.layers_shield = 0
        self.bonus_double_points_active = False
        self.bonus_double_points_end_time = 0
        self.bonus_expansive_bullet = False
        self.bonus_seek_bullet = False

    # carga las imagenes de acuerdo al numero de jugador
    def load_images(self, player_number):
        self.original_image = juego1.load_image(f"assets/player{player_number}.png")
        self.aura_image = juego1.load_image(f"assets/aura{player_number}.png", (110, 110))
        self.image = self.original_image
        self.icon_life = juego1.load_image("assets/extra_life_image.png", (15, 15))
        self.icon_life.set_colorkey(BLACK)
        self.image.set_colorkey(BLACK)
        self.foto1 = juego1.load_image(fotoU1, (35,35))
        self.foto2 = juego1.load_image(fotoU1, (35,35))

    def update(self):
        self.handle_movement()
        self.check_double_points()
        if self.disappear_start_time != 0 and time.time() > self.disappear_start_time + 0.5:
            self.reappear()

    def spawn(self):
        self.rect.centerx = self.spawnX
        self.rect.bottom = self.spawnY

    # controlador de movimiento del jugador
    def handle_movement(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speed_y = -15
        if keystate[pygame.K_DOWN]:
            self.speed_y = 15
        if keystate[pygame.K_LEFT]:
            self.speed_x = -15
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 15
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def check_double_points(self):
        if self.bonus_double_points_active and time.time() > self.bonus_double_points_end_time:
            self.disable_double_points()

    def shoot(self, ship_list):
        if self.bonus_expansive_bullet:
            bullet = Bullet(self.rect.centerx, self.rect.top + 5, "T", "Expansivo", ship_list)
            self.disable_bonus_expansive_bullet()
        elif self.bonus_seek_bullet:
            bullet = Bullet(self.rect.centerx, self.rect.top + 5, "B", "Perseguidor", ship_list)
            self.disable_bonus_seek_bullet()
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top, "T", "Basic")
        all_sprites.add(bullet)
        bullets.add(bullet)
        basic_sound_player.play()

    def dead(self):
        self.lives -= 1
        self.spawnX = self.rect.centerx
        self.spawnY = self.rect.bottom

    def reduce_health(self):
        if self.layers_shield > 0:
            self.layers_shield -= 1
        else:
            self.shield -= 50
            if self.shield < 1:
                self.destroy()

    def destroy(self):
        if self.layers_shield > 1:
            self.layers_shield -= 2
        else:
            self.shield = 100
            self.dead()

    def activate_bonus_expansive_bullet(self):
        if self.bonus_available:
            self.bonus_expansive_bullet = True
            self.bonus_available = False

    def activate_bonus_seek_bullet(self):
        if self.bonus_available:
            self.bonus_seek_bullet = True
            self.bonus_available = False

    def activate_bonus_shield(self):
        if self.bonus_available:
            self.layers_shield = 3
            self.bonus_available = False

    def activate_double_points(self):
        if self.bonus_available:
            self.bonus_double_points_active = True
            self.image = self.aura_image
            self.bonus_double_points_end_time = time.time() + 15
            self.bonus_available = False

    def activate_extra_life_bonus(self):
        if self.bonus_available:
            self.lives += 1
            self.bonus_available = False

    def disable_bonus_expansive_bullet(self):
        self.bonus_expansive_bullet = False

    def disable_bonus_seek_bullet(self):
        self.bonus_seek_bullet = False

    def disable_double_points(self):
        self.bonus_double_points_active = False
        self.image = self.original_image
        self.image.set_colorkey(BLACK)

    def enemy_destroyed(self):
        self.cant_enemies_distroyed += 1
        self.score += 400 if self.bonus_double_points_active else 200

    def disappear(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.image.set_colorkey(BLACK)
        self.disappear_start_time = time.time()

    def reappear(self):
        self.image = self.original_image
        if self.bonus_double_points_active:
            self.image = self.aura_image
        self.disappear_start_time = 0
        self.image.set_colorkey(BLACK)


class Ship(pygame.sprite.Sprite):
    def __init__(self, level, fly_pattern, image):
        super().__init__()
        self.level = level
        self.image = image
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH // 2 + int(random.random()))
        self.rect.y = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.choice([-2, 2])
        self.pattern = fly_pattern
        global last_shot_time_game
        self.last_shot_time = last_shot_time_game
        self.shot_cooldown = 1000
        self.can_shoot = True
        self.max_charge_projectiles = 1
        self.zigzag_limit_left = self.rect.x - WIDTH // 6
        self.zigzag_limit_right = self.rect.x + WIDTH // 6
        self.angle = 0
        self.radius = 5

    def shoot(self):
        sound = None
        if random.random() < 0.5:
            bullet = Bullet(self.rect.centerx, self.rect.top + 5, "B", "Basic")
            sound = basic_sound_ship
        else:
            if self.max_charge_projectiles > 0:
                bullet = Bullet(self.rect.centerx, self.rect.top + 5, "B", "CA")
                self.max_charge_projectiles -= 1
                sound = CA_sound
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top + 5, "B", "Basic")
                sound = basic_sound_ship
        bullets_ships.add(bullet)
        all_sprites.add(bullet)
        sound.play()

    def update(self):
        if self.pattern == "Diagonal":
            self.move_diagonal_pattern()
        elif self.pattern == "Spiral":
            self.move_in_spiral_pattern()
        elif self.pattern == "Zigzag":
            self.move_in_zigzag_pattern()
        elif self.pattern == "Horizontal":
            self.move_in_horizontal_pattern()
        elif self.pattern == "Senoidal":
            self.move_in_senoidal_pattern()
        global last_shot_time_game
        global current_time
        if current_time - last_shot_time_game >= self.shot_cooldown and current_time - self.last_shot_time >= self.shot_cooldown and self.can_shoot:
            self.shoot()
            self.last_shot_time = current_time
            last_shot_time_game = current_time
            self.can_shoot = False
        else:
            self.can_shoot = True

    def move_diagonal_pattern(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = HEIGHT

    def move_in_spiral_pattern(self):
        self.angle += 0.1
        self.radius += 0.1
        self.rect.x += int(self.radius * math.cos(self.angle)) + self.speedy
        self.rect.y += int(self.radius * math.sin(self.angle)) + self.speedy
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = HEIGHT

    def move_in_zigzag_pattern(self):
        self.rect.y += self.speedy
        if self.rect.x <= self.zigzag_limit_left or self.rect.x >= self.zigzag_limit_right:
            self.speedx = -self.speedx
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT
    def move_in_horizontal_pattern(self):
        if self.rect.top <= 0:
            self.rect.top = HEIGHT // 3
        self.rect.x += self.speedx
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = HEIGHT
    def move_in_senoidal_pattern(self):
        self.angle += 0.1
        self.rect.x += int(50 * math.cos(self.angle)) + self.speedx
        self.rect.y += self.speedy
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = HEIGHT
class Bullet(pygame.sprite.Sprite):
    EXPLOSIVE_RADIUS = 300

    def __init__(self, x, y, direction, bullet_type, ship_list=None):
        super().__init__()
        self.bullet_type = bullet_type
        self.direction = direction
        self.ship_list = ship_list
        if self.bullet_type in ["Basic", "Perseguidor", "Expansivo"]:
            self.image = juego1.load_image("assets/laser1.png") if direction == "T" else juego1.load_image("assets/laser1.1.png")
        else:
            self.image = juego1.load_image("assets/laser2.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10 if direction == "T" else 10

    def update(self):
        if self.bullet_type == "Perseguidor":
            self.seek_target()
        elif self.bullet_type == "Expansivo":
            if self.direction == "T" and self.rect.centery <= HEIGHT / 2:
                self.destroy_nearby_ships()
                self.kill()
            else:
                self.rect.y += self.speedy
        else:
            self.rect.y += self.speedy
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()

    def seek_target(self):
        closest_ship = None
        closest_distance = float('inf')
        for ship in self.ship_list:
            distance = math.hypot(self.rect.x - ship.rect.x, self.rect.y - ship.rect.y)
            if distance < closest_distance:
                closest_ship = ship
                closest_distance = distance
        if closest_ship:
            dx = closest_ship.rect.centerx - self.rect.centerx
            dy = closest_ship.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                self.rect.x += self.speedy * dx / distance
                self.rect.y += self.speedy * dy / distance

    def impact(self, current_player):
        if self.bullet_type == "Basic" and self.direction != "T":
            current_player.reduce_health()
        elif self.bullet_type == "CA" and self.direction != "T":
            current_player.destroy()
        return current_player

    def destroy_nearby_ships(self):
        for ship in self.ship_list:
            distance = math.hypot(self.rect.x - ship.rect.x, self.rect.y - ship.rect.y)
            if distance < Bullet.EXPLOSIVE_RADIUS:
                explosion = Explosion(ship.rect.center, "BIG")
                all_sprites.add(explosion)
                explosion_sound.play()
                ship.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size="SMALL"):
        super().__init__()
        self.explosion_anim = juego1.load_explosions(size)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Level:
    def __init__(self, number, image, pattern, music):
        self.number = number
        self.ships_created = 0
        self.fly_pattern = pattern
        self.music = music
        self.image = image
        self.bonus_availables = ['disparo_expansivo', 'disparo_perseguidor', 'puntos_dobles', 'escudo', 'vida_extra']

    def reset_ships_created(self):
        self.ships_created = 0

    def add_ship(self):
        self.ships_created += 1


#ConfiguracionDeLaPartida()
inicio = Inicio()
inicio.InicioSesion()
#Menú2()
