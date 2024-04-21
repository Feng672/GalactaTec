import pygame, random 

WIDTH = 800 # Ancho de ventana 
HEIGHT = 600 # Alto de ventana 
Black = (0,0,0)
White = (255,255,255)
Green = (0,255,0)

pygame.init()
pygame.mixer.init()    # Sonido 
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Ventana 
pygame.display.set_caption("GALAGA")   # Nombre del juego en pantalla 
Clock = pygame.time.Clock()   # Reloj

def draw_text (surface,text, size, x, y): #Funcion hace que pueda dibunar letras en pantalla
    font = pygame.font.SysFont("serif",size) # Tipo de letra fuente 
    text_surface = font.render (text,True, White)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect) # donde pintar  

def draw_shield_bar(surface, x, y, porcentaje): # Funcion de barra de vida
    BAR_LENGHT = 100 #Largo de barra
    BAR_HEIGHT = 10
    fill = (porcentaje / 100)* BAR_LENGHT #Calculo de % de barra 
    border = pygame.Rect(x,y,BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface, Green,fill)  #color de barra
    pygame.draw.rect (surface, White,border, 2)
    
class Player (pygame.sprite.Sprite):     # Clase del jugador 
    def __init__(self): 
        super(). __init__()
        self.image = pygame.image.load("assets/player.png").convert()    # Imagen del jugador 
        self.image.set_colorkey(Black)    # Renueve el fondo negro de la imagen del jugador 
        self.rect = self.image.get_rect()  # Centrara la imagen del jugador 
        self.rect.centerx = WIDTH // 2   #Lugar de centrado de imagen 
        self.rect.bottom = HEIGHT - 10 
        self.speed = 0  # Velocidad de movimiento
        self.shield = 100

    def update (self):   # Movimiento de nave 
        self.speed_x = 0 # Velocidad 
        keystate = pygame.key.get_pressed()   # Verifica si alguna tecla es precionada 
        if keystate [pygame.K_LEFT]:   # Si se pulso la izquierda.  
            self.speed_x = -5     # Se muevo a la izquierda.
        if keystate [pygame.K_RIGHT]: # Si se pulso la derecha. 
            self.speed_x = 5     # Se muevo a la derecha
        self.rect.x += self.speed_x 
        if self.rect.right > WIDTH : # Para que la nave no se salga de la pantalla 
            self.rect.right = WIDTH
        if self.rect.left < 0 : # Para que la nave no se salga de la pantalla
            self.rect.left = 0

    def shoot (self):
        bullet = Bullet (self.rect.centerx,self.rect.top) #Crear una bala
        all_sprites.add (bullet) # Agrega la funcion a los sprites
        bullets.add (bullet) #lista de balas
        laser_sound.play()

class Meteoro (pygame.sprite.Sprite):
    def __init__(self):    # Inicio de clase
        super(). __init__()
        self.image = random.choice (meteor_images)    # Imagen del meteoro
        self.image.set_colorkey(Black)    # Renueve el fondo negro de la imagen del jugador
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (WIDTH - self.rect.width)     # Lugar al azar del meteoro.
        self.rect.y = random.randrange (-140, -100)     # Lugar al azar del meteoro.
        self.speedy = random.randrange (1, 10)   # Velocidad de caida
        self.speedx = random.randrange (-5, 5) # Aleacion de meteoros


    def update (self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40: # si ya rebaso el alto de la ventana
            self.rect.x = random.randrange (WIDTH - self.rect.width)     # Lugar al azar del meteoro.
            self.rect.y = random.randrange (-100, -40)     # Lugar al azar del meteoro.
            self.speedy = random.randrange (1, 10)   # Velocidad de caida

class Bullet (pygame.sprite.Sprite):
    def __init__ (self, x, y):  # definicion de parametros de posicion
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10  # Negativo porque va de abajo hacia arriba 

    def update (self):
        self.rect.y += self.speedy  # Para que la bala suba en automatico 
        if self.rect.bottom    < 0:  # metodo para que la bala desaparesca al colicionar
            self.kill()

class Explosion(pygame.sprite.Sprite): #clase de explociones aleatorias
    def __init__ (self,center): # con esto podre centrar la explosion donde este el meteoro
        super(). __init__()
        self.image = explosion_anim [0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 # esa funcion hace el cambio de imagen.
        self.last_update = pygame.time.get_ticks ()
        self.frame_rate = 50 # velocidad de la explosion

    def update (self):
        now = pygame.time.get_ticks ()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim): #Averigua si ya se llego al fin de la lista
                self.kill()  # al llegar al final, eliminar las imagenes
            else:
                center = self.rect.center
                self.image = explosion_anim [self.frame]
                self.rect = self.image.get_rect ()
                self.rect.center = center 

def show_go_screen (): #Funcion de pantalla de game over
    screen.blit(background, [0,0])  # pone la imagen backgroun en la seccion de inicio
    draw_text(screen, "GALAGA", 65, WIDTH // 2, HEIGHT // 4 )
    draw_text(screen, "Instrucciones", 27, WIDTH //2, HEIGHT // 2)
    draw_text(screen, "Press key for start", 20, WIDTH //2, HEIGHT *3/4)
    pygame. display.flip()  # Mostrar en pantalla
    waiting = True
    while waiting:
        Clock.tick (60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False 


meteor_images = []  # lista para imagenes aleatoria
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list: #iteracion de imagenes
    meteor_images.append (pygame.image.load(img).convert())


#Explociones de meteoritos:
explosion_anim = []
for i in range (9):  #Bucle de imagenes
    file = "assets/regularExplosion0{}.png".format(i)  # Iteracion de todas la imagenes
    img = pygame.image.load(file).convert()
    img.set_colorkey(Black)
    img_scale = pygame.transform.scale (img, (70,70))
    explosion_anim.append (img_scale)  #cargado de imagenes 
            
# Cargar imagen de fondo 
background = pygame.image.load ("assets/background.png").convert()

#Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg") # Sonido laser 
explosion_sound = pygame.mixer.Sound("assets/explosion.wav") #sonido explosion 
pygame.mixer.music.load("assets/Cant Stop.mp3")  #sonido de fondo
pygame.mixer.music.set_volume(100)  #Volumen de musica 
        

pygame.mixer.music.play(loops =-1) # Musica infinita
game_over = True # fin del juego 


running = True 
while running:
    if game_over:
        show_go_screen()  #funcion de main 
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteoro_lista = pygame.sprite.Group() # Grupo de almacenamiento de meteoros
        bullets = pygame.sprite.Group()

        player = Player()   # Nombre del jugador 
        all_sprites.add(player)  # Añade al jugador a la lista.
        for i in range (8):
            meteoro = Meteoro ()
            all_sprites.add (meteoro)
            meteoro_lista.add(meteoro)
        score =  0  # Marcador 
   
    Clock.tick(60)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # tecla de barra espaciadora
                player.shoot ()  # cada que se presione, dispare 
        

    all_sprites.update()

    # Colisiones meteoro - laser
    hits = pygame.sprite.groupcollide(meteoro_lista, bullets, True, True)
    for hit in hits:  # Realiza que una vez el meteoro sea eliminado, reaparezca de nuevo. 
        score += 10 # Hace que el score aumente de 10 en 10
        explosion = Explosion(hit.rect.center) #Agrego de explosion al colicionar 
        all_sprites.add(explosion)
        explosion_sound.play()
        meteoro = Meteoro ()     
        all_sprites.add (meteoro)
        meteoro_lista.add(meteoro) 

    # Colisiones jugador - meteoro
    hits = pygame.sprite.spritecollide (player, meteoro_lista, True) # True = los objetos que colisionen desaparecen.
    for hit in hits:  #Verifica si algo dentro de esta lista colisiona
        player.shield -= 25  # Cada una colision -25 pts de vida 
        if player.shield <= 0:   # si la vida es 0, termina el juego 
            game_over = True 

    
    screen.blit(background, [0,0]) # Inpresion de background en la pantalla principal

    all_sprites.draw(screen)

    #Marcador
    draw_text (screen, str(score), 25, WIDTH // 2,10)

    #Escudo
    draw_shield_bar(screen, 5, 5, player.shield)  # Barra de vida 
    
    pygame.display.flip()
pygame.quit()

