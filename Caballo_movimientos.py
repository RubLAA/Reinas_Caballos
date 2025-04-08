from functools import lru_cache

def caballo_movimientos():
    @lru_cache(maxsize=None)
    def movimientos_caballo(k):
        movs = {
            0: [4,6], 1: [6,8], 2: [7,9], 3: [4,8],
            4: [0,3,9], 5: [], 6: [0,1,7], 7: [2,6],
            8: [1,3], 9: [2,4]
        }
        if k == 0: return {n:1 for n in range(10)}
        prev = movimientos_caballo(k-1)
        return {n: sum(prev[m] for m in movs[n]) for n in range(10)}

    k_values = [1,2,3,5,8,10,15,18,21,23,32]
    print("{:<10} {:<15}".format("Movimientos", "Total"))
    for k in k_values:
        total = sum(movimientos_caballo(k).values())
        print("{:<10} {:<15}".format(k, total))