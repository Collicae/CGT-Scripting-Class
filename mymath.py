#For this file only include the function with the formulas

#formula Ax+B=0
def SolveAxPlusB(a, b):
    if a == 0:
        raise ValueError ("No solution A cannot be 0 ")
    return -b/a

#formula A^2 + B^2 = C^2
def SolveHypotenuse(a, b):
    c = a**2 + b**2
    return c