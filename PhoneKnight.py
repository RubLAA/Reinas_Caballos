import pygame
import sys
import multiprocessing as mp
from pygame.math import Vector2
from colorsys import hsv_to_rgb
from datetime import datetime, timedelta

# Configuración común
KEY_POSITIONS = {
    0: (250, 480),
    1: (125, 180), 2: (250, 180), 3: (375, 180),
    4: (125, 280), 5: (250, 280), 6: (375, 280),
    7: (125, 380), 8: (250, 380), 9: (375, 380)
}

# ----------------------------
# Ventana de Animación
# ----------------------------
def animation_window(k, paths_queue):
    class AnimatedKnight:
        def __init__(self):
            self.image = pygame.image.load('caballero.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
            self.pos = Vector2(KEY_POSITIONS[0])
            self.speed = 0.2  # Velocidad ajustada
        
        def update(self, target_pos, dt):
            direction = target_pos - self.pos
            if direction.length() > 2:
                direction.normalize_ip()
                self.pos += direction * self.speed * dt
        
        def draw(self, surface):
            surface.blit(self.image, self.pos - Vector2(20, 20))

    pygame.init()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Animación del Caballo")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    
    knight = AnimatedKnight()
    paths = generate_paths(k)
    
    # Generar colores corregido
    colors = []
    if paths:
        colors = [
    tuple(int(c * 255) for c in hsv_to_rgb(i/len(paths), 0.8, 0.8))  # Paréntesis cerrado
    for i in range(len(paths))
]
    
    running = True
    current_path_index = 0
    current_step = 0
    last_time = pygame.time.get_ticks()
    
    while running:
        dt = pygame.time.get_ticks() - last_time
        last_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if current_path_index < len(paths):
            path = paths[current_path_index]
            target_pos = Vector2(KEY_POSITIONS[path[current_step]])
            
            knight.update(target_pos, dt)
            paths_queue.put((colors[current_path_index], Vector2(knight.pos)))
            
            if (knight.pos - target_pos).length() < 2:
                current_step += 1
                if current_step >= len(path):
                    current_path_index += 1
                    current_step = 0
        
        screen.fill((32, 32, 32))
        draw_interface(screen, font)
        knight.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

# ----------------------------
# Ventana de Rutas (Persistente)
# ----------------------------
def routes_window(paths_queue):
    class RouteVisualizer:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.background = pygame.Surface((800, 600))
            self.background.fill((255, 255, 255))
            self.paths = []
            self.end_time = None
        
        def run(self):
            start_time = datetime.now()
            running = True
            while running:
                if self.end_time and datetime.now() > self.end_time:
                    running = False
                
                # Recibir nuevos puntos
                while not paths_queue.empty():
                    color, pos = paths_queue.get()
                    if not self.paths or self.paths[-1]['color'] != color:
                        self.paths.append({'color': color, 'points': []})
                    self.paths[-1]['points'].append(pos)
                    self.end_time = datetime.now() + timedelta(minutes=5)
                
                # Dibujar rutas
                self.screen.blit(self.background, (0, 0))
                for path in self.paths:
                    if len(path['points']) > 1:
                        pygame.draw.aalines(
                            self.screen, 
                            path['color'], 
                            False, 
                            path['points'], 
                            3
                        )
                pygame.display.flip()
                
                # Manejar eventos
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
            pygame.quit()

    visualizer = RouteVisualizer()
    visualizer.run()

# ----------------------------
# Funciones Auxiliares
# ----------------------------
def generate_paths(k):
    """Genera rutas válidas de k pasos (ejemplo)"""
    return [
        [0, 4, 3, 8],
        [0, 6, 1, 8]
    ]

def draw_interface(surface, font):
    """Dibuja el teclado numérico"""
    pygame.draw.rect(surface, (50, 50, 50), (50, 100, 400, 400), border_radius=20)
    for num, pos in KEY_POSITIONS.items():
        color = (100, 100, 100) if num != 5 else (150, 50, 50)
        pygame.draw.circle(surface, color, pos, 35)
        text = font.render(str(num), True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=pos))

# ----------------------------
# Lanzador Principal
# ----------------------------
if __name__ == '__main__':
    mp.freeze_support()
    k = 3
    paths_queue = mp.Queue()
    
    anim_proc = mp.Process(target=animation_window, args=(k, paths_queue))
    viz_proc = mp.Process(target=routes_window, args=(paths_queue,))
    
    anim_proc.start()
    viz_proc.start()
    
    anim_proc.join()
    viz_proc.join()