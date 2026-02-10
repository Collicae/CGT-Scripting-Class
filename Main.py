from mymath import SolveAxPlusB, SolveHypotenuse

#Obtaining the Values
A_Value = float(input("Please enter in your first value: "))
B_Value = float(input("Please enter in your second value: "))


repeat_Question = input("Please enter 'a' if you would like to find Ax+B=0, or 'b' if you would like to find A^2 + B^2 = C^2: ").lower()

if repeat_Question not in ("a", "b"):
    raise ValueError ("Please enter either a or b")
else:
    if repeat_Question == "a":
        foundXorC = SolveAxPlusB(A_Value, B_Value)
    else:
        foundXorC = SolveHypotenuse(A_Value, B_Value)

print(foundXorC)