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

# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

global numero_usuario
global id2
global primeros_cinco
opcion_seleccionada = None
opcion_seleccionada2 = None
opcion_seleccionada3 = None

archivo = open("registro.csv", "a")
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
        print("presionó")
    def IniciarJugador2(self):
        ventana7.destroy()
        inicio2()
    def Datos(self):
        ventana7.destroy()
        Datos(1,numero_usuario)
    def salón(self):
        global primeros_cinco
        ventana7.destroy()
        observador = ObserverCSV()
        observador.__int__()
        SalonDeLaFama(primeros_cinco,1)
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
        boton5.place(x=400, y=350)
        #Botón para salir del juego
        boton4 = Button(text="Salir del juego", command=self.Presionó,font=("fixedsys", 20), fg="white", bg="black")
        boton4.place(x=325, y=410)
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
        pass
    def salón(self):
        global primeros_cinco
        ventana10.destroy()
        observador = ObserverCSV()
        observador.__int__()
        SalonDeLaFama(primeros_cinco,2)
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
        boton5.place(x=400, y=350)
        # Botón para salir del juego
        boton6 = Button(text="Salir del juego", command=self.Presionó, font=("fixedsys", 20), fg="white", bg="black")
        boton6.place(x=325, y=410)

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
        boton11.place(x=1200, y=350)
        # Botón para salir del juego para jugador 2
        boton12 = Button(text="Salir del juego", command=self.Presionó, font=("fixedsys", 20), fg="white", bg="black")
        boton12.place(x=1125, y=410)
        ventana10.mainloop()

class IniciarPartida:
    def __init__(self,modo,id1,id2):
        if modo == 1:
            print("Partida iniciada con una persona")
        else:
            with open(nombre_archivo, 'r', newline='') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                for fila in lector_csv:
                    if int(fila[7]) == id1:
                        jugador1 = fila[0]
                    elif int(fila[7]) == id2:
                        jugador2 = fila[0]
            jugador_inicial = random.choice([jugador1,jugador2])
            print("El jugador " + jugador_inicial + " iniciará la partida")

# Clase observer para saber cuándo se modifica el archivo CSV
class ObserverCSV:
    def __int__(self):
        global primeros_cinco
        global puntajes
        puntajes = []
        with open(nombre_archivo, 'r') as file:
            reader = csv.reader(file)
            for fila in reader:
                puntajes.append([int(fila[10]),int(fila[7])])
        self.sort(puntajes)
        primeros_cinco = puntajes[:5]
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
                elif int(fila[7]) == ganador2:
                    usuario2 = fila[0]
                    foto2 = fila[4]
                elif int(fila[7]) == ganador3:
                    usuario3 = fila[0]
                    foto3 = fila[4]
                elif int(fila[7]) == ganador4:
                    usuario4 = fila[0]
                    foto4 = fila[4]
                elif int(fila[7]) == ganador5:
                    usuario5 = fila[0]
                    foto5 = fila[4]

    def Regresar(self,modo):
        ventana11.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()

    def __init__(self, top5, modo):
        self.Iniciar_Variables(top5)
        global ventana11
        ventana11 = Tk()
        ventana11.geometry("900x800")
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
        boton.place(x= 375, y= 700)
        imagen14 = Image.open("Campeón.png")
        imagen15 = imagen14.resize(nuevo_tamaño)
        imagen16 = ImageTk.PhotoImage(imagen15)
        label_imagen6 = tk.Label(image=imagen16)
        label_imagen6.place(x=100, y=15)
        if puntuacion1 == 0:
            label19 = Label(ventana11, text="Disponible", font=("fixedsys", 20), fg="white", bg="black")
            label19.place(x=450, y=100)
        else:
            imagen1 = Image.open("C:/Users/PC/Desktop/2024/I semestre/Pruebas/Edison.png")
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
            imagen2 = Image.open("C:/Users/PC/Desktop/2024/I semestre/Pruebas/Edison.png")
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
            imagen5 = Image.open("C:/Users/PC/Desktop/2024/I semestre/Pruebas/Edison.png")
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
            imagen8 = Image.open("C:/Users/PC/Desktop/2024/I semestre/Pruebas/Edison.png")
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
            imagen11 = Image.open("C:/Users/PC/Desktop/2024/I semestre/Pruebas/Edison.png")
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
        ventana12.destroy()
        if modo == 1:
            Menú()
        else:
            Menú2()
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
        opciones = ["Patrón 1", "Patrón 2", "Patrón 3", "Patrón 4", "Patrón 5"]
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
        ventana12.mainloop()

class VentanaAyuda:
    def __init__(self, modo):
        self.modo = modo
        self.ventana13 = Tk()
        self.ventana13.configure(bg="black")
        self.ventana13.title("Ayuda del Videojuego")
        self.ventana13.geometry("400x400")

        # Contenido de la ventana de ayuda
        label = Label(self.ventana13, text="Aquí va el contenido de ayuda del videojuego")
        label.pack(pady=20)

        # Botón para cerrar la ventana de ayuda
        boton_cerrar = Button(self.ventana13, text="Cerrar", command=self.cerrar_ventana)
        boton_cerrar.pack(pady=10)

        self.ventana13.mainloop()

    def cerrar_ventana(self):
        self.ventana13.destroy()
        if self.modo == 1:
            Menú()
        else:
            Menú2()

#ConfiguracionDeLaPartida()
inicio = Inicio()
inicio.InicioSesion()
#Menú2()
