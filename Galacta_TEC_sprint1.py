# Importar bibliotecas
from tkinter import *

#Ventana de los mejores jugadores
class TopPlayersWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Salon de la fama")
        self.minsize(500, 500)
        self.config(bg="black")

        labels = ["First:", "Second:", "Third:", "Fourth:", "Fifth:"]
        for i, label_text in enumerate(labels):
            Label(self, text=label_text, bg="black", fg="white", font=('fixedsys', 20)).grid(row=i + 1, column=0, padx=5, pady=5)

        # Botón de regreso al menú
        Button(self, text="Atrás", bg='black', fg='white', font=('fixedsys', 20), command=self.back_to_main_menu).grid(row=6, column=0, padx=5, pady=5)

    #Función para volver al menu
    def back_to_main_menu(self):
        self.destroy()
        self.master.deiconify()

class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = Tk()
        self.ventana.title("GalactaTEC")
        self.ventana.minsize(500, 500)
        self.ventana.resizable(width=NO, height=NO)

        #Botón de salon de la fama
        btn_top = Button(self.ventana, text='Salon de la fama', bg='black', fg='white', font=('fixedsys', 20), command=self.show_top_players)
        btn_top.place(x=125, y=200)

        self.ventana.mainloop()

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
        
#Termina
if __name__ == "__main__":
    main_menu = MainMenu(None)



