def nand(a,b):
    if (a+b == 2):
        return 0
    else:
        return 1

def nt(a):
    return ((a+1) % 2)

def and_(a, b):
    return nt(
        nand(a, b)
    )

def or_(a, b): #0,0 gives 1,1 - - anything else gives anything else
    return nand(
        nand(a,nt(b)),
        nt(b)
        )
