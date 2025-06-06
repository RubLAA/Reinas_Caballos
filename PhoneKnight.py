import pygame
import sys
from pygame.math import Vector2
from math import sin
from colorsys import hsv_to_rgb

class PhoneKnight:
    def __init__(self):
        self.movements = {
            0: [4, 6], 
            1: [6, 8], 
            2: [7, 9], 
            3: [4, 8],
            4: [0, 3, 9], 
            5: [], 
            6: [0, 1, 7], 
            7: [2, 6],
            8: [1, 3], 
            9: [2, 4]
        }
        self.dp = None

    def calculate_moves(self, k):
        self.dp = [[0]*10 for _ in range(k+1)]
        for i in range(10): self.dp[0][i] = 1
        
        for step in range(1, k+1):
            for num in range(10):
                for dest in self.movements[num]:
                    self.dp[step][dest] += self.dp[step-1][num]
        return sum(self.dp[k])

class AnimatedKnight:
    def __init__(self, start_pos):
        self.original_image = pygame.image.load('sprites/caballero.png')  # Asegúrate de tener una imagen
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect(center=start_pos)
        self.current_pos = start_pos
        self.target_pos = start_pos
        self.speed = 5
        self.angle = 0

    def update(self):
        dx = self.target_pos[0] - self.current_pos[0]
        dy = self.target_pos[1] - self.current_pos[1]
        
        if dx != 0 or dy != 0:
            self.current_pos = (
                self.current_pos[0] + dx/self.speed,
                self.current_pos[1] + dy/self.speed
            )
            self.angle = sin(pygame.time.get_ticks() * 0.005) * 15  # Efecto de balanceo

        self.rect.center = self.current_pos

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)

class EnhancedKnightVisualizer:
    def __init__(self, k):
        pygame.init()
        self.k = k
        self.knight_logic = PhoneKnight()
        self.total_moves = self.knight_logic.calculate_moves(k)
        
        # Configuración de pantalla
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Caballo de Ajedrez Animado")
        
        # Configuración visual
        self.colors = {
            'background': (32, 32, 32),
            'keys': (80, 80, 80),
            'text': (240, 240, 240)
        }
        
        # Posiciones del teclado (coordenadas verificadas)
        self.key_positions = {
            0: Vector2(250, 480),
            1: Vector2(125, 180), 2: Vector2(250, 180), 3: Vector2(375, 180),
            4: Vector2(125, 280), 5: Vector2(250, 280), 6: Vector2(375, 280),
            7: Vector2(125, 380), 8: Vector2(250, 380), 9: Vector2(375, 380)
        }
        
        # Inicialización del caballo
        self.knight_pos = Vector2(self.key_positions[0])
        self.knight_angle = 0
        self.load_knight_sprite()
        
        # Generación de rutas
        self.paths = self.generate_valid_paths()
        self.current_path_index = 0
        self.current_step = 0

        self.running_animation = True  # Nuevo flag de control

        self.current_trail = []  # Almacena puntos de la estela
        self.trail_colors = []  # Almacena colores por ruta
        self.current_color = (255, 0, 0)  # Color inicial
        self.trail_history = []  # Lista de tuplas (color, puntos)

    def load_knight_sprite(self):
        """Carga y escala el sprite del caballo"""
        self.knight_img = pygame.image.load('sprites/caballero.png').convert_alpha()
        self.knight_img = pygame.transform.scale(self.knight_img, (40, 40))

    def generate_valid_paths(self):
        """Genera TODOS los caminos válidos desde TODAS las posiciones iniciales"""
        from collections import deque
        
        valid_paths = []
        
        # Explorar desde todas las posiciones iniciales (0-9, excepto 5)
        start_positions = [n for n in range(10) if n != 5]  # El 5 no tiene movimientos
        
        for start in start_positions:
            queue = deque([(start, [start])])
            
            while queue:
                current_pos, path = queue.popleft()
                
                if len(path) == self.k + 1:
                    valid_paths.append(path)
                    continue
                    
                for move in sorted(self.knight_logic.movements[current_pos]):
                    queue.append((move, path + [move]))
        
        # Generar colores únicos para todas las rutas
        if valid_paths:
            self.route_colors = [
                tuple(int(c * 255) for c in hsv_to_rgb(i/len(valid_paths), 0.8, 0.8))
                for i in range(len(valid_paths))
            ]
        
        print(f"Total de rutas generadas: {len(valid_paths)}")
        return valid_paths

    def draw_interface(self):
        """Dibuja la interfaz de usuario"""
        self.screen.fill(self.colors['background'])
        
        # Panel informativo
        font = pygame.font.Font(None, 28)
        title = font.render(f"Movimientos válidos: {self.total_moves}", True, (200, 200, 255))
        self.screen.blit(title, (20, 20))
        
        # Dibujar teclado
        pygame.draw.rect(self.screen, (50, 50, 50), (50, 100, 400, 400), border_radius=20)
        for num, pos in self.key_positions.items():
            color = self.colors['keys'] if num != 5 else (150, 50, 50)
            pygame.draw.circle(self.screen, color, pos, 35)
            pygame.draw.circle(self.screen, (30, 30, 30), pos, 35, 3)
            text = font.render(str(num), True, self.colors['text'])
            self.screen.blit(text, text.get_rect(center=pos))

    def update_knight_position(self):
        if not self.running_animation:
            return
            
        if not self.paths or self.current_path_index >= len(self.paths):
            self.running_animation = False
            return
            
        current_path = self.paths[self.current_path_index]
        
        if self.current_step < len(current_path) - 1:
            self.current_trail.append(Vector2(self.knight_pos))
            
            target_num = current_path[self.current_step + 1]
            target_pos = self.key_positions[target_num]
            
            if (self.knight_pos - target_pos).length() <= 2:
                self.current_step += 1
                if self.current_step >= len(current_path) - 1:
                    self.save_current_trail()
                    self.next_path()
                return
                
            direction = target_pos - self.knight_pos
            direction.normalize_ip()
            self.knight_pos += direction * min(150, direction.length())
            self.knight_angle = sin(pygame.time.get_ticks() * 0.008) * 15


    def next_path(self):
        """Prepara la siguiente ruta o finaliza"""
        self.current_path_index += 1
        if self.current_path_index < len(self.paths):
            self.current_step = 0
            start_pos = self.paths[self.current_path_index][0]  # Primera posición de la ruta
            self.knight_pos = Vector2(self.key_positions[start_pos])
        else:
            self.running_animation = False

    def save_current_trail(self):
        """Guarda la estela actual con su color correspondiente"""
        if self.current_trail and self.current_path_index < len(self.route_colors):
            self.trail_history.append((
                self.route_colors[self.current_path_index],
                self.current_trail.copy()
            ))
            self.current_trail.clear()

    def draw_trails(self):
        # Dibujar todas las estelas históricas
        for color, trail in self.trail_history:
            if len(trail) >= 2:
                pygame.draw.aalines(self.screen, color, False, trail, 3)
        
        # Dibujar estela actual
        if len(self.current_trail) >= 2:
            current_color = self.route_colors[self.current_path_index]
            pygame.draw.aalines(self.screen, current_color, False, self.current_trail, 3)

    def draw_knight(self):
        """Dibuja el caballo con rotación"""
        rotated_img = pygame.transform.rotate(self.knight_img, self.knight_angle)
        rect = rotated_img.get_rect(center=self.knight_pos)
        self.screen.blit(rotated_img, rect.topleft)

    def run(self):
        """Bucle principal de ejecución"""
        clock = pygame.time.Clock()
        while self.running_animation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.time.wait(15000)
                    pygame.quit()
                    sys.exit()
            
            self.update_knight_position()
            self.screen.fill(self.colors['background'])
            self.draw_interface()
            self.draw_trails()  # Dibujar antes que el caballo
            self.draw_knight()
            pygame.display.flip()
            clock.tick(60)