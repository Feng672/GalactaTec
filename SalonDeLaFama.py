# Importar bibliotecas
from tkinter import *
import csv
from PIL import Image, ImageTk
import DatosDeUsuario

#Ventana de los mejores jugadores
class TopPlayersWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Salon de la fama")
        self.minsize(500, 500)
        self.config(bg="black")

        # Botón de regreso al menú
        Button(self, text="Atrás", bg='black', fg='white', font=('fixedsys', 20), command=self.back_to_main_menu).grid(row=10, column=1, padx=5, pady=5)

        # Leer datos del archivo csv
        self.load_data("registro.csv")

        # Labels de photo, name, score
        column_labels = ["Photo", "Name", "Score"]
        for i, label_text in enumerate(column_labels):
            Label(self, text=label_text, bg="black", fg="white", font=('fixedsys', 20)).grid(row=0, column=i+1, padx=5, pady=5)
            
        # Labels de first, second, third, fourth, fifth
        top_labels = ["First:", "Second:", "Third:", "Fourth:", "Fifth:"]
        for i, label_text in enumerate(top_labels):
            Label(self, text=label_text, bg="black", fg="white", font=('fixedsys', 20)).grid(row=i + 1, column=0, padx=5, pady=5)

        #Mostrar datos en la ventana
        self.show_data()

        #Mostrar imagen
        self.show_image()

    # Cargar datos de archivo
    def load_data(self, filename):
        self.data = []
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    #if int(row[4]) == filename:
                        #return self.data.append(row)
                    self.data.append(row)
        except FileNotFoundError:
            print("El archivo no se encontró")
        print("Datos cargados", self.data)

    def show_data(self):
        if self.data:
            for i, row in enumerate(self.data):
                for j, value in enumerate(row):
                    Label(self, text=value, bg="black", fg="white", font=('fixedsys', 20)).grid(row=i + 2, column=j, padx=5, pady=5)
        else:
            Label(self, text="No hay datos disponibles", bg="black", fg="white", font=('fixedsys', 20)).grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    def show_image(self):
        try:
            img = Image.open(r"\\Este equipo\\Descargas\\GalactaTec-main\\assets\\campeones.png")
            img = img.resize((200, 200), Image.ANTIALIAS)  # Redimensionar la imagen
            photo = ImageTk.PhotoImage(img)
            canvas = Canvas(self, bg="black", width=200, height=200)
            canvas.image = photo  
            canvas.create_image(0, 0, anchor=NW, image=photo)
            canvas.grid(row=1, column=5, rowspan=5, padx=10, pady=10)
        except FileNotFoundError:
            print("No se pudo encontrar la imagen")
            
    #Función para volver al menu
    def back_to_main_menu(self):
        self.destroy()
        self.master.deiconify()
        
#Ventana de los mejores jugadores
class SettingsGameWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración de la partida")
        self.minsize(500, 500)
        self.config(bg="black")

        # Botón de regreso al menú
        Button(self, text="Atrás", bg='black', fg='white', font=('fixedsys', 20), command=self.back_to_main_menu).grid(row=5, column=1, padx=5, pady=5)

        # Labels para los niveles de juego
        Label(self, text="Seleccione un nivel de juego:", bg="black", fg="white", font=('fixedsys', 20)).grid(row=1, column=1, padx=5, pady=5)

        # Variables para los niveles de juego
        self.selected_level = StringVar()

        # Radiobuttons para los niveles de juego
        levels = ["Fácil", "Intermedio", "Difícil"]
        for i, level in enumerate(levels):
            Radiobutton(self, text=level, variable=self.selected_level, value=level, bg="black", fg="white", font=('fixedsys', 20)).grid(row=i+2, column=1, padx=5, pady=5)

    #Función para volver al menú
    def back_to_main_menu(self):
        self.destroy()
        self.master.deiconify()

# Ventana de logueo para el jugador 2
class LoginWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        self.geometry("300x200")
        self.config(bg="black")

        # Etiqueta y entrada para el nombre de usuario
        Label(self, text="Nombre de usuario:", bg="black", fg="white", font=('fixedsys', 14)).pack()
        self.username_entry = Entry(self, bg="white", fg="black", font=('fixedsys', 14))
        self.username_entry.pack()

        # Etiqueta y entrada para la contraseña
        Label(self, text="Contraseña:", bg="black", fg="white", font=('fixedsys', 14)).pack()
        self.password_entry = Entry(self, bg="white", fg="black", font=('fixedsys', 14), show="*")
        self.password_entry.pack()

        # Botón para iniciar sesión
        Button(self, text="Iniciar Sesión", bg="black", fg="white", font=('fixedsys', 14), command=self.login).pack()

   
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
            
    def login(self):
        # Aquí agregarías la lógica para verificar el nombre de usuario y contraseña
        # Por ahora, simplemente imprimiré los valores de las entradas
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("Nombre de usuario:", username)
        print("Contraseña:", password)
        # Cierra la ventana de inicio de sesión después de imprimir los valores
        self.destroy()

class Menú:
    def Presionó(self):
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

    def logeo2(self):
        login_window = LoginWindow(ventana)
        # Bloquea la ventana principal mientras la ventana de inicio de sesión esté abierta
        ventana.wait_window(login_window)

    def Top_players(self):
        top_players_window = TopPlayersWindow(ventana)
        top_players_window.mainloop()

    def settings_game(self):
        settings_game_window = SettingsGameWindow(ventana)
        settings_game_window.mainloop()

    def salir_del_juego(self):
        ventana.destroy()

    def __init__(self):
        global ventana
        ventana = Tk()
        ventana.geometry("700x450")
        #Botón para editar configuaciones
        boton = Button(text = "Editar configuración del usuario", command = self.Datos)
        boton.place(x = 300, y = 70)
        # Botón para ver salón de la fama
        boton = Button(text="Salón de la fama", command=self.Top_players)
        boton.place(x=300, y=100)
        #Botón para editar configuración de la partida
        boton2 = Button(text="Configuración de la partida", command=self.settings_game)
        boton2.place(x=300, y=130)
        # Botón para iniciar jugador 2
        boton = Button(text="Iniciar jugador 2", command=self.logeo2)
        boton.place(x=300, y=160)
        #Botón para iniciar partida
        boton3 = Button(text="Iniciar partida", command=self.Presionó)
        boton3.place(x=285, y=190)
        #Botón para salir del juego
        boton4 = Button(text="Salir del juego", command=self.salir_del_juego)
        boton4.place(x=310, y=220)
        ventana.mainloop()

    # Función para mostrar los mejores jugadores
    def show_top_players(self):
        self.ventana.iconify()
        top_players_window = TopPlayersWindow(self.ventana)

        if False:
            # Si no hay mejores partidas guardadas, muestra "No disponible"
            self.no_data_label = Label(top_players_window, text="No disponible", bg="black", fg="white", font=('fixedsys', 20))
            self.no_data_label.place(x=250, y=250)
        else:
            # Si hay mejores partidas guardadas, muestra "Disponible"
            self.no_data_label = Label(top_players_window, text="Disponible", bg="black", fg="white", font=('fixedsys', 20))
            self.no_data_label.place(x=250, y=250)

objeto = Menú()
objeto.__init__()
