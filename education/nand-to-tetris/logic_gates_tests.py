from logic_gates import *

print("Test cases \n")

def test_maker(gate, output_tuples):
    # See below func def for usage
    # Last value in tuple is result
    # Values before it are the input
    title = gate.__name__
    print(title + "() tests:")
    for i in output_tuples:
        print(title + str(i[0:-1]) +" == " + str(i[-1]), end=" ")
        print(gate(*i[0:-1]) == i[-1])
    print("")

    return 0

test_maker(nt, ((0,1),(1,0)) )
test_maker(nand, ((0,0,1),(0,1,1),(1,1,0)) )
test_maker(and_, ((1,1,1),(0,1,0),(0,0,0)) )
test_maker(or_, ((0,0,0),(0,1,1),(1,0,1),(1,1,1)))
test_maker(xor, ((0,0,0),(0,1,1),(1,0,1),(1,1,0)))
