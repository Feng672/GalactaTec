#Importar Bibliotecas
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ventana de Menú")
icono = pygame.image.load("Assets/nave_screen.png")
pygame.display.set_icon(icono)

# Definir dimensiones de la ventana de las mejores 5 partidas
TOP_5_SCREEN_WIDTH = 400
TOP_5_SCREEN_HEIGHT = 400

#Definir dimensiones de la ventana de configuración
SETTINGS_SCREEN_WIDTH = 400
SETTINGS_SCREEN_HEIGHT = 400

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,221,0)
BLUE = (0,95,224)

# Fuente
font = pygame.font.Font(None, 36)

# Función para mostrar las mejores 5 partidas
def show_top_5():
    # Esta función mostraría las mejores 5 partidas en una nueva ventana
    show_top_5 = pygame.display.set_mode((TOP_5_SCREEN_WIDTH, TOP_5_SCREEN_HEIGHT))
    show_top_5.fill(BLACK)
    pygame.display.set_caption("Mejores 5 partidas")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        

#Función para mostrar la configuración de la partida
def show_settings():
    #Esta función mostraria la configuración de la partida
    show_settings = pygame.display.set_mode((SETTINGS_SCREEN_WIDTH, SETTINGS_SCREEN_HEIGHT))
    show_settings.fill(BLACK)
    pygame.display.set_caption("Configuraciones")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

#Función para Iniciar Jugador 2
def Player_2():
    #Esta función mostraria la configuración para player 2
    print("Iniciando Player 2")

#Función para iniciar la partida
def play():
    #Esta función mostraria la pantalla del cideojuego
    print("Playing...")

# Clase para crear botones
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, YELLOW)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Botón para mostrar las mejores 5 partidas
top_5_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 85, 200, 50, "Top 5", show_top_5)

#Botón para mostrar la configurtación de la partida
settings_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50, "Configuración", show_settings)

#Botón para iniciar player 2
iniciar_player2 = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 50, "Player 2", Player_2)

#Botón de iniciar partida
play_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 140, 200, 50, "Play", play)

def draw_menu():
    screen.fill(BLACK)
    top_5_button.draw(screen)
    settings_button.draw(screen)
    iniciar_player2.draw(screen)
    play_button.draw(screen)
    #pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            top_5_button.handle_event(event)
            settings_button.handle_event(event)
            iniciar_player2.handle_event(event)
            play_button.handle_event(event)

        draw_menu()

if __name__ == "__main__":
    main_menu()
