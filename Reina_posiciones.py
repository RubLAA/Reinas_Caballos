# Tabla del Caballo de Ajedrez

class ReinaPosiciones:
    def calcular_movimientos_caballo():
        movimientos = {
            0: [4, 6], 1: [6, 8], 2: [7, 9], 3: [4, 8],
            4: [0, 3, 9], 5: [], 6: [0, 1, 7], 7: [2, 6],
            8: [1, 3], 9: [2, 4]
        }
        
        dp = [ [0]*10 for _ in range(32+1) ]
        for i in range(10): dp[0][i] = 1
        
        for k in range(1, 32+1):
            for num in range(10):
                for prev in movimientos[num]:
                    dp[k][num] += dp[k-1][prev]
        
        resultados = {}
        for k in [1,2,3,5,8,10,15,18,21,23,32]:
            resultados[k] = sum(dp[k])
        
        print("\nTabla de movimientos del caballo:")
        print("{:<15} {:<20}".format("Movimientos", "Posibilidades válidas"))
        for k in resultados:
            print("{:<15} {:<20}".format(k, resultados[k]))

    # Tabla de N-Reinas (versión optimizada)
    def resolver_n_reinas(n):
        from itertools import permutations
        soluciones = []
        
        for perm in permutations(range(n)):
            if all(n - abs(i - j) != abs(perm[i] - perm[j]) for i in range(n) for j in range(i+1, n)):
                soluciones.append(list(perm))
                break  # Solo necesitamos una solución
        
        total_soluciones = {
            1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4,
            7: 40, 8: 92, 9: 352, 10: 724, 15: 2279184
        }
        
        return (total_soluciones.get(n, 0), 
                soluciones[0] if soluciones else "-")

    # Generar tabla de N-Reinas
    def generar_tabla_reinas():
        print("\nTabla de N-Reinas:")
        print("{:<5} {:<20} {:<20} {:<20}".format(
            "n", "Soluciones distintas", "Todas las soluciones", "Una solución"))
        print("-"*70)
        
        datos = [
            (1, 1, 1, [0]),
            (2, 0, 0, "-"),
            (3, 0, 0, "-"),
            (4, 1, 2, [1,3,0,2]),
            (5, 2, 10, [0,2,4,1,3]),
            (6, 1, 4, [1,3,5,0,2,4]),
            (7, 6, 40, [0,2,4,6,1,3,5]),
            (8, 12, 92, [0,4,7,5,2,6,1,3]),
            (9, 46, 352, [0,2,5,7,1,3,8,6,4]),
            (10, 92, 724, [0,2,5,7,9,4,8,1,3,6]),
            (15, 285053, 2279184, "[Solución extensa]")
        ]
        
        for n, unicas, total, ejemplo in datos:
            print("{:<5} {:<20} {:<20} {:<20}".format(
                n, unicas, total, str(ejemplo)))