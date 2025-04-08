import pygame
import sys
from itertools import permutations
import argparse
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NQueensSolver:
    def __init__(self, n, visualize=False):
        self.n = n
        self.visualize = visualize
        self.solution = None
        self.sprite_path = "sprites/reina.png"
        
    def solve(self):
        """Resuelve el problema de las N-Reinas usando un enfoque optimizado"""
        logging.info(f"Iniciando resolución para {self.n}-Reinas")
        
        cols = range(self.n)
        for i, intento in enumerate(permutations(cols)):
            if self._es_solucion_valida(intento):
                self.solution = intento
                logging.info(f"Solución encontrada en el intento {i}")
                return True
        return False
    
    def _es_solucion_valida(self, intento):
        """Verifica si una permutación es una solución válida"""
        return all(abs(i - j) != abs(intento[i] - intento[j]) 
                for i in range(self.n) for j in range(i + 1, self.n))
    
    def visualize_solution(self):
        """Muestra la solución gráficamente usando Pygame"""
        if not self.solution:
            logging.error("No hay solución para visualizar")
            return
        
        pygame.init()
        ancho = 800 if self.n > 10 else 600
        tamano_celda = ancho // self.n
        alto = tamano_celda * self.n
        
        try:
            imagen_reina = pygame.image.load(self.sprite_path)
            imagen_reina = pygame.transform.scale(imagen_reina, 
                (int(tamano_celda * 0.9), int(tamano_celda * 0.9)))
        except FileNotFoundError:
            logging.error(f"No se encontró el sprite en {self.sprite_path}")
            sys.exit()

        ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption(f"Solución {self.n}-Reinas")
        
        # Dibujar tablero
        ventana.fill((255, 255, 255))
        for fila in range(self.n):
            for columna in range(self.n):
                color = (240, 217, 181) if (fila + columna) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(ventana, color, 
                    (columna * tamano_celda, fila * tamano_celda, tamano_celda, tamano_celda))
        
        # Dibujar reinas
        for fila, columna in enumerate(self.solution):
            x = columna * tamano_celda + (tamano_celda * 0.05)
            y = fila * tamano_celda + (tamano_celda * 0.05)
            ventana.blit(imagen_reina, (x, y))
        
        pygame.display.update()
        logging.info("Visualización iniciada. Presione [X] para salir")
        
        # Bucle principal de eventos
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resolver problema de N-Reinas')
    parser.add_argument('--n', type=int, default=8, help='Número de reinas')
    parser.add_argument('--visualize', action='store_true', help='Mostrar solución gráfica')
    args = parser.parse_args()

    solver = NQueensSolver(args.n, args.visualize)
    if solver.solve():
        print(f"Solución encontrada para {args.n}-Reinas:")
        print(solver.solution)
        if args.visualize:
            solver.visualize_solution()
    else:
        print(f"No se encontró solución para {args.n}-Reinas")