import pygame
import sys

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.solution = []
        
    def solve(self):
        def is_safe(board, row, col):
            for i in range(col):
                if board[i] == row or abs(board[i] - row) == col - i:
                    return False
            return True
        
        def backtrack(col=0, board=[]):
            if col == self.n:
                self.solution = board.copy()
                return True
            for row in range(self.n):
                if is_safe(board, row, col):
                    if backtrack(col+1, board + [row]):
                        return True
            return False
        
        return backtrack()

class QueensVisualizer:
    def __init__(self, n):
        self.n = n
        self.solver = NQueensSolver(n)
        self.solver.solve()
        
        pygame.init()
        self.size = 600
        self.cell_size = self.size // n
        self.screen = pygame.display.set_mode((self.size, self.size))
        self.colors = [(255, 206, 158), (209, 139, 71)]
        
    def draw_board(self):
        for row in range(self.n):
            for col in range(self.n):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, 
                               (col*self.cell_size, row*self.cell_size,
                                self.cell_size, self.cell_size))
                
    def draw_queens(self):
        for col, row in enumerate(self.solver.solution):
            x = col * self.cell_size + self.cell_size//2
            y = row * self.cell_size + self.cell_size//2
            pygame.draw.circle(self.screen, (200, 50, 50), (x, y), self.cell_size//3)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.draw_queens()
            pygame.display.flip()