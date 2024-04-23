from tkinter import *
import Registro
import csv
from tkinter import messagebox
import MenúPrincipal
import random
import yagmail
import threading
import time

# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

nombre_archivo = "registro.csv"
numero_usuario = None
email = 'progra672@gmail.com'
contraseña = 'znioymdmmtslkgar'
global destinatario
#destinatario = 'bryanfeng01@gmail.com'
asunto = 'Recuperación de contraseña'
mensaje = 'Este es tu código de verificación'
yag = yagmail.SMTP(user = email, password=contraseña)
#yag.send(destinatario, asunto, mensaje)


class Inicio:
    def InicioDeSesion(self, usuario, contraseña, archivo):
        if usuario == "" or contraseña == "":
            messagebox.showinfo(message = "Hay un campo vacío", title = "Error")
        elif self.usuario_correcto(usuario, contraseña, archivo) == False:
            messagebox.showinfo(message = "Usuario o contraseña incorrecta", title = "Error")
        else:
            ventana.destroy()
            menu = MenúPrincipal
            menu.Menú.usuario(menu,numero_usuario)
            menu.Menú()
            #messagebox.showinfo(message = "Usuario existente", title = "Éxito")
    def RecuperarContraAux(self, correo):
        if self.CorreoExiste(correo) == True:
            global correo2
            correo2 = correo
            self.generar_codigo()
            global ventana3
            ventana3 = Tk()
            ventana3.geometry("900x450")
            #Caja de código de verificación
            caja4 = Entry(ventana3)
            caja4.place(x=280, y=70)
            label4 = Label(ventana3, text="Código:")
            label4.place(x=230, y=70)
            # Botón de verificar
            boton4 = Button(ventana3, text ="Verificar", command=lambda : self.VerificarCodigo(self.codigo, int(caja4.get())))
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
            yag.send(correo2, asunto, mensaje + "," + str(self.codigo))
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
            ventana4.geometry("900x450")
            #Caja de contraseña nueva
            caja5 = Entry(ventana4)
            caja5.place(x=310, y=70)
            label5 = Label(ventana4, text="Contraseña:")
            label5.place(x=230, y=70)
            #Botón de cambiar contraseña
            boton5 = Button(text="Confirmar", command=lambda: self.CambioDeContra(caja5.get(), contraCambiar))
            boton5.place(x=310, y=130)
            ventana4.mainloop()
        else:
            messagebox.showinfo(message="Código erróneo", title="Error")
    def CambioDeContra(self, contraseña_nueva, posicion):
        verificar = Registro.registro
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
        ventana2.geometry("900x450")
        #Caja de texto de correo
        caja3 = Entry()
        caja3.place(x=280, y=70)
        label3 = Label(ventana2, text="Correo:")
        label3.place(x=230, y=70)
        #Botón de enviar
        boton4 = Button(text="Enviar", command=lambda : self.RecuperarContraAux(caja3.get()))
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
        Registro.registro()
    def InicioSesion(self):
        self.timer = None
        self.codigo = None
        self.tiempo_inicio = None
        self.tiempo_expiracion = None
        global ventana
        ventana = Tk()
        ventana.geometry("900x450")
        #Caja de texto de usuario
        caja = Entry()
        caja.place(x = 280, y = 70)
        label = Label(ventana, text="Usuario:")
        label.place(x = 230, y = 70)
        #Caja de texto de contraseña
        caja2 = Entry()
        caja2.place(x=280, y=100)
        label2 = Label(ventana, text="Contraseña:")
        label2.place(x=210, y=100)
        #Botón para registrarse
        boton = Button(text = "Registrarse", command = self.Ventana_registro)
        boton.place(x = 310, y = 130)
        #Botón para iniciar sesión
        boton2 = Button(text="Iniciar sesión", command= lambda: self.InicioDeSesion(caja.get(), caja2.get(), nombre_archivo))
        boton2.place(x=300, y=160)
        #Botón para recuperar contraseña
        boton3 = Button(text="Recuperar contraseña", command=self.RecuperarContra)
        boton3.place(x=285, y=190)
        ventana.mainloop()


inicio = Inicio()
inicio.InicioSesion()