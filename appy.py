import pygame
import random

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 850, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador 2D - Clasificación Kola Real")
clock = pygame.time.Clock()

# Definición de Colores
WHITE = (245, 245, 245)
BELT_GRAY = (120, 120, 120)
CAMERA_BLUE = (0, 122, 204)
TEXT_COLOR = (50, 50, 50)

COLOR_ROJA = (220, 20, 60)   # KR Fresa
COLOR_AMARILLA = (255, 215, 0) # KR Piña
COLOR_NEGRA = (30, 30, 30)   # KR Cola

# Fuentes de texto
font = pygame.font.SysFont("Arial", 16, bold=True)
title_font = pygame.font.SysFont("Arial", 22, bold=True)

# Contadores
contadores = {'Fresa': 0, 'Piña': 0, 'Cola': 0}

class Botella:
    def __init__(self):
        self.x = 0
        self.y = 200
        self.tipo = random.choices(['Fresa', 'Piña', 'Cola'], weights=[30, 30, 40])[0]
        self.speed_x = 4
        self.speed_y = 2
        
        # Asignar color y carril de destino según el sabor
        if self.tipo == 'Fresa':
            self.color = COLOR_ROJA
            self.target_y = 80
        elif self.tipo == 'Piña':
            self.color = COLOR_AMARILLA
            self.target_y = 200
        else:
            self.color = COLOR_NEGRA
            self.target_y = 320

    def move(self):
        # Movimiento en la faja principal
        if self.x < 400:
            self.x += self.speed_x
        else:
            # Movimiento de desvío (Servomotores)
            self.x += self.speed_x
            if self.y < self.target_y:
                self.y += self.speed_y
            elif self.y > self.target_y:
                self.y -= self.speed_y

    def draw(self, surface):
        # Dibujar la botella (Círculo)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 12)
        # Brillo del envase
        pygame.draw.circle(surface, (255,255,255), (int(self.x - 4), int(self.y - 4)), 3)

botellas = []
spawn_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(WHITE)
    
    # 1. Dibujar Fajas Transportadoras
    # Faja Principal
    pygame.draw.rect(screen, BELT_GRAY, (0, 185, 400, 30))
    # Carriles de desvío
    pygame.draw.rect(screen, BELT_GRAY, (400, 65, 450, 30))  # Carril A (Arriba)
    pygame.draw.rect(screen, BELT_GRAY, (400, 185, 450, 30)) # Carril B (Centro)
    pygame.draw.rect(screen, BELT_GRAY, (400, 305, 450, 30)) # Carril C (Abajo)
    
    # 2. Dibujar la Cámara Inteligente
    pygame.draw.rect(screen, CAMERA_BLUE, (380, 130, 40, 40), border_radius=5)
    pygame.draw.circle(screen, (20,20,20), (400, 150), 10) # Lente
    
    # 3. Lógica de aparición de botellas (Spawner)
    spawn_timer += 1
    if spawn_timer > 45: # Generar una botella cada 45 frames
        botellas.append(Botella())
        spawn_timer = 0
        
    # 4. Mover y dibujar botellas
    for b in botellas[:]:
        b.move()
        b.draw(screen)
        
        # Si pasa por la cámara, sumar al contador (solo cuenta una vez)
        if 398 <= b.x <= 402:
            contadores[b.tipo] += 1
            
        # Eliminar botella si sale de la pantalla
        if b.x > WIDTH + 20:
            botellas.remove(b)
            
    # 5. Textos e Interfaz
    screen.blit(title_font.render("Simulador de Selección Visual - Industrias San Miguel", True, TEXT_COLOR), (20, 20))
    
    # Etiquetas de carriles
    screen.blit(font.render(f"Carril A (Fresa): {contadores['Fresa']}", True, COLOR_ROJA), (650, 40))
    screen.blit(font.render(f"Carril B (Piña): {contadores['Piña']}", True, (200, 180, 0)), (650, 160))
    screen.blit(font.render(f"Carril C (Cola): {contadores['Cola']}", True, COLOR_NEGRA), (650, 280))
    screen.blit(font.render("Sensor Cámara IA", True, CAMERA_BLUE), (340, 105))

    pygame.display.flip()
    clock.tick(60) # 60 FPS (Velocidad de la simulación)

pygame.quit()
