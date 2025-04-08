from NQueensSolver import NQueensSolver
from Reina_posiciones import ReinaPosiciones
from PhoneKnight import EnhancedKnightVisualizer
from Caballo_movimientos import caballo_movimientos

def main():
    # Configuración
    n = 12  # Cambiar este valor según necesidad
    visualizar = True  # Cambiar a False para solo solución numérica
    
    solver = NQueensSolver(n, visualizar)
    if solver.solve():
        print("Solución encontrada:")
        print(solver.solution)
        if visualizar:
            solver.visualize_solution()
    else:
        print("No se encontró solución")

    ReinaPosiciones.calcular_movimientos_caballo()
    ReinaPosiciones.generar_tabla_reinas()

    visualizer = EnhancedKnightVisualizer(k=1)
    visualizer.run()

    caballo_movimientos()



if __name__ == "__main__":
    main()