from tkinter import *
import DatosDeUsuario


# Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

global numero_usuario

class Menú:
    def ComaprarLetras(self):
        print("presionó")
    def Datos(self):
        ventana.destroy()
        dato = DatosDeUsuario
        dato.Datos.obtenerPosi(dato, numero_usuario)
        dato.Datos.iniciarVariables(dato)
        dato.Datos()
    def usuario(self, posicion):
        global numero_usuario
        numero_usuario = posicion
        print(numero_usuario)
    def __init__(self):
        global ventana
        ventana = Tk()
        ventana.geometry("900x450")
        #Botón para editar configuaciones
        boton = Button(text = "Editar configuración del usuario", command = self.Datos)
        boton.place(x = 300, y = 70)
        # Botón para ver salón de la fama
        boton = Button(text="Salón de la fama", command=self.ComaprarLetras)
        boton.place(x=300, y=100)
        #Botón para editar configuración de la partida
        boton2 = Button(text="Editar configuración de la partida", command=self.ComaprarLetras)
        boton2.place(x=300, y=130)
        # Botón para iniciar jugador 2
        boton = Button(text="Iniciar jugador 2", command=self.ComaprarLetras)
        boton.place(x=300, y=160)
        #Botón para iniciar partida
        boton3 = Button(text="Iniciar partida", command=self.ComaprarLetras)
        boton3.place(x=285, y=190)
        #Botón para salir del juego
        boton4 = Button(text="Salir del juego", command=self.ComaprarLetras)
        boton4.place(x=310, y=220)
        print("muestra")
        ventana.mainloop()


#objeto = Menú()
#objeto.Menu()