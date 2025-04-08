from NQueensSolver import QueensVisualizer
from PhoneKnight import EnhancedKnightVisualizer

if __name__ == "__main__":
    # Para el caballo
    visualizer = EnhancedKnightVisualizer(k=2)
    visualizer.run()
    
    # Para las reinas
    # queens_vis = QueensVisualizer(n=8)
    # queens_vis.run()